import nltk
import pickle
import os
import string
from collections import Counter
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag, sent_tokenize, wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.util import ngrams
from nltk.corpus import PlaintextCorpusReader
from corpus_monitor import SermonCorpusReader

# Define the directory where your transcripts are stored
corpus_root = './transcripts'  # Update this to the path of your Transcripts directory

class Preprocessor(object):
    """
    The preprocessor wraps an `HTMLCorpusReader` and performs tokenization
    and part-of-speech tagging.
    """
    def __init__(self, corpus, target=None, **kwargs):
        self.corpus = corpus
        self.target = target

    def fileids(self, fileids=None, categories=None):
        fileids = self.corpus.resolve(fileids, categories)
        if fileids:
            return fileids
        return self.corpus.fileids()

    def abspath(self, fileid):
        # Find the directory, relative to the corpus root.
        parent = os.path.relpath(
            os.path.dirname(self.corpus.abspath(fileid)), self.corpus.root
        )

        # Compute the name parts to reconstruct
        basename  = os.path.basename(fileid)
        name, ext = os.path.splitext(basename)

        # Create the pickle file extension
        basename  = name + '.pickle'

        # Return the path to the file relative to the target.
        return os.path.normpath(os.path.join(self.target, parent, basename))
    
    def tokenize(self, fileid):
        for doc in self.corpus(fileids=fileid):
            sentences = sent_tokenize(doc)
            yield [
                pos_tag(wordpunct_tokenize(sent))
                for sent in sentences
            ]

    def process(self, fileid):
        """
        For a single file, checks the location on disk to ensure no errors,
        uses +tokenize()+ to perform the preprocessing, and writes transformed
        document as a pickle to target location.
        """
        # Compute the outpath to write the file to.
        target = self.abspath(fileid)
        parent = os.path.dirname(target)

        # Make sure the directory exists
        if not os.path.exists(parent):
            os.makedirs(parent)

        # Make sure that the parent is a directory and not a file
        if not os.path.isdir(parent):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )

        # Create a data structure for the pickle
        document = list(self.tokenize(fileid))

        # Open and serialize the pickle to disk
        with open(target, 'wb') as f:
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

        # Clean up the document
        del document

        # Return the target fileid
        return target
    
    def transform(self, fileids=None, categories=None):
        # Make the target directory if it doesn't already exist
        if not os.path.exists(self.target):
            os.makedirs(self.target)

        # Resolve the fileids to start processing
        for fileid in self.fileids(fileids, categories):
            yield self.process(fileid)


sermon_text = ""

directory = "transcripts"

def read_files_from_directory(directory):
    aggregated_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                aggregated_text += file.read() + " "
    return aggregated_text

# text = read_files_from_directory("transcripts")


# with open(os.path.join("transcripts", "1000597345214.txt"), 'r') as file:
#     sermon_text = file.read()

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

# bigrams, trigrams, quadgrams, quingrams = pre_process_transcript(text)
# ngram_counts = Counter(quingrams)
# most_common_quadgrams = ngram_counts.most_common(20)  

# print("Most Common Quadgrams:")
# for ngram, count in most_common_quadgrams:
#     print(f"{ngram}: {count}")