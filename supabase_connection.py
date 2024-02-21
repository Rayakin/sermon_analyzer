import os
import json
from supabase import create_client, Client

user_pw = os.environ.get("USER_PW")
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

# Create a new user:
# new_user = supabase.auth.sign_up({ "email": 'david@triplane.digital', "password": 'simfod-8xypju-Qahrun' })

# Sign on with password:
user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": user_pw })

# This is an example table query. All column selections can just be appended, separated by commas. (.eq is an optional path to return specific results)
response = supabase.table('sermons').select("id", "download_link").eq("id", 1000591927285).execute()


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Takes a sermon object and does the OG insert to the Sermons table:
def insert_sermon_metadata(sermon_metadata_object):
    try:
        data = supabase.table("sermons").insert({
            "id":sermon_metadata_object['trackId'],
            "title":sermon_metadata_object['trackName'],
            "time_length":sermon_metadata_object['trackTimeMillis'],
            "speaker":sermon_metadata_object['speaker'],
            "download_link":sermon_metadata_object['episodeUrl'],
            "releaseDate":sermon_metadata_object['releaseDate'],
            "description":sermon_metadata_object['description'],
            "orgId":"3ca000daf5212a4908bc4aa57205162b"
        }).execute()
        # Assert we pulled real data.
        assert len(data.data) > 0
    except Exception as e:
        print(f"There was an error trying to insert the sermon: {e}")
    

# Read in transcriptions and load them into the DB by sermon ID
def read_files_from_directory(directory):
    sermon_transcript = ""
    for filename in os.listdir(directory):
        name = filename.replace(".txt", "")
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                sermon_transcript = file.read()
                try:
                    data = supabase.table("sermons").update({"transcription": sermon_transcript}).eq("id", int(name)).execute()
                except Exception as e:
                    print(f"There was an error: {e}")

# Main function to process the JSON data for embeddings done locally
def process_json_data(file_path):
    data = load_json(file_path)
    try:
        for sermon in data:
            id = sermon.get('id', 'No ID')
            embedding = sermon.get('embedding', 'No Embedding')
            name = id.replace(".txt", "")
            # Load embeddings
            # data = supabase.table("sermons").update({"embedding": embedding}).eq("id", int(name)).execute()
            data = supabase.table("sermons").update({"has_been_transcribed": True}).eq("id", int(name)).execute()
            data = supabase.table("sermons").update({"has_been_embedded": True}).eq("id", int(name)).execute()
    except Exception as e:
        print(f"There was an error: {e}")

