import json
import re
import os
from nltk.tokenize import sent_tokenize

def read_files_from_directory(directory):
    aggregated_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                aggregated_text += file.read() + " "
    return aggregated_text

text = read_files_from_directory("transcripts")

# Lists of books in the Old and New Testaments
old_testament_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", 
    "Joshua", "Judges", "Ruth", "first Samuel","1 Samuel", "second Samuel","2 Samuel", 
    "first Kings","1 Kings", "second Kings","2 Kings", "first Chronicles","1 Chronicles", "second Chronicles","2 Chronicles", 
    "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs", 
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", 
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", 
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", 
    "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

new_testament_books = [
    "Matthew", "Mark", "Luke", "John", "Acts", 
    "Romans", "First Corinthians", "1 Corinthians", "Second Corinthians", "2 Corinthians", "Galatians", 
    "Ephesians", "Philippians", "Colossians", "first Thessalonians", "1 Thessalonians", 
    "second Thessalonians", "2 Thessalonians", "first Timothy","1 Timothy", "second Timothy","2 Timothy", "Titus", 
    "Philemon", "Hebrews", "James", "first Peter", "1 Peter", "second Peter", "2 Peter",
    "first John","1 John", "second John","2 John", "third John","3 John", "Jude", "Revelation"
]

# Combine both lists
bible_books = old_testament_books + new_testament_books

# Function to check if a sentence contains a book of the Bible
def contains_bible_reference(sentence):
    for book in bible_books:
        if re.search(r'\b' + re.escape(book) + r'\b', sentence, re.IGNORECASE):
            return True
    return False

# Function to process transcripts
def process_transcripts(transcript):
    sentences = sent_tokenize(transcript)
    count = 0
    with open("processed_transcripts.jsonl", "w") as f:
        for sentence in sentences:
            count += 1
            if not count % 100:
                print(count)
            if contains_bible_reference(sentence):
                json_object = json.dumps({"source": sentence})
                f.write(json_object + '\n')
    print(f"Processed {count} sentences with biblical references.")

process_transcripts(text)