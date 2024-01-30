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

    file_path = os.path.join('transcripts', filename)
    print(f"Trying to open: {file_path}")

    try:
        with open(file_path, 'r') as file:
            aggregated_texts_by_speaker[speaker] += file.read() + " "
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Print out if file not found


# List of books in the Old and New Testaments
old_testament_books = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "first Samuel","1 Samuel", "second Samuel","2 Samuel", "first Kings","1 Kings", "second Kings","2 Kings", "first Chronicles","1 Chronicles", "second Chronicles","2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

new_testament_books = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "First Corinthians", "1 Corinthians", "Second Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "first Thessalonians", "1 Thessalonians", "second Thessalonians", "2 Thessalonians", "first Timothy","1 Timothy", "second Timothy","2 Timothy", "Titus", "Philemon", "Hebrews", "James", "first Peter", "1 Peter", "second Peter", "2 Peter", "first John","1 John", "second John","2 John", "third John","3 John", "Jude", "Revelation"
]

biblical_characters = [
    "Aaron", "Abednego", "Abel", "Abigail", "Abram","Abraham", "Absalom", "Achitophel", "Ahithophel", "Adam", "Ahab", "Ahasuerus", "Ammon", "Amos", "Ananias", "Andrew", "Asher", "Balaam", "Balthazar", "Barabbas", "Bartholomew", "Baruch", "Bathsheba", "Beelzebub", "Belial", "Belshazzar", "Benjamin", "Boanerges", "Boaz", "Caiaphas", "Cain", "Cephas", "Caspar", "Cush", "Kush", "Dan", "Daniel", "David", "Deborah", "Delilah", "Dinah", "Dives", "Dorcas", "Elias", "Elijah", "Elisha", "Enoch", "Enos", "Ephraim", "Esau", "Esther", "Eve", "Ezekiel", "Ezra", "Gabriel", "Gad", "Gideon", "Gilead", "Gog", "Magog", "Goliath", "Good Samaritan", "Habakkuk", "Hagar", "Haggai", "Ham", "Hannah", "Herod", "Hezekiah", "Hiram", "Holofernes", "Hosea", "Isaac", "Isaiah", "Ishmael", "Issachar", "Jacob", "Jael", "James", "Japheth", "Jehoshaphat", "Jehu", "Jephthah", "Jephte", "Jeremiah", "Jeroboam", "Jesse", "Jesus Christ", "Jethro", "Jezebel", "Joab", "Joel", "John the Baptist", "Jonah", "Jonas", "Jonathan", "Joseph", "Joshua", "Josiah", "Jubal", "Judah", "Judas", "Jude", "Judith", "Laban", "Lazarus", "Leah", "Levi", "Lot", "Luke", "Magus", "Malachi", "Manasseh", "Mark", "Martha", "Mary", "Mary Magdalene", "Matthew", "Matthias", "Melchior", "Melchizedek", "Melchisedech", "Meshach", "Methuselah", "Micah", "Midian", "Miriam", "Mordecai", "Moses", "Nabonidus", "Naboth", "Nahum", "Naomi", "Naphtali", "Nathan", "Nathanael", "Nebuchadnezzar", "Nebuchadrezzar", "Nehemiah", "Nicodemus", "Nimrod", "Noah", "Obadiah", "Paul", "Peter", "Philip", "Pilate", "Potiphar", "Queen of Sheba", "Rachel", "Rebecca", "Reuben", "Ruth", "Salome", "Samson", "Samuel", "Sapphira", "Sarai", "Sarah", "Saul", "Seth", "Shadrach", "Shem", "Simeon", "Magus", "Simon", "Solomon", "Susanna", "Thaddeus", "Thadeus", "Thomas", "Tobit", "Tubal-cain", "Uriah", "Zacharias", "Zachariah", "Zachary", "Zebedee", "Zebulun", "Zechariah", "Zedekiah", "Zephaniah", "Zilpah"
]

# Combine into one list for ease of searching
bible_books = old_testament_books + new_testament_books + biblical_characters

biblical_characters = ["Adam", "Eve", "Abel", "Cain", "Seth", "Noah", "Shem", "Ham", "Japheth", "Abraham", "Lot", "Sarah", "Isaac", "Rebekah", "Jacob", "Leah", "Rachel", "Joseph", "Moses", "Aaron", "Miriam", "Joshua", "Caleb", "Samuel", "Saul", "David", "Solomon", "Jonathan", "Absalom", "Elijah", "Elisha", "Isaiah", "Jeremiah", "Ezekiel", "Daniel", "Job", "Ruth", "Naomi", "Esther", "Mordecai", "Ezra", "Nehemiah", "Jesus", "Christ", "Mary", "Joseph", "John the Baptist", "Mary Magdalene", "Lazarus", "Peter", "Cephas", "Andrew", "James", "John", "Philip", "Bartholomew", "Thomas", "Matthew", "James", "Mark", "Luke", "Thaddaeus", "Simon the Zealot", "Judas Iscariot", "Paul", "Barnabas", "Silas", "Timothy", "Titus", "Philemon", "Stephen", "Philip", "Luke", "Priscilla", "Aquila"]


def read_files_from_directory(directory):
    aggregated_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                aggregated_text += file.read() + " "
    return aggregated_text
text = read_files_from_directory("transcripts")

# Function to count mentions of each book
def count_mentions(text, items):
    ordinal_map = {'first': '1', 'second': '2', 'third': '3'}
    person_map = {'sarai': 'Sarah', 'cephas': 'Peter'}

    for ordinal, number in ordinal_map.items():
        text = re.sub(r'\b' + ordinal + r'\b', number, text, flags=re.IGNORECASE)
    
    for person, agg in person_map.items():
        text = re.sub(r'\b' + person + r'\b', agg, text, flags=re.IGNORECASE)

    book_mentions = Counter()
    for item in items:
        count = len(re.findall(r'\b' + re.escape(item) + r'\b', text, flags=re.IGNORECASE))
        if count > 0:
            book_mentions[item] += count
    return book_mentions

nt_mentions = {}

for speaker, texts in aggregated_texts_by_speaker.items():
    mentions = count_mentions(texts, old_testament_books)
    print(f"Speaker: {speaker}")
    print(mentions)

for speaker, texts in aggregated_texts_by_speaker.items():
    nt_mentions = count_mentions(texts, new_testament_books)
    print(f"Speaker: {speaker}")
    print(mentions)

for speaker, texts in aggregated_texts_by_speaker.items():
    mentions = count_mentions(texts, biblical_characters)
    print(f"Speaker: {speaker}")
    print(mentions)

# Function to split text into sentences and count topic frequency
def count_topic_frequency(text, topic):
    # Split text into sentences
    sentences = sent_tokenize(text)
    print(sentences)
    # Count how many sentences contain the topic
    topic_count = sum(topic.lower() in sentence.lower() for sentence in sentences)

    return topic_count, len(sentences)

# Example usage
topic = "Christ"

topic_count, total_sentences = count_topic_frequency(text, topic)

print(f"Number of sentences talking about '{topic}': {topic_count}")
print(f"Total number of sentences: {total_sentences}")
