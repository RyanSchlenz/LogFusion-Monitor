# log_monitoring.py
These scripts work together to process JSON log files, find common values, and monitor log file changes in real-time, logging added and erased data.

entry_matcher script:

EntryMatcher Class:
Purpose: 
This class is responsible for matching IP addresses extracted from JSON log entries with a set of IP addresses from a CSV file and saving the matching entries to an output file.

Methods:
  __init__(self, csv_file_path, json_file_path, output_file_path): Initializes the class with paths to the CSV file, JSON file, and output file.
  extract_ip_addresses(self, json_str): Extracts the IP address from a JSON log entry string.

  find_and_save_matching_entries(self): Compares IP addresses between the JSON log entries and CSV data, saving matching entries to the output file.

json_log_processing Module:

Purpose: 
This module provides functions for processing JSON log data.

Functions:
open_json_log_file(*paths): Opens JSON log files and yields their contents as JSON strings.

parse_json_log(log_entry): Parses a JSON log entry and extracts specific user-related data.

compare_json(*args): Compares lists of JSON log entries and returns common values.

save_common_values_to_json(): Compares JSON log files specified in a configuration and saves common values to a JSON file.


log_monitor Module:

Purpose: 
This module handles real-time monitoring of log files for changes.

Classes:
LogFileEventHandler: Subclass of FileSystemEventHandler, responsible for detecting file modifications and logging added/erased data.

start_file_monitoring(entry_matcher, log_directory, activity_log_path): Starts monitoring log files for changes.

main script:

Purpose: 
The main entry point of the script, orchestrating the entire log processing and monitoring workflow.

Steps:
Sets up logging to record activities.
Calls the save_common_values_to_json function to generate common values from JSON log files.
Waits for the JSON file to be created (waits up to 60 seconds).
If the JSON file exists, it initializes the EntryMatcher, performs matching, and starts log file monitoring.
The script runs continuously, with log monitoring active, until interrupted by a keyboard interrupt (Ctrl+C).
