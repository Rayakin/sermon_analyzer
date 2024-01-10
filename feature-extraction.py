import nltk
import os
import string
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from all_sermon_metadata import all_sermon_metadata
from get_existing_trackIds import get_existing_trackIds

aggregated_texts_by_speaker = {}

for sermon in all_sermon_metadata:
    speaker = sermon['speaker']
    transcript_file = sermon['transcriptFile']
    filename = f"{transcript_file}.txt"

    if speaker not in aggregated_texts_by_speaker:
        aggregated_texts_by_speaker[speaker] = ""

    file_path = os.path.join('transcripts2', filename)
    print(f"Trying to open: {file_path}")

    try:
        with open(file_path, 'r') as file:
            aggregated_texts_by_speaker[speaker] += file.read() + " "
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Print out if file not found


# List of books in the Old and New Testaments
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

# Combine into one list for ease of searching
bible_books = old_testament_books + new_testament_books

biblical_characters = ["Adam", "Eve", "Abel", "Cain", "Seth", "Noah", "Shem", "Ham", "Japheth", "Abraham", "Lot", "Sarah", "Isaac", "Rebekah", "Jacob", "Leah", "Rachel", "Joseph", "Moses", "Aaron", "Miriam", "Joshua", "Caleb", "Samuel", "Saul", "David", "Solomon", "Jonathan", "Absalom", "Elijah", "Elisha", "Isaiah", "Jeremiah", "Ezekiel", "Daniel", "Job", "Ruth", "Naomi", "Esther", "Mordecai", "Ezra", "Nehemiah", "Jesus", "Christ", "Mary", "Joseph", "John the Baptist", "Mary Magdalene", "Lazarus", "Peter", "Andrew", "James", "John", "Philip", "Bartholomew", "Thomas", "Matthew", "James", "Mark", "Luke", "Thaddaeus", "Simon the Zealot", "Judas Iscariot", "Paul", "Barnabas", "Silas", "Timothy", "Titus", "Philemon", "Stephen", "Philip", "Luke", "Priscilla", "Aquila"]



def read_files_from_directory(directory):
    aggregated_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming the sermon files are text files
            with open(os.path.join(directory, filename), 'r') as file:
                aggregated_text += file.read() + " "
    return aggregated_text

text = read_files_from_directory("transcripts")

# Function to count mentions of each book
def count_mentions(text, items):
    book_mentions = Counter()
    for item in items:
        # Using regex to match whole word, avoiding partial matches (e.g., "Job" in "Job's")
        count = len(re.findall(r'\b' + re.escape(item) + r'\b', text, flags=re.IGNORECASE))
        if count > 0:
            book_mentions[item] += count
    return book_mentions

# Counting mentions of each book in the sermon
# OT_book_mentions_count = count_mentions(text, old_testament_books)
# print(OT_book_mentions_count)
# NT_book_mentions_count = count_mentions(text, new_testament_books)
# print(NT_book_mentions_count)
# biblical_characters_mentions_count = count_mentions(text, biblical_characters)
# print(biblical_characters_mentions_count)

for speaker, texts in aggregated_texts_by_speaker.items():
    mentions = count_mentions(texts, old_testament_books)
    print(f"Speaker: {speaker}")
    print(mentions)

for speaker, texts in aggregated_texts_by_speaker.items():
    mentions = count_mentions(texts, new_testament_books)
    print(f"Speaker: {speaker}")
    print(mentions)

for speaker, texts in aggregated_texts_by_speaker.items():
    mentions = count_mentions(texts, biblical_characters)
    print(f"Speaker: {speaker}")
    print(mentions)



# # Function to split text into sentences and count topic frequency
# def count_topic_frequency(text, topic):
#     # Split text into sentences
#     sentences = sent_tokenize(text)
#     print(sentences)
#     # Count how many sentences contain the topic
#     topic_count = sum(topic.lower() in sentence.lower() for sentence in sentences)

#     return topic_count, len(sentences)

# # Example usage
# topic = "Christ"

# topic_count, total_sentences = count_topic_frequency(text, topic)

# print(f"Number of sentences talking about '{topic}': {topic_count}")
# print(f"Total number of sentences: {total_sentences}")
