from test_embeddings import full_embedding, first_half_embedding, second_half_embeddings
import os
import numpy as np
from itertools import islice
import tiktoken
from nltk.tokenize import sent_tokenize
from openai import OpenAI
client = OpenAI()

EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'

text = ""

with open(os.path.join('transcripts2', '1000609181862.txt'), 'r') as file:
    text += file.read()

def mag(arr):
   v = np.array(arr)
   return np.linalg.norm(v)
def print_vector(msg, arr):
    v = np.array(arr)
    print(msg)
    print(np.linalg.norm(v))
    print(v)
    print("\n")
def unit_vector(arr):
    v = np.array(arr)
    #print("unit_vector")
    #print(v)
    mag = np.linalg.norm(v)
    #print(mag)
    uv = v / mag
    #print(uv)
    return uv.tolist()

def dot(arr1, arr2):
    v1 = np.array(arr1)
    v2 = np.array(arr2)

    #print("v1")
    #print(v1)
    #print("\nv2")
    #print(v2)
    #print(v1.tolist()[0], arr1[0])

    return np.dot(v1,v2)

def combine(em1, em2):
#   em1 = unit_vector(em1)
#   em2 = unit_vector(em2)

   l = len(em1)
   c = [0] * l

   for i in range(l):
      c[i] = em1[i] + em2[i]

   c = unit_vector(c)
   return c

em0 = combine(first_half_embedding,second_half_embeddings)
print_vector("em0 (combined)", em0)

dp = dot(em0, full_embedding)

print("\nDot")
print(dp)


def split_with_overlap(sentences, overlap_percentage=0.1):
    # Calculate the splitting index
    split_index = len(sentences) // 2

    # Calculate the number of sentences for overlap
    overlap_count = int(len(sentences) * overlap_percentage)

    # Create two parts with overlap
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

averaged_output = len_safe_get_embedding(text)
print(f"Averaged Output: {averaged_output}")