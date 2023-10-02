import json
import config

def open_json_log_file(*paths):
    for path in paths:
        with open(path, 'r') as log_file:
            try:
                log_data = json.load(log_file)
                for log_entry in log_data:
                    yield json.dumps(log_entry)
            except json.JSONDecodeError:
                print(f"Invalid JSON in the file: {path}")

def parse_json_log(log_entry):
    r = {}
    try:
        log_data = json.loads(log_entry)
        user_data = log_data.get("user", {})

        r["name"] = user_data.get("name", "N/A")
        r["ip_address"] = user_data.get("ip_address", "N/A")
        r["UserId"] = user_data.get("UserId", "N/A")

        return r
    except json.JSONDecodeError:
        r["error"] = "Invalid JSON format"
        return r

def compare_json(*args):
    common_values = set(args[0]).intersection(*args[1:])
    return list(common_values)

def save_common_values_to_json():
    log_file_paths = config.LOG_FILE_PATHS
    output_file_path = config.JSON_FILE_PATH

    common_values = []
    for i, file_path1 in enumerate(log_file_paths):
        for file_path2 in log_file_paths[i + 1:]:
            data1 = list(open_json_log_file(file_path1))
            data2 = list(open_json_log_file(file_path2))
            common_values.extend(compare_json(data1, data2))

    with open(output_file_path, 'w') as json_file:
        json.dump(common_values, json_file, indent=4)

if __name__ == "__main__":
    save_common_values_to_json()
