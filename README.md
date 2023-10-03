# log_monitoring.py
These modules and the main script work together to process JSON log files, perform data comparisons based on IP address, and monitor log file changes, all while logging activities and errors in a separate activity log.


**Modules Explained:**

**entry_matcher module:**
This module defines a class called EntryMatcher, which is responsible for matching data between a CSV file and a JSON file.

The EntryMatcher class has methods to:
  Initialize the object with paths to CSV, JSON, and output files.
  Extract IP addresses from JSON data.
  Find and save matching entries between the CSV and JSON files.
  It uses the csv and json modules for file handling and JSON decoding.


**json_log_processing Module:**
This module provides functions for processing JSON log files. It also interacts with JSON log files and is used for data comparison and extraction.

open_json_log_file(*paths): Opens and reads JSON log files specified by paths. It yields JSON log entries as strings.

parse_json_log(log_entry): Parses a JSON log entry and extracts specific fields.

compare_json(*args): Compares multiple lists of JSON data and returns common values.

save_common_values_to_json(): Calls functions to open JSON log files, compare data, and save common values to a JSON file.


**log_monitor Module:**
This module handles monitoring changes in log files within a specified directory and provides a mechanism to detect and log changes in log files.

LogFileEventHandler is a class that inherits from FileSystemEventHandler. It watches for changes in log files (with specific extensions like .log, .json, .csv) and logs added and erased data.

start_file_monitoring() initializes file monitoring using the watchdog library and schedules the LogFileEventHandler.


**main script:**
This is the main script that orchestrates various tasks using the other modules.

It sets up logging to record script activities.

Calls the JSON generation script (save_common_values_to_json) to generate or update JSON data.

Waits for the JSON file to be created or updated, with a timeout of 60 seconds.

If the JSON file exists, it initializes the EntryMatcher class to compare data between CSV and JSON files.

Calls the find_and_save_matching_entries method of EntryMatcher to perform the comparison and save matching entries.

Starts monitoring log files using the log_monitor module, providing an update callback function (update_matches_files) that is called when changes are detected.

Handles a KeyboardInterrupt (Ctrl+C) to gracefully exit the script.

Logs relevant information about the script's progress and completion.
