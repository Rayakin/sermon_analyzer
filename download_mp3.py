import os
from pydub import AudioSegment
import requests

def download_mp3(sermon):
    download_link = sermon['episodeUrl']
    sermon_id = sermon['id']  # Renamed variable to avoid shadowing the built-in 'id'
    try:
        response = requests.get(download_link, stream=True)
        if response.status_code == 200:
            file_path = os.path.join("mp3s", f"{sermon_id}.mp3")
            # First, save the downloaded file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
            # Note: This step is only necessary if you want to change the file in some way (e.g., adjust bitrate)
            audio = AudioSegment.from_file(file_path)
            audio.export(file_path, format="mp3", bitrate="64k")  # Ensure bitrate is a string
            return file_path
        else:
            print(f"Failed to download {download_link} - HTTP status code {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while downloading {download_link}: {e}")
        return False