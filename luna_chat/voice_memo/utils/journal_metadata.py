import json
from typing import Any

# Extract address information
def get_non_empty_value(key:str, dictionary:dict, default='') -> Any:
    value = dictionary.get(key, default)
    return value if value else default

class JournalMetadata:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            try:
                self.data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from {file_path}: {e}")
            
            # Extract top-level keys
            self.location_address = self.data.get("location_address", {})
            self.datetime_str = self.data.get("datetime", "")
            self.location_gps = self.data.get("location_gps", {})
            self.device_info = self.data.get("device_info", {})

            self.street = get_non_empty_value('street')
            self.zip_code = get_non_empty_value('zip_code')
            self.city = get_non_empty_value('city')
            self.state = get_non_empty_value('state')
            self.region = get_non_empty_value('region')

            address_parts = [self.street, self.zip_code, self.city, self.state, self.region]
            self.address_line = ', '.join(part for part in address_parts if part)
            
            self.date_obj = datetime.fromisoformat(datetime_str)

            self.short_date = date_obj.strftime("%y%m%d-%H%M")
            self.long_date = date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={address_line.replace(' ', '+')}"
            self.markdown_address_link = f"[{address_line}]({google_maps_link})"

            self.lat = location_gps.get("lattitude", 0)
            self.lon = location_gps.get("longitude", 0)
            self.alt = location_gps.get("altitude", 0)
            self.gps_link = f"https://www.google.com/maps?q={lat},{lon}"
            self.markdown_gps_link = f"[{lat}, {lon}, {alt}]({gps_link})"

    def get_location_address(self):
        return self.data.get('location_address', {})

    def get_datetime(self):
        return self.data.get('datetime', '')

    def get_location_gps(self):
        return self.data.get('location_gps', {})

    def get_device_info(self):
        return self.data.get('device_info', {})

# Example usage:
# journal_metadata = JournalMetadata('/path/to/your/json/file.json')
# print(journal_metadata.get_location_address())
# print(journal_metadata.get_datetime())
# print(journal_metadata.get_location_gps())
# print(journal_metadata.get_device_info())