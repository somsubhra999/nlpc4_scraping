import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.probability import FreqDist
from string import punctuation
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Ngram:
    def __init__(self, text):
        """
        Initialize
        :param text: The string based on which the Ngram instance is created
        """
        self.stop_words = set(stopwords.words('english'))
        self.text = text
        self.correction_dict = dict()
        tokens = [token.lower() for token in nltk.word_tokenize(text)]
        self.tokens = self.raw_tokens = tokens
        self.filter_tokens(stpwords=True, punct=True)

    def filter_tokens(self, stpwords=False, punct=False):
        """
        Filter out tokens which are stopwords or punctuation characters based on parameters
        :param stpwords: Filter out stopwords if set to True
        :param punct: Filter out punctuation characters if set to True
        :return: Nothing
        """
        self.tokens = self.raw_tokens
        if stpwords:
            self.tokens = [token for token in self.tokens if token not in self.stop_words]
        if punct:
            self.tokens = [token for token in self.tokens if token not in punctuation]

    def get_ngrams(self, n):
        """
        Get a list of n-grams for the tokens attribute
        :param n: The value of n in n-gram. eg. n=2 means bi-gram
        :return: List of n-grams
        """
        return ngrams(self.tokens, n)

    def get_fdist(self, n):
        """
        Get the frequency distribution for every n-gram (for a particular value of n).
        Uses instance method get_ngrams to get the ngrams
        :param n: The value of n in n-gram. eg. n=2 means bi-gram
        :return: The frequency distribution object
        """
        if n == 1:
            fd = FreqDist(self.tokens)
        else:
            fd = FreqDist(self.get_ngrams(n))
        return fd

    @staticmethod
    def update_fdist(old_fdist, new_ngrams):
        """
        Updates the frequency distribution object for a new list of n-grams.
        Useful when generating a single fdist from a text stream like when reading a file line by line
        :param old_fdist: The old frequency distribution object
        :param new_ngrams: The new list of n-grams which need to be included in fdist calculation
        :return: The new frequency distribution object
        """
        new_fdist = old_fdist
        for ng in new_ngrams:
            new_fdist[ng] += 1
        return new_fdist

    @staticmethod
    def filter_fdist(old_fdist, keyword):
        """
        Filters the frequency distribution object and keeps only n-grams which include the provided keyword
        :param old_fdist: The old frequency distribution object
        :param keyword: The word which must be necessarily present in every n-gram in the fdist
        :return: The new frequency distribution object after filtering
        """
        new_fdist = FreqDist()
        for ng in old_fdist:
            if keyword in ng:
                new_fdist[ng] = old_fdist[ng]
        return new_fdist

    @staticmethod
    def get_word_cloud(words, width=800, height=800, background_color='white', min_font_size=10):
        """
        Plot the wordcloud image based on parameters and word string
        :param words: The string containing words to be used
        :param width: Width of the image
        :param height: Height of the image
        :param background_color: Bg color of the image
        :param min_font_size: Size of the smallest word in the wordcloud
        :return: Nothing
        """
        wc = WordCloud(width=width, height=height,
                       background_color=background_color,
                       min_font_size=min_font_size).generate(words)

        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wc)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
