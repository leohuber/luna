import json
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime

# Extract address information
def get_non_empty_value(key:str, dictionary:dict, default='') -> Any:
    value = dictionary.get(key, default)
    return value if value else default

@dataclass(init=False)
class JournalMetadata:
    file_path: str
    data: dict = field(init=False)
    location_address: dict = field(init=False)
    datetime_str: str = field(init=False)
    location_gps: dict = field(init=False)
    device_info: dict = field(init=False)
    street: str = field(init=False)
    zip_code: str = field(init=False)
    city: str = field(init=False)
    state: str = field(init=False)
    region: str = field(init=False)
    address_line: str = field(init=False)
    date_obj: datetime = field(init=False)
    short_date: str = field(init=False)
    long_date: str = field(init=False)
    google_maps_link: str = field(init=False)
    markdown_address_link: str = field(init=False)
    lat: float = field(init=False)
    lon: float = field(init=False)
    alt: float = field(init=False)
    gps_link: str = field(init=False)
    markdown_gps_link: str = field(init=False)

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(self.file_path, 'r') as file:
            try:
                self.data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from {self.file_path}: {e}")
            
            # Extract top-level keys
            self.location_address = self.data.get("location_address", {})
            self.datetime_str = self.data.get("datetime", "")
            self.location_gps = self.data.get("location_gps", {})
            self.device_info = self.data.get("device_info", {})

            self.street = get_non_empty_value('street', self.location_address)
            self.zip_code = get_non_empty_value('zip_code', self.location_address)
            self.city = get_non_empty_value('city', self.location_address)
            self.state = get_non_empty_value('state', self.location_address)
            self.region = get_non_empty_value('region', self.location_address)

            address_parts = [self.street, self.zip_code, self.city, self.state, self.region]
            self.address_line = ', '.join(part for part in address_parts if part)
            
            self.date_obj = datetime.fromisoformat(self.datetime_str)

            self.short_date = self.date_obj.strftime("%y%m%d-%H%M")
            self.long_date = self.date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
            self.google_maps_link = f"https://www.google.com/maps/search/?api=1&query={self.address_line.replace(' ', '+')}"
            self.markdown_address_link = f"[{self.address_line}]({self.google_maps_link})"

            self.lat = self.location_gps.get("latitude", 0)
            self.lon = self.location_gps.get("longitude", 0)
            self.alt = self.location_gps.get("altitude", 0)
            self.gps_link = f"https://www.google.com/maps?q={self.lat},{self.lon}"
            self.markdown_gps_link = f"[{self.lat}, {self.lon}, {self.alt}]({self.gps_link})"
            