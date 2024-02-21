import os
import json
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# This is an example table query. All column selections can just be appended, separated by commas. (.eq is an optional path to return specific results)
# response = supabase.table('sermons').select("id").execute()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Read in transcriptions and load them into the DB by sermon ID
def read_files_from_directory(directory, table):
    sermon_transcript = ""
    for filename in os.listdir(directory):
        removed_txt = filename.replace(".txt", "")
        name = removed_txt.replace("compressed_", "")
        cleaned_name = name.replace("_", " ")
        print(name)
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                transcript = file.read()
                try:
                    data = supabase.table(table).insert({
                        "name": cleaned_name,
                        "type": 'theology',
                        "description": transcript,
                    }).execute()
                except Exception as e:
                    print(f"There was an error: {e}")
