import requests
import os
import re
from datetime import datetime
from compress import compress_all_mp3_in_directory
from transcribe import get_all_transcripts_in_directory
from get_existing_trackIds import get_existing_trackIds

sermons_meta_data = []
sermon_volume = 60

def extract_podcast_url(podcast_id):
    try:
        itunes_response = requests.get(f"https://itunes.apple.com/lookup?id={podcast_id}&media=podcast&entity=podcastEpisode&limit={sermon_volume}")
        if itunes_response.status_code == 200:
            data = itunes_response.json()
            return(data['results'])
    except Exception as e:
        print(f"An error occurred: {e}")

sermons = extract_podcast_url('1244778987')

def download_mp3(download_url, sermon_title, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(download_dir, f"{sermon_title}.mp3")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {sermon_title}")
        else:
            print(f"Failed to download {download_url} - HTTP status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {download_url}: {e}")

download_dir = "mp3s"

retrieved_trackIds = get_existing_trackIds("mp3s")
for sermon in sermons:
    meta_data = {}
    sermon_release_date = datetime.fromisoformat(sermon['releaseDate'].rstrip('Z')).date()
    if str(sermon['trackId']) in retrieved_trackIds:
        print('Already got this one')
        continue
    if sermon['wrapperType'] != 'track' and sermon_release_date > datetime(2022, 12, 31).date():
        match = re.search(r"Speaker:\s*([A-Za-z]+(?:\s[A-Za-z]+)*)", sermon['description'])
        if match:
            speaker = match.group(1)
        else:
            speaker = "Unknown"
        meta_data['trackId'] = sermon['trackId']
        meta_data['trackName'] = sermon['trackName']
        meta_data['trackViewUrl'] = sermon['trackViewUrl']
        meta_data['trackTimeMillis'] = sermon['trackTimeMillis']
        meta_data['description'] = sermon['description']
        meta_data['releaseDate'] = sermon['releaseDate']
        meta_data['episodeUrl'] = sermon['episodeUrl']
        meta_data['speaker'] = speaker 
        sermons_meta_data.append(meta_data)
        download_mp3(meta_data['episodeUrl'], f"{meta_data['trackId']}--{meta_data['trackName']}", download_dir)

compress_all_mp3_in_directory(download_dir)
get_all_transcripts_in_directory(download_dir)

print(sermons_meta_data)