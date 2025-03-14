# %%
import os
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, Template
from openai import OpenAI
from utils.audio_enhancer import improve_audio
from utils.journal_metadata import JournalMetadata

# Load environment variables from .env file
load_dotenv()

cloud_memo_path = Path("/Users/leo/Library/Mobile Documents/com~apple~CloudDocs/") / "VoiceMemo/Journal/"
luna_repo_memo_path = Path("/Users/leo/Development/projects/luna_repo/") / "voicememo/journal/"

# Print the environment variable OPENAPI_KEY and exit
openapi_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def get_journal_dirs(main_dir: Path) -> list[Path]:
    return [p for p in main_dir.iterdir() if p.is_dir()]


def get_journal_entries(rec_dir: Path) -> list[str]:
    journal_entries = [audio_file.stem for audio_file in rec_dir.glob("*.m4a")]
    journal_entries.sort()
    return journal_entries


def get_journal_template() -> Template:
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    return env.get_template("journal_template.md.j2")


def enhance_voice_memo(rec_dir: Path, journal_entires: list[str], *, enforce: bool = False) -> None:
    for memo in journal_entires:
        m4a_file = rec_dir / f"{memo}.m4a"
        enhanced = rec_dir / f"{memo}.enhanced.mp3"
        if not enhanced.exists() or enforce:
            improve_audio(m4a_file)


def transcribe_enhanced_audio(rec_dir: Path, journal_entires: list[str], *, enforce: bool = False) -> None:
    for memo in journal_entires:
        enhanced = rec_dir / f"{memo}.enhanced.mp3"
        transcription_file = rec_dir / f"{memo}.txt"
        if not transcription_file.exists() or enforce:
            with enhanced.open("rb") as audio_file:
                transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            with transcription_file.open("w") as f:
                f.write(transcription.text)


def generate_markdown(journal_dir: Path, journal_entries: list[str], template: Template, *, enforce: bool = False) -> None:
    markdown_file = journal_dir / f"{dir_path.name}.md"
    rec_dir = journal_dir / "rec"
    entries = []
    if not markdown_file.exists() or enforce:
        for memo in journal_entries:
            transcription_file = rec_dir / f"{memo}.txt"
            meta_data_file = rec_dir / f"{memo}.json"
            metadata = JournalMetadata(meta_data_file)
            with transcription_file.open() as f:
                transcription = f.read()
            entries.append((metadata, transcription))
        rendered_markdown = template.render(entries=entries)
        markdown_file = dir_path / f"{dir_path.name}.md"
        markdown_file.write_text(rendered_markdown, encoding="utf-8")


# %%
journal_dirs = get_journal_dirs(cloud_memo_path)
template = get_journal_template()
for dir_path in journal_dirs:
    rec_dir = dir_path / "rec"
    journal_entries = get_journal_entries(rec_dir)
    enhance_voice_memo(rec_dir, journal_entries)
    transcribe_enhanced_audio(rec_dir, journal_entries)
    generate_markdown(dir_path, journal_entries, template, enforce=True)

# %%

system_prompt = """
You are a helpful assistant. Your task is to correct any spelling discrepancies in the transcribed text.
Make sure that the following names are spelled correctly: Danielle, Mayla, Elina, Leo, Adnovum. Only
correct obvious grammatical errors and spelling mistakes. If there is redundancy, remove it. Add
necessary punctuation such as periods, commas, and capitalization, and use only the context provided and
change as little as necessary but as much as needed to make the text correct.
"""


def generate_corrected_transcript(rec_dir: Path, journal_entries: list[str], system_prompt: str) -> None:
    for memo in journal_entries:
        transcription_file = rec_dir / f"{memo}.txt"
        transcription_file_enhanced = rec_dir / f"{memo}.enhanced.txt"
        with transcription_file.open() as f:
            transcription = f.read()
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=1.0,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": transcription}],
        )
        with transcription_file_enhanced.open("w") as f:
            f.write(response.choices[0].message["content"])


journal_dirs = get_journal_dirs(cloud_memo_path)
for dir_path in journal_dirs:
    rec_dir = dir_path / "rec"
    journal_entries = get_journal_entries(rec_dir)
    generate_corrected_transcript(rec_dir, journal_entries, system_prompt)

# %%
