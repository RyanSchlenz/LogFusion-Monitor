import os
import logging
import time
import datetime
from watchdog.observers import Observer
import config
from entry_matcher import EntryMatcher
from json_log_processing import save_common_values_to_json
import log_monitor

log_csv = config.CSV_FILE_PATH
json_matches = config.JSON_FILE_PATH
csv_matches = config.OUTPUT_FILE_PATH
activity_log = config.LOG_FILE_PATH
log_directory = config.LOG_DIRECTORY

def setup_logging(log_file_path):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[logging.FileHandler(log_file_path, mode='a')]
    )

def main():
    setup_logging(activity_log)

    csv_file_path = log_csv
    json_file_path = json_matches
    output_file_path = csv_matches
    log_file_path = activity_log

    try:
        logging.info("Calling JSON generation script...")
        save_common_values_to_json()
        logging.info("JSON generation script called.")
    except Exception as e:
        logging.error(f"Error calling JSON generation script: {str(e)}")

    wait_time = 0
    while not os.path.exists(json_file_path) and wait_time < 60:
        time.sleep(2)
        wait_time += 2

    if os.path.exists(json_file_path):
        logging.info("JSON file exists. Starting comparison...")
        entry_matcher = EntryMatcher(csv_file_path, json_file_path, output_file_path)
        entry_matcher.find_and_save_matching_entries()
        logging.info("Comparison completed.")
        logging.info(f"Success! {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")      

        # Start monitoring the log files within the specified log_directory for changes
        log_observer = log_monitor.start_file_monitoring(entry_matcher, log_directory, activity_log)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log_observer.stop()
        log_observer.join()
    else:
        logging.error(f"The file {json_file_path} does not exist.")

if __name__ == "__main__":
    main()
