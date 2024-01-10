import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download
download('vader_lexicon')

def read_files_from_directory(directory):
    aggregated_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming the sermon files are text files
            with open(os.path.join(directory, filename), 'r') as file:
                aggregated_text += file.read() + " "
    return aggregated_text

def perform_sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

# Usage
directory = "transcripts"
aggregated_text = read_files_from_directory(directory)
sentiment_result = perform_sentiment_analysis(aggregated_text)
print(sentiment_result)