"""Provides functionality to extract and process metadate of voice memos.

This module provides functionality to extract and process metadata from a JSON
file containing journal entry details of voice memos. It focuses on handling various aspects of
the metadata, including location information, datetime values, device information,
and GPS coordinates.

Note:
    The module expects the input JSON file to have specific keys for each of the metadata
    sections. If the JSON content is improperly formatted or missing, a ValueError is raised.

"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(init=False)
class JournalMetadata:
    __file_path: Path = field(init=False)
    __data: dict = field(init=False)
    __location_address: dict = field(init=False)
    __datetime_str: str = field(init=False)
    __location_gps: dict = field(init=False)
    __device_info: dict = field(init=False)
    __device_name: str = field(init=False)
    __os: str = field(init=False)
    __system_version: str = field(init=False)
    __device_type: str = field(init=False)
    __device_info_line: str = field(init=False)
    __street: str = field(init=False)
    __zip_code: str = field(init=False)
    __city: str = field(init=False)
    __state: str = field(init=False)
    __region: str = field(init=False)
    __address_line: str = field(init=False)
    __date_obj: datetime = field(init=False)
    __date: str = field(init=False)
    __short_datetime: str = field(init=False)
    __long_datetime: str = field(init=False)
    __address_link: str = field(init=False)
    __lat: float = field(init=False)
    __lon: float = field(init=False)
    __alt: float = field(init=False)
    __gps_line: str = field(init=False)
    __gps_link: str = field(init=False)

    def __init__(self, file_path: Path) -> None:
        """Initialize the object by loading and parsing a JSON file from file_path to extract and format metadata from a journal voice memo."""
        self.__file_path = file_path
        with file_path.open() as file:
            try:
                self.__data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from {self.__file_path}: {e}")

            # Extract top-level keys
            self.__location_address = self.__data.get("location_address", {})
            self.__datetime_str = self.__data.get("datetime", "")
            self.__location_gps = self.__data.get("location_gps", {})
            self.__device_info = self.__data.get("device_info", {})
            self.__device_info_line = f"{self.__device_info.get('device_name', '')}, {self.__device_info.get('os', '')}, {self.__device_info.get('system_version', '')}, {self.__device_info.get('device_type', '')}"

            # Extract device info
            # In the constructor, extract each device_info property into its own private attribute.
            self.__device_name = self.__device_info.get("device_name", "")
            self.__os = self.__device_info.get("os", "")
            self.__system_version = self.__device_info.get("system_version", "")
            self.__device_type = self.__device_info.get("device_type", "")

            self.__street = self.__location_address.get("street", "")
            self.__zip_code = self.__location_address.get("zip_code", "")
            self.__city = self.__location_address.get("city", "")
            self.__state = self.__location_address.get("state", "")
            self.__region = self.__location_address.get("region", "")

            address_parts = [self.__street, self.__zip_code, self.__city, self.__state, self.__region]
            self.__address_line = ", ".join(part for part in address_parts if part)

            self.__date_obj = datetime.fromisoformat(self.__datetime_str)
            self.__date = self.__date_obj.strftime("%Y-%m-%d")
            self.__short_datetime = self.__date_obj.strftime("%Y-%m-%d %H:%M")
            self.__long_datetime = self.__date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
            self.__address_link = f"https://www.google.com/maps/search/?api=1&query={self.__address_line.replace(' ', '+')}"

            self.__lat = self.__location_gps.get("latitude", 0)
            self.__lon = self.__location_gps.get("longitude", 0)
            self.__alt = self.__location_gps.get("altitude", 0)
            self.__gps_line = f"{self.__lat},{self.__lon},{self.__alt}"
            self.__gps_link = f"https://www.google.com/maps?q={self.__lat},{self.__lon}"

    def get_file_path(self) -> str:
        return self.__file_path

    def get_data(self) -> dict:
        return self.__data

    def get_device_name(self) -> str:
        return self.__device_name

    def get_os(self) -> str:
        return self.__os

    def get_system_version(self) -> str:
        return self.__system_version

    def get_device_type(self) -> str:
        return self.__device_type

    def get_device_info_line(self) -> str:
        return self.__device_info_line

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

    def get_date(self) -> str:
        return self.__date

    def get_short_datetime(self) -> str:
        return self.__short_datetime

    def get_long_datetime(self) -> str:
        return self.__long_datetime

    def get_address_link(self) -> str:
        return self.__address_link

    def get_lat(self) -> float:
        return self.__lat

    def get_lon(self) -> float:
        return self.__lon

    def get_alt(self) -> float:
        return self.__alt

    def get_gps_line(self) -> str:
        return self.__gps_line

    def get_gps_link(self) -> str:
        return self.__gps_link
