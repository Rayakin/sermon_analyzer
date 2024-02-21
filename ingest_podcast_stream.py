from create_org import create_org #Expects an Org Name 
from podcast_retrieval import build_sermon_metadata #expects a podcast ID and the number of sermons you want to retrieve 
from download_mp3 import download_mp3
from compress import compress_mp3 #expects a filename and a directory name where the file is located
from transcribe import get_transcript #expects a filepath and returns a transcript
from transcript_token_counter import count_tokens #expects a filepath and returns 0 if the token count is under embed limit and a number of how many chunks this document needs if it is over it
from embed import embed #expects a transcript and the number of chunks it should generate, that is the output of the count_tokens function
from pydub import AudioSegment
from supabase import create_client, Client
import os
from audio_utilities import get_mp3_length
from openai import OpenAI
client = OpenAI()
user_pw = os.environ.get("USER_PW")

EMBEDDING_MODEL = 'text-embedding-3-small'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

# Sign on with password:
user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": user_pw })

response = supabase.table('sermons').select('id', 'title', 'has_been_embedded').eq('org_id', '8dfac8d9bc29521e1e87a6c121d7a5c2').execute()
print(response.data)

orgs = [137254859, 266129847]

def ingest_podcast_stream(stream_id, numOfSermons):
    sermons, stream_name = build_sermon_metadata(stream_id, numOfSermons)
    print(sermons)
    orgId = create_org(stream_name, stream_id)
    for sermon in sermons:
        response = supabase.table('sermons').select("id", "has_been_transcribed", "has_been_embedded", "org_id").eq("id", sermon['id']).execute()
        sermon_db_status = response.data
        print(f"sermon_db_status: {sermon_db_status}")
        transcript = ''
        if sermon_db_status:
            if not sermon_db_status[0]['has_been_transcribed']:
                print('This sermon existed, but hasn\'t been transcribed...')
                dl_sermon_path = download_mp3(sermon)
                print(f"Download was succesful for {sermon['id']}")
                compressed_sermon_path = compress_mp3(dl_sermon_path)
                transcript = get_transcript(compressed_sermon_path)
                print(transcript)
                directory_path = os.path.join(f"transcripts/{stream_name}")
                os.makedirs(directory_path, exist_ok=True)
                output_file_path = os.path.join(directory_path, f"{sermon['id']}.txt")
                with open(output_file_path, 'w') as file:
                    file.write(transcript)
                data = supabase.table('sermons').update({
                    "transcription": transcript,
                    "has_been_transcribed": True
                }).eq("id", sermon["id"]).execute()
                print(f"Transcription was succesful for {sermon['id']}")
                try:
                    os.remove(dl_sermon_path)
                    os.remove(compressed_sermon_path)
                except Exception as e:
                    print(e)
            if not sermon_db_status[0]['has_been_embedded']:
                print('This sermon existed, but hasn\'t been embedded...')
                if len(transcript) == 0:
                    get_transcript_from_db = supabase.table('sermons').select("transcription").eq("id", sermon['id']).execute()
                    transcript = get_transcript_from_db.data[0]["transcription"]
                    chunk_count = count_tokens(transcript)
                    embedding = embed(transcript, chunk_count)
                    data = supabase.table('sermons').update({
                        "embedding":embedding,
                        "has_been_embedded": True
                    }).eq("id", sermon["id"]).execute()
                    print(f"Embedding was succesful for {sermon['id']}")
                else: 
                    chunk_count = count_tokens(transcript)
                    embedding = embed(transcript, chunk_count)
                    data = supabase.table('sermons').update({
                        "embedding":embedding,
                        "has_been_embedded": True
                    }).eq("id", sermon["id"]).execute()
                    print(f"Embedding was succesful for {sermon['id']}")
        else:
            dl_sermon_path = download_mp3(sermon)
            print(f"Download was succesful for {sermon['id']}")
            audio_length = get_mp3_length(dl_sermon_path)
            data = supabase.table('sermons').insert({
                "id":sermon['id'],
                "title":sermon['name'],
                "time_length":audio_length,
                "speaker":sermon['speaker'],
                "download_link":sermon['episodeUrl'],
                "releaseDate":sermon['releaseDate'],
                "description":sermon['description'],
                "org_id":orgId
            }).execute()
            compressed_sermon_path = compress_mp3(dl_sermon_path)
            transcript = get_transcript(compressed_sermon_path)
            directory_path = os.path.join(f"transcripts/{stream_name}")
            os.makedirs(directory_path, exist_ok=True)
            output_file_path = os.path.join(directory_path, f"{sermon['id']}.txt")
            with open(output_file_path, 'w') as file:
                file.write(transcript)
            data = supabase.table('sermons').update({
                "transcription":transcript,
                "has_been_transcribed": True
            }).eq("id", sermon["id"]).execute()
            print(f"Transcription was succesful for {sermon['id']}")
            if not len(transcript) == 0:
                chunk_count = count_tokens(transcript)
                embedding = embed(transcript, chunk_count)
                data = supabase.table('sermons').update({
                    "embedding":embedding,
                    "has_been_embedded": True
                }).eq("id", sermon["id"]).execute()
                print(f"Embedding was succesful for {sermon['id']}")
            try:
                os.remove(dl_sermon_path)
                os.remove(compressed_sermon_path)
            except Exception as e:
                print(e)
    return True


# run = ingest_podcast_stream(1417448020, 30)

for org in orgs:
    run = ingest_podcast_stream(org, 75)
    if run:
        print("Success!")