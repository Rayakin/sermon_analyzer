import os
from nltk.tokenize import sent_tokenize

def read_files_from_directory(directory):
    sentences = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming the sermon files are text files
            with open(os.path.join(directory, filename), 'r') as file:
                sentences = sent_tokenize(file.read())
                print(f"{filename}: {len(sentences)}")
# Usage
directory = "transcripts2"
read_files_from_directory(directory)