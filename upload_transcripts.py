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

# Read in transcriptions and load them into the DB by sermon ID
def read_files_from_directory(directory):
    sermon_transcript = ""
    for filename in os.listdir(directory):
        removed_txt = filename.replace(".txt", "")
        name = removed_txt.replace("compressed_", "")
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                sermon_transcript = file.read()
                try:
                    data = supabase.table("sermons").update({"transcription": sermon_transcript}).eq("id", int(name)).execute()
                except Exception as e:
                    print(f"There was an error: {e}")

read_files_from_directory('transcripts/New')