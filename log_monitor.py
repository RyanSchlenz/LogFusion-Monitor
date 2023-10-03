import os
import logging
import difflib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogFileEventHandler(FileSystemEventHandler):
    def __init__(self, entry_matcher, log_directory, activity_log_path, previous_contents, update_callback):
        super().__init__()
        self.entry_matcher = entry_matcher
        self.log_directory = log_directory
        self.activity_log_path = activity_log_path
        self.previous_contents = previous_contents
        self.update_callback = update_callback


    def on_modified(self, event):
        if event.is_directory:
            return  # Ignore changes to directories

        log_filename = os.path.basename(event.src_path)

        # Check if the modified file has the desired extensions (e.g., .log, .json, .csv)
        if log_filename.endswith((".log", ".json", ".csv")):
            logging.info(f"File {event.src_path} has been modified.")

            # Read the changes from the modified log file
            with open(event.src_path, 'r') as modified_log_file:
                new_contents = modified_log_file.read()

            # Compare the new contents with the previous contents
            previous = self.previous_contents.get(event.src_path, "")
            added_data, erased_data = self.get_changed_data(previous, new_contents)

            if added_data:
                # Log added data
                with open(self.activity_log_path, 'a') as activity_log_file:
                    activity_log_file.write(f"Added Data in {event.src_path}:\n")
                    activity_log_file.write(added_data)
                    activity_log_file.write("\n")

            if erased_data:
                # Log erased data
                with open(self.activity_log_path, 'a') as activity_log_file:
                    activity_log_file.write(f"Erased Data in {event.src_path}:\n")
                    activity_log_file.write(erased_data)
                    activity_log_file.write("\n")

            # Update the previous contents for future comparisons
            self.previous_contents[event.src_path] = new_contents

        # After detecting changes, call the update_callback
        if self.update_callback:
            self.update_callback()

    @staticmethod
    def get_changed_data(previous, new):
        d = difflib.Differ()
        diff = list(d.compare(previous.splitlines(), new.splitlines()))

        added_data = "\n".join(line[2:] for line in diff if line.startswith('+ '))
        erased_data = "\n".join(line[2:] for line in diff if line.startswith('- '))

        return added_data, erased_data

def start_file_monitoring(entry_matcher, log_directory, activity_log_path, update_callback=None):
    # Initialize the previous_contents dictionary with the current contents of monitored files
    previous_contents = {}
    for root, _, files in os.walk(log_directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                previous_contents[file_path] = f.read()

    # Start monitoring the log files within the specified log_directory for changes
    log_file_handler = LogFileEventHandler(entry_matcher, log_directory, activity_log_path, previous_contents,update_callback)
    log_observer = Observer()
    log_observer.schedule(log_file_handler, path=log_directory, recursive=False)
    log_observer.start()
    return log_observer
