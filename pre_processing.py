import nltk
import os
import string
from collections import Counter
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.util import ngrams

sermon_text = ""

with open(os.path.join("transcripts", "1000597345214.txt"), 'r') as file:
    sermon_text = file.read()

# Libraries that need to be downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# Initialization of nlp functions
lemmatizer = WordNetLemmatizer()

def tokenize_text(text):
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]
    return sentences, words

def lowercase_tokens(tokens):
    return [[word.lower() for word in sentence] for sentence in tokens]

def remove_punctuation(tokens):
    # Remove punctuation from each sentence
    punctuation_table = str.maketrans('', '', string.punctuation)
    return [[word.translate(punctuation_table) for word in sentence] for sentence in tokens]

def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    return [[word for word in sentence if word not in stop_words] for sentence in tokens]

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_tokens(tokens):
    return [[lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in sentence] for sentence in tokens]

def create_ngrams(tokens, n):
    # Generate n-grams
    ngram_list = list(ngrams(tokens, n))

    # Filter out n-grams with empty strings
    ngram_list = [ngram for ngram in ngram_list if all(isinstance(token, str) and token.strip() for token in ngram)]
    
    return ngram_list

def flatten(list_of_lists):
    """ Flatten a list of lists into a single list """
    return [item for sublist in list_of_lists for item in sublist]

def pre_process_transcript(sermon):
    sentences, words = tokenize_text(sermon)
    text = lowercase_tokens(words)
    text = remove_punctuation(text)
    text = remove_stop_words(text)
    text = lemmatize_tokens(text)
    text = flatten(text)
    bigrams = create_ngrams(text, 2)
    trigrams = create_ngrams(text, 3)
    quadgrams = create_ngrams(text, 4)
    print(quadgrams)
    quingrams = create_ngrams(text, 5)
    return bigrams, trigrams, quadgrams, quingrams

bigrams, trigrams, quadgrams, quingrams = pre_process_transcript(sermon_text)
ngram_counts = Counter(quingrams)
most_common_quadgrams = ngram_counts.most_common(20)  

print("Most Common Quadgrams:")
for ngram, count in most_common_quadgrams:
    print(f"{ngram}: {count}")