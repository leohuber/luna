# %%
from openai import OpenAI
import os
from dotenv import load_dotenv
from utils.journal_metadata import JournalMetadata
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from utils.audio_enhancer import improve_audio

# Load environment variables from .env file
load_dotenv()

# Print the environment variable OPENAPI_KEY and exit
openapi_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# %%
cloud_memo_path = Path("/Users/leo/Library/Mobile Documents/com~apple~CloudDocs/") / "VoiceMemo/Journal/"
luna_repo_memo_path = Path("/Users/leo/Development/projects/luna_repo/") / "voicememo/journal/"

# Set up Jinja2 environment once
template_dir = Path(__file__).parent
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("journal_template.md.j2")

# Iterate through each directory in the cloud memo path
for dir_path in (p for p in cloud_memo_path.iterdir() if p.is_dir()):
    rec_dir = dir_path / "rec"
    memo_json_files = list(rec_dir.glob("*.json"))
    memos = [js.stem for js in memo_json_files]
    memos.sort()

    last_transcription = None
    last_metadata = None

    entries = []
    for memo in memos:
        json_file = rec_dir / f"{memo}.json"
        metadata = JournalMetadata(json_file)
        m4a_file = rec_dir / f"{memo}.m4a"
        enhanced = improve_audio(m4a_file)
        with enhanced.open("rb") as audio_file:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        entries.append((metadata, transcription.text))

    # Render template with the metadata and transcription result
    rendered_markdown = template.render(entries=entries)
    markdown_file = dir_path / f"{dir_path.name}.md"
    markdown_file.write_text(rendered_markdown, encoding="utf-8")

    # %%
