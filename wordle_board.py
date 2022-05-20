from typing import Callable, Dict, List
from enum import Enum


class CharacterResponse(Enum):
    GREEN = "g",
    YELLOW = "y",
    GREY = "_"


class InvalidWordLengthException(Exception):
    """An exception raised when a word is used within a wordle board that is not of valid length."""

    def __init__(self, length, expected_length) -> None:
        super().__init__(self, f"Word of length {length} cannot be used on wordle board expecting words of length {expected_length}.")


class WordleException(Exception):
    """A general exception raised when a error occurs on the Wordle board."""


class WordleBoard:
    """
    Represents the state of a wordle board during an attempt without knowledge of the underlying, correct word.
    """

    def __init__(self, possible_words: List[str]) -> None:
        self.available_words = possible_words
        self.word_attempts = []
        self.yellow_chars = []
        self.green_chars = []
        self.word_length = len(possible_words[0])

    def reset_board(self, possible_words: List[str]):
        """Resets the state of the wordle board as if no attempts have been made (word_attempt() calls)."""
        self.available_words = possible_words
        self.word_attempts = []
        self.yellow_chars = []
        self.green_chars = []

    def word_attempt(self, word: str, responses: List[CharacterResponse]):
        """ Updates the wordle board given a response to a word attempt.

        Args:
          word: A word attempt, lower case. Must be same length as self.word_length
          responses: Character responses for each character in the inputted word. Must be same length as paramater word.
        """
        if len(word) != self.word_length:
            raise InvalidWordLengthException(len(word), self.word_length)
        
        if len(responses) != self.word_length:
            raise WordleException(f"Character response has {len(responses)} characters. Expected {self.word_length}.")

        filtered_count = 0

        for i, c, r  in zip(range(self.word_length), word, responses):
            if r == CharacterResponse.GREEN:
                self.green_chars.append(c)
            elif r == CharacterResponse.YELLOW:
                self.yellow_chars.append(c)

            filtered_count  += self.filter_words_with_character(c, r, i)

        self.word_attempts.append(word)
        return filtered_count

    def filter_words_with_character(self, c: str, response: CharacterResponse, index: int) -> int:
        """ Filters words out of the available list of words, given a response to a character at a given index in the word.

        Args:
            c: single character in a-z.
            response: the response to the character c, being played at position, index.
            index: the position in the word where the character was played. Assumed to be within [0, self.word_length]

        Return: The number of words filtered out of the remaining, available words

        NOTE: Inefficient method. Should update data structure of self.available_words to avoid repeated list iterations.
        """
        filtered_count = 0

        # Describe specific filters per response colour
        filter_fns: Dict[CharacterResponse, Callable[[str, str, int], bool]] = {
            CharacterResponse.GREY: lambda c, word, i:    c in word,
            CharacterResponse.YELLOW: lambda c, word, i:  c not in word,
            CharacterResponse.GREEN: lambda c, word, i:   c != word[i]
        }

        for i, word in zip(range(len(self.available_words)),self.available_words):
            if filter_fns[response](c, word, index):
                self.available_words.pop(i)
                filtered_count +=1

        return filtered_count
