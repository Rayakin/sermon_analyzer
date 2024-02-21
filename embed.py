from test_embeddings import full_embedding, first_half_embedding, second_half_embeddings
import math
import os
import json
import numpy as np
from itertools import islice
import tiktoken
from nltk.tokenize import sent_tokenize, word_tokenize
from openai import OpenAI
from supabase import create_client, Client
from transcript_token_counter import count_tokens #expects a filepath and returns True if the token count is under embed limit and False if it is over it

user_pw = os.environ.get("USER_PW")

client = OpenAI()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

EMBEDDING_MODEL = 'text-embedding-3-small'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'

# Sign on with password:
user = supabase.auth.sign_in_with_password({ "email": 'david@triplane.digital', "password": user_pw })

transcripts = []

def read_files_from_directory(directory):
    sermon_transcript = ""
    for filename in os.listdir(directory):
        removed_txt = filename.replace(".txt", "")
        name = removed_txt.replace("compressed_", "")
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                sermon_transcript = file.read()
                try:
                    embedding = len_safe_get_embedding(sermon_transcript)
                    print(f"{name}: {embedding}")
                    # data = supabase.table("sermons").update({"has_been_embedded": True}).eq("id", int(name)).execute()
                    # data = supabase.table("sermons").update({"has_been_transcribed": True}).eq("id", int(name)).execute()
                    data = supabase.table("sermons").update({"embedding": embedding}).eq("id", int(name)).execute()
                except Exception as e:
                    print(f"There was an error: {e}")

def embed(text, chunk_count):
    print(f"This is the chunk count... {chunk_count}")
    if chunk_count:
        chunk_embeddings = []
        chunk_lens = []
        for chunk in chunked_tokens(text, chunk_count):
            try:
                response = client.embeddings.create(
                    input=chunk,
                    model=EMBEDDING_MODEL
                )
                embedding = response.data[0].embedding
                chunk_embeddings.append(embedding)
                chunk_lens.append(len(chunk.split()))  # Use number of words as weight
            except Exception as e:
                print(f"There was an error: {e}")
        print(len(chunk_embeddings))
        # Compute weighted average of embeddings
        total_len = sum(chunk_lens)
        weights = [length / total_len for length in chunk_lens]
        averaged_embedding = np.average(chunk_embeddings, axis=0, weights=weights)
        normalized_embedding = averaged_embedding / np.linalg.norm(averaged_embedding)
        return normalized_embedding.tolist()
    else:
        try:
            response = client.embeddings.create(
                input=text,
                model=EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"There was an error: {e}")

def read_transcripts_from_db(orgId):
    sermon_transcript = supabase.table('sermons').select("id", "transcription").eq("orgId", orgId).execute()
    sermons = sermon_transcript.data
    for transcript in sermons:
        try:
            embedding = len_safe_get_embedding(transcript["transcription"])
            print(f"{transcript['id']}: {embedding}")
            data = supabase.table("sermons").update({"embedding": embedding}).eq("id", transcript["id"]).execute()
        except Exception as e:
            print(f"There was an error: {e}")

def read_topics_from_db(table):
    topic_descriptions = supabase.table(table).select("id", "name", "description").execute()
    topics = topic_descriptions.data
    for topic in topics:
        try:
            embedding = len_safe_get_embedding(topic["description"])
            print(f"{topic['name']}: {embedding}")
            data = supabase.table(table).update({"embedding": embedding}).eq("id", topic["id"]).execute()
        except Exception as e:
            print(f"There was an error: {e}")

def chunked_tokens(text, count_chunks, overlap_percentage=0.1):
    words = word_tokenize(text)
    total_words = len(words)
    print(count_chunks)
    print(total_words)
    chunk_size = math.ceil(total_words / count_chunks)
    print(f"This is the chunk size expectation: {chunk_size}")
    overlap_size = int(chunk_size * overlap_percentage)

    chunks = []
    for i in range(count_chunks):
        # Calculate start index for each chunk
        start = i * chunk_size
        if i > 0:
            start -= overlap_size  # Apply overlap by stepping back

        # Calculate end index for each chunk
        end = start + chunk_size + overlap_size if i < count_chunks - 1 else total_words

        # Ensure we don't start with a negative index
        start = max(0, start)

        # Join words to form the chunk
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)

    # Debugging prints to check chunk sizes and content
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} length (in characters): {len(chunk)}")
    print(f"Total chunks: {len(chunks)}")

    return chunks



# transcripts_file = "theology_topics.json"

def embed_all_transcripts(transcripts):
    for transcript in transcripts:
        try: 
            embedding = len_safe_get_embedding(transcript['text'])
            transcript['embedding'] = embedding
        except Exception as e:
            transcript['embedding'] = "error"
            print(f"Transcript {transcript['id']} had this error: {e}")
    with open(transcripts_file, 'w') as file:
        json.dump(transcripts, file, indent=4)
    print(transcripts)
        
# read_transcripts_from_db("8dfac8d9bc29521e1e87a6c121d7a5c2")
# read_topics_from_db('topics')