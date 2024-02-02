from test_embeddings import full_embedding, first_half_embedding, second_half_embeddings
import os
import json
import numpy as np
from itertools import islice
import tiktoken
from nltk.tokenize import sent_tokenize
from openai import OpenAI
from supabase import create_client, Client

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

def split_with_overlap(sentences, overlap_percentage=0.1):
    split_index = len(sentences) // 2
    overlap_count = int(len(sentences) * overlap_percentage)
    part1 = sentences[:split_index + overlap_count]
    part2 = sentences[split_index - overlap_count:]

    return part1, part2

def chunked_tokens(text, encoding_name, chunk_length):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    if len(tokens) > chunk_length:
        print("the text is large")
        text_sentences = sent_tokenize(text)
        chunks_iterator = split_with_overlap(text_sentences)
    else:
        chunks_iterator = [text]
    yield from chunks_iterator

def len_safe_get_embedding(text, average=True, max_tokens=EMBEDDING_CTX_LENGTH, encoding_name=EMBEDDING_ENCODING):
    chunk_embeddings = []
    chunk_lens = []
    for chunk in chunked_tokens(text, encoding_name=encoding_name, chunk_length=max_tokens):
        try:
            response = client.embeddings.create(
                input=chunk,
                model=EMBEDDING_MODEL
            )
            numerical_embedding = response.data[0].embedding
            chunk_embeddings.append(numerical_embedding)
            chunk_lens.append(len(chunk))
        except Exception as e:
            print(f"There was an error: ${e}")
    if average:
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings)  # normalizes length to 1
        chunk_embeddings = chunk_embeddings.tolist()
    return chunk_embeddings

transcripts_file = "theology_topics.json"

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
        
read_files_from_directory('transcripts/SPBC')