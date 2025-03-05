import unittest
import tempfile
import os
import json
from datetime import datetime
from luna_chat.voice_memo.utils import journal_metadata

class TestJournalMetadataInit(unittest.TestCase):
    
    def test_init_valid_file(self):
        # Prepare valid JSON data for testing.
        data = {
            "location_address": {"street": "123 Main St", "city": "New York"},
            "datetime": "2023-10-10T10:10:10",
            "location_gps": {"lattitude": 40.7128, "longitude": -74.0060, "altitude": 10},
            "device_info": {"model": "iPhone"}
        }
        # Create temporary file with valid JSON content.
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
            json.dump(data, tmp_file)
            tmp_file.flush()
            tmp_path = tmp_file.name
        try:
            # Instantiate JournalMetadata with the temporary file.
            jm = journal_metadata.JournalMetadata(tmp_path)
            # Validate the loaded JSON data.
            self.assertEqual(jm.data, data)
            self.assertEqual(jm.get_location_address(), data["location_address"])
            self.assertEqual(jm.get_datetime(), data["datetime"])
            self.assertEqual(jm.get_location_gps(), data["location_gps"])
            self.assertEqual(jm.get_device_info(), data["device_info"])
        finally:
            os.remove(tmp_path)

    def test_init_invalid_json(self):
        # Create temporary file with invalid JSON content.
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
            tmp_file.write("this is not a valid json")
            tmp_file.flush()
            tmp_path = tmp_file.name
        try:
            # Expect ValueError due to JSON decoding error.
            with self.assertRaises(ValueError):
                journal_metadata.JournalMetadata(tmp_path)
        finally:
            os.remove(tmp_path)

if __name__ == '__main__':
    unittest.main()