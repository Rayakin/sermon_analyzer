import os
import json
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

# Sign on with password:
# user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": 'simfod-8xypju-Qahrun' })

# This is an example table query. All column selections can just be appended, separated by commas. (.eq is an optional path to return specific results)
# response = supabase.table('sermons').select("id").execute()


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Main function to process the JSON data for embeddings done locally
def process_json_data(file_path):
    data = load_json(file_path)
    try:
        for sermon in data:
            id = sermon.get('id', 'No ID')
            embedding = sermon.get('embedding', 'No Embedding')
            name = id.replace(".txt", "")
            # data = supabase.table("sermons").update({"embedding": embedding}).eq("id", int(name)).execute()
            data = supabase.table("sermons").update({"has_been_transcribed": True}).eq("id", int(name)).execute()
            data = supabase.table("sermons").update({"has_been_embedded": True}).eq("id", int(name)).execute()
    except Exception as e:
        print(f"There was an error: {e}")


read_files_from_directory('transcripts/New')