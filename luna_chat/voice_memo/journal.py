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
luna_repo_path = "/Users/leo/Development/projects/luna_repo/"
luna_repo_memo_path = os.path.join(luna_repo_path, voice_memo_path.lower())

# List all directories in the cloud path
new_dirs = [d for d in os.listdir(cloud_memo_path) if os.path.isdir(os.path.join(cloud_memo_path, d))]

# iterate through directories
for new_dir in new_dirs:
    rec_dir = Path(cloud_memo_path, new_dir, "rec")
    memo_files = list(rec_dir.glob("*.json"))
    memos = [m.stem for m in memo_files]

    print(f"Memos in {new_dir}: {memos}")

    for memo in memos:
        json_file = rec_dir / f"{memo}.json"
        metadata = JournalMetadata(json_file)
        print(f"Address: {metadata.get_address_line()}")
        print(f"Date: {metadata.get_short_date()}")
        print(f"GPS: {metadata.get_gps_link()}")
        print(f"Device: {metadata.get_device_info()}")

        m4a_file = rec_dir / f"{memo}.m4a"
        print(f"Transcribing {m4a_file}")
        with m4a_file.open('rb') as audio_file:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            print(transcription)

# %%
