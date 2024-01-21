import os
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

def split_text_into_sentences(directory):
    sentences = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                sentences = sent_tokenize(file.read())
                avernage_sentence_length = average_length_of_sentences(sentences)
                average_word_count = average_word_count_per_sentences(sentences)
                max_words = max_word_length_sentence(sentences)
                print(f"{filename}: Sentences: {len(sentences)}, Avg. Senetence Length: {avernage_sentence_length}, Avg. Word Count: {average_word_count}, Max Sentence Length: {max_words}")

def average_length_of_sentences(sentences):
    average_length = []
    for sentence in sentences:
        average_length.append(len(sentence))
    average = sum(average_length) / len(average_length)
    return average

def average_word_count_per_sentences(sentences):
    average_word_count = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        average_word_count.append(len(words))
    average = sum(average_word_count) / len(average_word_count)
    return average

def max_word_length_sentence(sentences):
    word_count = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        word_count.append(len(words))
    max_words = max(word_count)
    return max_words

directory = "transcripts"
sentences = split_text_into_sentences(directory)