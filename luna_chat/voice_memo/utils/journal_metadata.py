import json
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime

# Extract address information
def get_non_empty_value(key: str, dictionary: dict, default='') -> Any:
    value = dictionary.get(key, default)
    return value if value else default

@dataclass(init=False)
class JournalMetadata:
    __file_path: str
    __data: dict = field(init=False)
    __location_address: dict = field(init=False)
    __datetime_str: str = field(init=False)
    __location_gps: dict = field(init=False)
    __device_info: dict = field(init=False)
    __street: str = field(init=False)
    __zip_code: str = field(init=False)
    __city: str = field(init=False)
    __state: str = field(init=False)
    __region: str = field(init=False)
    __address_line: str = field(init=False)
    __date_obj: datetime = field(init=False)
    __short_date: str = field(init=False)
    __long_date: str = field(init=False)
    __google_maps_link: str = field(init=False)
    __markdown_address_link: str = field(init=False)
    __lat: float = field(init=False)
    __lon: float = field(init=False)
    __alt: float = field(init=False)
    __gps_link: str = field(init=False)
    __markdown_gps_link: str = field(init=False)

    def __init__(self, file_path: str):
        self.__file_path = file_path
        with open(self.__file_path, 'r') as file:
            try:
                self.__data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from {self.__file_path}: {e}")
            
            # Extract top-level keys
            self.__location_address = self.__data.get("location_address", {})
            self.__datetime_str = self.__data.get("datetime", "")
            self.__location_gps = self.__data.get("location_gps", {})
            self.__device_info = self.__data.get("device_info", {})

            self.__street = self.__location_address.get('street', '')
            self.__zip_code = self.__location_address.get('zip_code', '')
            self.__city = self.__location_address.get('city', '')
            self.__state = self.__location_address.get('state', '')
            self.__region = self.__location_address.get('region', '')

            address_parts = [self.__street, self.__zip_code, self.__city, self.__state, self.__region]
            self.__address_line = ', '.join(part for part in address_parts if part)
            
            self.__date_obj = datetime.fromisoformat(self.__datetime_str)

            self.__short_date = self.__date_obj.strftime("%y%m%d-%H%M")
            self.__long_date = self.__date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
            self.__google_maps_link = f"https://www.google.com/maps/search/?api=1&query={self.__address_line.replace(' ', '+')}"
            self.__markdown_address_link = f"[{self.__address_line}]({self.__google_maps_link})"

            self.__lat = self.__location_gps.get("latitude", 0)
            self.__lon = self.__location_gps.get("longitude", 0)
            self.__alt = self.__location_gps.get("altitude", 0)
            self.__gps_link = f"https://www.google.com/maps?q={self.__lat},{self.__lon}"
            self.__markdown_gps_link = f"[{self.__lat}, {self.__lon}, {self.__alt}]({self.__gps_link})"

    def get_file_path(self) -> str:
        return self.__file_path

    def get_data(self) -> dict:
        return self.__data

    def get_location_address(self) -> dict:
        return self.__location_address

    def get_datetime_str(self) -> str:
        return self.__datetime_str

    def get_location_gps(self) -> dict:
        return self.__location_gps

    def get_device_info(self) -> dict:
        return self.__device_info

    def get_street(self) -> str:
        return self.__street

    def get_zip_code(self) -> str:
        return self.__zip_code

    def get_city(self) -> str:
        return self.__city

    def get_state(self) -> str:
        return self.__state

    def get_region(self) -> str:
        return self.__region

    def get_address_line(self) -> str:
        return self.__address_line

    def get_date_obj(self) -> datetime:
        return self.__date_obj

    def get_short_date(self) -> str:
        return self.__short_date

    def get_long_date(self) -> str:
        return self.__long_date

    def get_google_maps_link(self) -> str:
        return self.__google_maps_link

    def get_markdown_address_link(self) -> str:
        return self.__markdown_address_link

    def get_lat(self) -> float:
        return self.__lat

    def get_lon(self) -> float:
        return self.__lon

    def get_alt(self) -> float:
        return self.__alt

    def get_gps_link(self) -> str:
        return self.__gps_link

    def get_markdown_gps_link(self) -> str:
        return self.__markdown_gps_link