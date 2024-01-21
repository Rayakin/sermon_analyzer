import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# new_user = supabase.auth.sign_up({ "email": 'david@triplane.digital', "password": 'simfod-8xypju-Qahrun' })

user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": 'simfod-8xypju-Qahrun' })

# response = supabase.table('sermons').select("*").execute()

def insert_sermon_metadata(sermon_metadata_object):
    try:
        data = supabase.table("sermons").insert({
            "id":sermon_metadata_object['trackId'],
            "title":sermon_metadata_object['trackName'],
            "time_length":sermon_metadata_object['trackTimeMillis'],
            "speaker":sermon_metadata_object['speaker'],
            "download_link":sermon_metadata_object['episodeUrl'],
            "releaseDate":sermon_metadata_object['releaseDate'],
            "description":sermon_metadata_object['description']
            }).execute()
        # Assert we pulled real data.
        assert len(data.data) > 0
    except Exception as e:
        print(f"There was an error trying to insert the sermon: {e}")
    