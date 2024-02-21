import os
from embed import embed
from supabase import create_client, Client

user_pw = os.environ.get("USER_PW")
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

# Sign on with password:
user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": user_pw })

# This is an example table query. All column selections can just be appended, separated by commas. (.eq is an optional path to return specific results)
response = supabase.table('sermons').select("id", "download_link").eq("id", 1000591927285).execute()

def upload_topic(name, text):
    response = supabase.table('topics').select("id", "download_link").eq("id", 1000591927285).execute()
    try:
        print('This needs to be built out in order to help upload new topics.')
    except Exception as e:
        print(e)

for filename in os.listdir(directory):
    if not filename.startswith("compressed_"):
        continue
    if not filename.endswith(".mp3"):
        continue