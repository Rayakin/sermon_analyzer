import tiktoken
import os
import math

def count_tokens(text):
    print(f"This is the text count_tokens was given: {text}")
    encoding = tiktoken.get_encoding('cl100k_base')
    tokens = encoding.encode(text)
    if len(tokens) > 8191:
        length = math.ceil(len(tokens) / 8191)
        print(length)
        print(f"{len(tokens)} is too large")
        return length 
    else: 
        print(f"{len(tokens)} is under the token limit")
        return 0