# %%
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Print the environment variable OPENAPI_KEY and exit
openapi_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# %%
cloud_path = "/Users/leo/Library/Mobile Documents/com~apple~CloudDocs/VoiceMemo/Journal/"

# List all directories in the cloud path
new_dirs = [d for d in os.listdir(cloud_path) if os.path.isdir(os.path.join(cloud_path, d))]

for new_dir in new_dirs:
    json_files = [f for f in os.listdir(os.path.join(cloud_path, new_dir)) if f.endswith('.json')]
    print(f"JSON files in {new_dir}: {json_files}")
    for json_file in json_files:
        with open(os.path.join(cloud_path, new_dir, json_file), 'r') as file:
            data = json.load(file)
            location_address = data.get("location_address", {})
            datetime_str = data.get("datetime", "")
            location_gps = data.get("location_gps", {})
            device_info = data.get("device_info", {})

            address_line = f"{location_address.get('street', '')}, {location_address.get('zip_code', '')} {location_address.get('city', '')}, {location_address.get('state', '')}, {location_address.get('region', '')}"
            date_obj = datetime.fromisoformat(datetime_str)
            short_date = date_obj.strftime("%y%m%d-%H%M")
            long_date = date_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={address_line.replace(' ', '+')}"
            markdown_address_link = f"[{address_line}]({google_maps_link})"

            lat = location_gps.get("lattitude", 0)
            lon = location_gps.get("longitude", 0)
            alt = location_gps.get("altitude", 0)
            gps_link = f"https://www.google.com/maps?q={lat},{lon}"
            markdown_gps_link = f"[{lat}, {lon}, {alt}]({gps_link})"

            device_info_str = f"{device_info.get('device_name', '')} {device_info.get('os', '')} {device_info.get('system_version', '')} {device_info.get('device_type', '')}"

            print(f"Address: {address_line}")
            print(f"Date: {long_date}")
            print(f"GPS: {markdown_gps_link}")
            print(f"Device: {device_info_str}")


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
