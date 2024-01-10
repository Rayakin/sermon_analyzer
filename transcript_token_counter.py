import tiktoken
import os

EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'

def count_tokens(encoding_name, chunk_length, directory="transcripts2"):
    text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                text = file.read()
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(text)
        if len(tokens) > chunk_length:
            print(f"{filename}: {len(tokens)} is too large")
        else: 
            print(f"{filename}: {len(tokens)} is under the token limit")

count_tokens(EMBEDDING_ENCODING, EMBEDDING_CTX_LENGTH)