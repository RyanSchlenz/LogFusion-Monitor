import csv
import json

class EntryMatcher:
    def __init__(self, csv_file_path, json_file_path, output_file_path):
        self.csv_file_path = csv_file_path
        self.json_file_path = json_file_path
        self.output_file_path = output_file_path

    def extract_ip_addresses(self, json_str):
        try:
            entry_dict = json.loads(json_str)
            user_data = entry_dict.get('user')
            if user_data:
                ip_address = user_data.get('ip_address')
                return ip_address
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        return None

    def find_and_save_matching_entries(self):
        csv_ip_addresses = set()
        with open(self.csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                csv_ip_addresses.add(row['ip_address'])

        with open(self.json_file_path, 'r') as json_file:
            try:
                json_data = json.load(json_file)
                matching_entries = []

                for entry_str in json_data:
                    ip_address = self.extract_ip_addresses(entry_str)
                    if ip_address and ip_address in csv_ip_addresses:
                        matching_entries.append(entry_str)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except FileNotFoundError:
                print(f"File not found: {self.json_file_path}")

        if matching_entries:
            with open(self.output_file_path, 'w') as output_file:
                output_file.write('\n'.join(matching_entries))
            print(f"Matching entries saved to {self.output_file_path}")
        else:
            print("No matching entries found.")

        with open(self.csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            extracted_ip_addresses = set(row['ip_address'] for row in csv_reader)
