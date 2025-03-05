# %%
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.journal_metadata import JournalMetadata
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Print the environment variable OPENAPI_KEY and exit
openapi_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# %%
cloud_path = "/Users/leo/Library/Mobile Documents/com~apple~CloudDocs/"
voice_memo_path = "VoiceMemo/Journal/"
cloud_memo_path = os.path.join(cloud_path, voice_memo_path)

# List all directories in the cloud path
new_dirs = [d for d in os.listdir(cloud_memo_path) if os.path.isdir(os.path.join(cloud_memo_path, d))]

for new_dir in new_dirs:
    memos = [file.stem for file in Path(cloud_memo_path, new_dir).glob("*.json")]
    print(f"Memos in {new_dir}: {memos}")
    for memo in memos:
        json_file_path = os.path.join(cloud_memo_path, new_dir, memo + ".json")
        meta_data = JournalMetadata(json_file_path)
        print(f"Address: {meta_data.get_address_line()}")
        print(f"Date: {meta_data.get_short_date()}")
        print(f"GPS: {meta_data.get_gps_link()}")
        print(f"Device: {meta_data.get_device_info()}")
        m4a_file_path = os.path.join(cloud_memo_path, new_dir, memo + ".m4a")
        print(f"Transcribing {m4a_file_path}")
        with open(m4a_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            print(transcription)

# %%
