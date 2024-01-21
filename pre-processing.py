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
    lowercased = lowercase_tokens(words)
    cleaned_sentences = remove_punctuation(lowercased)
    filtered_words = remove_stop_words(cleaned_sentences)
    lemmatized_words = lemmatize_tokens(filtered_words)
    flatten_lemmatized_words = flatten(lemmatized_words)
    bigrams = create_ngrams(flatten_lemmatized_words, 2)
    # print(bigrams)
    trigrams = create_ngrams(flatten_lemmatized_words, 3)
    # print(trigrams)
    quadgrams = create_ngrams(flatten_lemmatized_words, 4)
    print(quadgrams)
    pentagrams = create_ngrams(flatten_lemmatized_words, 5)
    # print(pentagrams)
    return quadgrams
    

quadgrams = pre_process_transcript(sermon_text)
quadgram_counts = Counter(quadgrams)
most_common_quadgrams = quadgram_counts.most_common(20)  

print("Most Common Quadgrams:")
for quadgram, count in most_common_quadgrams:
    print(f"{quadgram}: {count}")