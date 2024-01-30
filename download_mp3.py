import os
import requests

# Expects an array of objects from the supabase DB for a given sermon.
def download_mp3(sermon):
    download_link = sermon['episodeUrl']
    id = sermon['trackId']
    try:
        response = requests.get(download_link, stream=True)
        if response.status_code == 200:
            file_path = os.path.join("mp3s", f"{id}.mp3")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {id} from {download_link}")
        else:
            print(f"Failed to download {download_link} - HTTP status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {download_link}: {e}")