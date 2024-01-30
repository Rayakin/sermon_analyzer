import nltk
import os
import time
from nltk.corpus.reader.api import CategorizedCorpusReader
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader


DOC_PATTERN = r'(?!\.)[\w_\s]+/[\w\s\d\-]+\.txt'
CAT_PATTERN = r'([\w_\s]+)/.*'

from nltk.corpus.reader import CategorizedPlaintextCorpusReader

class SermonCorpusReader(CategorizedPlaintextCorpusReader):
    def __init__(self, root, fileids, cat_pattern=None, cat_map=None, cat_file=None, **kwargs):
        # Ensure only one of cat_pattern, cat_map, cat_file is provided
        cat_args = [cat_pattern, cat_map, cat_file]
        if sum(arg is not None for arg in cat_args) != 1:
            raise ValueError("Specify exactly one of: cat_pattern, cat_map, cat_file")

        # Initialize the CategorizedPlaintextCorpusReader with the provided arguments
        super().__init__(root, fileids, cat_pattern=cat_pattern)

    def resolve(self, fileids, categories):
            """
            Returns a list of fileids or categories depending on what is passed
            to each internal corpus reader function. Implemented similarly to
            the NLTK ``CategorizedPlaintextCorpusReader``.
            """
            if fileids is not None and categories is not None:
                raise ValueError("Specify fileids or categories, not both")

            if categories is not None:
                return self.fileids(categories)
            return fileids

    def docs(self, fileids=None, categories=None):
            """
            Returns the complete text of an HTML document, closing the document
            after we are done reading it and yielding it in a memory safe fashion.
            """
            # Resolve the fileids and the categories
            fileids = self.resolve(fileids, categories)

            # Create a generator, loading one document into memory at a time.
            for path, encoding in self.abspaths(fileids, include_encoding=True):
                print("Reading file:", path)  # Debugging line
                with open(path, 'r', encoding=encoding) as file:
                    yield file.read()

    def describe(self, fileids=None, categories=None):
            """
            Performs a single pass of the corpus and
            returns a dictionary with a variety of metrics
            concerning the state of the corpus.
            """
            started = time.time()

            # Structures to perform counting.
            counts  = nltk.FreqDist()
            tokens  = nltk.FreqDist()

            for sent in self.sents(fileids, categories):
                counts['sents'] += 1
                for word in sent:
                    counts['words'] += 1
                    tokens[word] += 1

            # Compute the number of files and categories in the corpus
            n_fileids = len(self.resolve(fileids, categories) or self.fileids())
            n_topics  = len(self.categories(self.resolve(fileids, categories)))

            # Return data structure with information
            return {
                'files':  n_fileids,
                'topics': n_topics,
                'sents':  counts['sents'],
                'words':  counts['words'],
                'vocab':  len(tokens),
                'lexdiv': float(counts['words']) / float(len(tokens)),
                'ppdoc':  float(counts['paras']) / float(n_fileids),
                'secs':   time.time() - started,
            }

    def sizes(self, fileids=None, categories=None):
            """
            Returns a list of tuples, the fileid and size on disk of the file.
            This function is used to detect oddly large files in the corpus.
            """
            # Resolve the fileids and the categories
            fileids = self.resolve(fileids, categories)

            # Create a generator, getting every path and computing filesize
            for path in self.abspaths(fileids):
                yield os.path.getsize(path)

corpus = SermonCorpusReader('./transcripts', DOC_PATTERN, cat_pattern=CAT_PATTERN)

print(corpus.categories())
print(corpus.fileids())
print(corpus.sizes())
print(corpus.resolve(fileids=DOC_PATTERN, categories=None))
# print(corpus.docs())
print(corpus.describe())

docs = corpus.docs()

for doc in docs:
     print(doc)