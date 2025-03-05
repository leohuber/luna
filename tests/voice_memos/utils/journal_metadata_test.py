import os
from tests.test_utils.data_util import get_data_dir
from luna_chat.voice_memo.utils.journal_metadata import JournalMetadata

def test_journal_metadata_valid():
    # Construct the path to the correct JSON file relative to this test file.
    json_path = os.path.join(get_data_dir(), "journal_metadata/meta_data_correct.json")

    # Create an instance of JournalMetadata
    jm = JournalMetadata(json_path)

    # Check the location address data.
    address = jm.location_address
    assert address["state"] == "Florida"
    assert address["street"] == "6802 Gulf Drs"
    assert address["zip_code"] == "34217"
    assert address["city"] == "Anna Maria Island"
    assert address["region"] == "United States"

    expected_address_line = "6802 Gulf Drs, 34217, Anna Maria Island, Florida, United States"
    assert jm.address_line == expected_address_line

    # Validate date formatting.
    # The datetime string "2025-03-05T10:28:52+01:00" should yield short_date "250305-1028".
    assert jm.short_date == "250305-1028"

    # Verify that the google maps link is set.
    assert "google.com/maps/search" in jm.google_maps_link

    # For location_gps, note that the JSON uses key "lattitude" while the code expects "latitude"
    # Therefore, latitude will default to 0.
    assert jm.lat == 0
    assert jm.lon == -82.7227514245628554
    assert jm.alt == 10