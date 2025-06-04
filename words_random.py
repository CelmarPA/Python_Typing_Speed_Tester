import requests
from random import sample

class WordsList:
    """
    A class to retrieve a list of random words from an online API
    based on the specified language.
    Attributes:
        idiom (str): Language code for the desired words.
        words_list (list): List of words retrieved from the API.
    """
    def __init__(self, idiom = None):
        """
        Initialize the WordsList object with an optional language code.
        :param idiom: (str, optional) The language code (e.g., 'en', 'pt-br').
                                      Defaults to None for English.
        """
        self.words_list = None
        self.idiom = idiom
        self.get_words(self.idiom)

    def get_words(self, idiom):
        """
        Fetches the list of words from the random-word-api.
        :param idiom: (str) The language code for the API query.
        """
        try:
            if idiom is None:
                url = "https://random-word-api.herokuapp.com/all"
            else:
                url = f"https://random-word-api.herokuapp.com/all?lang={idiom}"

            # Send GET request to the API
            self.words_list = requests.get(url, timeout = 5).json()
        except Exception as e:
            print(f"Unable to load words: {e}")
            # Fallback list in case of API failure
            self.words_list = ["default", "word", "list", "in", "case", "of", "error"]


    def get_list(self):
        """
         Filters and samples a subset of the retrieved words.

        - Only selects words of length <= 8.
        - Randomly selects up to 200 words.
        :return ist: A list of up to 200 short words.
        """
        # Filter for words with max length of 8
        filtered_words = [word for word in self.words_list if len(word) <= 8]

        # Randomly sample up to 200 words
        words = sample(filtered_words, min(200, len(filtered_words)))

        return words
