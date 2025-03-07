from luna_chat.voice_memo.utils.journal_metadata import JournalMetadata
from tests.test_utils.data_util import get_data_dir


def test_journal_metadata_valid() -> None:
    # Construct the path to the correct JSON file relative to this test file.
    json_path = get_data_dir() / "journal_metadata/meta_data_correct.json"

    # Create an instance of JournalMetadata
    jm = JournalMetadata(json_path)

    # Check the location address data.
    assert jm.state == "Florida"
    assert jm.street == "6802 Gulf Drs"
    assert jm.zip_code == "34217"
    assert jm.city == "Anna Maria Island"
    assert jm.region == "United States"

    expected_address_line = "6802 Gulf Drs, 34217, Anna Maria Island, Florida, United States"
    assert jm.address_line == expected_address_line

    # Validate date formatting.
    assert jm.date == "2025-03-05"
    assert jm.short_datetime == "2025-03-05 10:28"
    assert jm.long_datetime == "2025-03-05 10:28:52 UTC+01:00"

    # Verify that the google maps link is set.
    assert "google.com/maps/search" in jm.address_link

    # For location_gps, note that the JSON uses key "lattitude" while the code expects "latitude"
    # Therefore, latitude will default to 0.
    assert jm.lat == 27.514386217778767
    assert jm.lon == -82.7227514245628554
    assert jm.alt == 10
