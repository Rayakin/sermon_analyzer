import requests
import os
import re
from datetime import datetime
from supabase_connection import insert_sermon_metadata
from supabase import create_client, Client
from download_mp3 import download_mp3
user_pw = os.environ.get("USER_PW")
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# This function retrieves metadata for a list of sermons/podcasts from the itunes api.
def extract_podcast_url(podcast_id, sermon_volume):
    try:
        itunes_response = requests.get(f"https://itunes.apple.com/lookup?id={podcast_id}&media=podcast&entity=podcastEpisode&limit={sermon_volume}")
        if itunes_response.status_code == 200:
            data = itunes_response.json()
            return (data['results'])
    except Exception as e:
        print(f"An error occurred: {e}")

# retrieved_trackIds = get_existing_trackIds("mp3s")
user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": user_pw })
def build_sermon_metadata(podcast_id, sermon_volume):
    sermons = extract_podcast_url(podcast_id, sermon_volume)
    sermons_meta_data = []
    stream_name = sermons[0]['collectionName']
    for sermon in sermons:
        meta_data = {}
        sermon_release_date = datetime.fromisoformat(sermon['releaseDate'].rstrip('Z')).date()
        if sermon['wrapperType'] != 'track' and sermon_release_date > datetime(2022, 12, 31).date():
            match = re.search(r"([s|S]peaker|[p|P]reacher|[t|T]eacher|[p|P]astor):\s*([A-Za-z]+(?:\s[A-Za-z]+)*)", sermon['description'])
            if match:
                speaker = match.group(1)
            else:
                speaker = "Unknown"
            meta_data['id'] = sermon['trackId']
            meta_data['name'] = sermon['trackName']
            meta_data['trackViewUrl'] = sermon['trackViewUrl']
            meta_data['description'] = sermon['description']
            meta_data['releaseDate'] = sermon['releaseDate']
            meta_data['episodeUrl'] = sermon['episodeUrl']
            if speaker:
                meta_data['speaker'] = speaker
            else: 
                meta_data['speaker'] = "Null"
            sermons_meta_data.append(meta_data)
    return sermons_meta_data, stream_name