from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print the environment variable OPENAPI_KEY and exit
openapi_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# %%
from datetime import datetime
cloud_path = "/Users/leo/Library/Mobile Documents/com~apple~CloudDocs/VoiceMemos/Journal/"
txt_files = [fn[:-4] for fn in os.listdir(cloud_path) if fn.endswith('.txt')]

m4a_files = [fn + '.m4a' for fn in txt_files]
txt_files = [fn + '.txt' for fn in txt_files]

# %%
for txt_file in txt_files:
    with open(os.path.join(cloud_path, txt_file), 'r') as file:
        lines = file.readlines()
        if len(lines) >= 4:
            # Read and parse the first line as a date in the format yyyymmdd_HHmmss
            date_line = lines[0].strip()
            try:
                date_obj = datetime.fromisoformat(date_line)
            except ValueError:
                raise ValueError(f"Invalid date format: {date_line}")
            short_date = date_obj.strftime("%y%m%d-%H%M")
            long_date = date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
            address_line = lines[1].strip()
            if address_line:
                address_line = address_line.replace(';', ' ')
                google_maps_link = f"https://www.google.com/maps/search/?api=1&query={address_line.replace(' ', '+')}"
                markdown_address_link = f"[{address_line}]({google_maps_link})"
            else:
                address_line = "Unbekannte Adresse"
            gps_line = lines[2].strip()
            if gps_line:
                try:
                    lat, lon, alt = map(float, gps_line.split(';'))
                    gps_link = f"https://www.google.com/maps?q={lat},{lon}"
                    markdown_gps_link = f"[{lat}, {lon}, {alt}]({gps_link})"
                    print(gps_link)
                except ValueError:
                    raise ValueError(f"Invalid GPS format: {gps_line}")
            else:
                gps_line = "Unbekannte GPS-Koordinaten"
            device_line = lines[3].strip()
            if device_line:
                device_info = device_line.replace(';', ' ')
            else:
                device_info = "Unbekanntes Gerät"
            template_path = "/Users/leo/Development/projects/luna/luna_chat/journal_template.md"
            with open(template_path, 'r') as template_file:
                journal_template = template_file.read()
                journal_template = journal_template.replace("{{short_date}}", short_date)
                journal_template = journal_template.replace("{{date}}", long_date)
                journal_template = journal_template.replace("{{address}}", markdown_address_link)
                journal_template = journal_template.replace("{{gps}}", markdown_gps_link)
                journal_template = journal_template.replace("{{device}}", device_info)
            output_path = os.path.join(cloud_path, txt_file.replace('.txt', '.md'))
            with open(output_path, 'w') as output_file:
                output_file.write(journal_template)

# %%

with open(WAVE_FILENAME, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

print(transcription.text)
# %%
