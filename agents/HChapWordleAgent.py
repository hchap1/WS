import random
import unittest

from agents.WordleAgent import WordleAgent
from game import Game
from wordlist import wordlist

class HChapWordleAgent:
    def __init__(self, initial: str = "crane", show_debug: bool = False) -> None:
        self._initial = initial
        self._show_debug = show_debug
        self.letters_not_in_word = []
        self.letters_in_word = []
        self.yellow_letters = []
        self.word = "_____"

    def name(self) -> str:
        return "Original hchap1/WordleSolver"

    def initial_word(self) -> str:
        return self._initial
    
    def next_word(self, last_guess: str, feedback: str) -> str:
        if self.process_guess(last_guess, feedback):
            print("Pretty sure we won...")
        candidates = self.find_compatible_words()
        return candidates[random.randint(0, len(candidates)-1)]

    def win(self) -> None:
        print("##### Agent won! #####")

    def process_guess(self, guess_word: str, colour_code: str = None) -> list[str]:
        word_return = ""

        if colour_code == None:
            colour_code = input("> ")
        if colour_code == "ggggg":
            return True
        else:
            for colour in range(5):
                #If the colour is green, record it's position in the word variable, and add it to letters in word.
                if colour_code[colour] == "g":
                    self.letters_in_word.append(guess_word[colour])
                    word_return += guess_word[colour]
                #If it's yellow, record the index and letter in the yellow_words list, then add it
                #to the letters_in_word list.
                elif colour_code[colour] == "y":
                    self.letters_in_word.append(guess_word[colour])
                    self.yellow_letters.append([guess_word[colour], colour])
                    word_return += "_"
                #If it's black, than put it in letters_not_in_word.
                else:
                    if guess_word[colour] not in self.letters_in_word:
                        self.letters_not_in_word.append(guess_word[colour])
                    word_return += "_"
            #Record the new word in the current wordle_attempt object.
            self.word = word_return
            return False


    #Internal function to find a list of compatible words for a criteria.
    #For example, inputting "hel__" will return hello and helix, but if we
    #know that 'O' is not in the word, it will only return helix.
    def find_compatible_words(self):
        potential_words = []
        for word in wordlist:
            word_is_compatible = True
            #If it's not a 5 letter word, than it cannot be the answer.
            if len(word) == 5:
                for index in range(len(word)):
                    #The word is only valid if each character is equal to that of the actual word,
                    #or if said character is unknown in the actual word.
                    if word[index] == self.word[index] or self.word[index] == "_":
                        #If the word contains characters that aren't in the word, remove it from
                        #the sample.
                        if word[index] in self.letters_not_in_word:
                            word_is_compatible = False
                        for yellow_letter in self.yellow_letters:
                            #If the word is missing a letter that was previously yellow,
                            #remove it from the sample.
                            if yellow_letter[0] not in word:
                                word_is_compatible = False
                            #If a yellow letter is repeated at the same index, remove it
                            #from the sample.
                            elif yellow_letter[0] == word[index] and yellow_letter[1] == index:
                                word_is_compatible = False
                            #If the word is missing any letters we know it has, remove
                            #it from the sample
                            for letter in self.letters_in_word:
                                if letter not in word:
                                    word_is_compatible = False
                    else:
                        word_is_compatible = False
                #If this word is still valid after checks, add it to potential_words list.
                if word_is_compatible:
                    potential_words.append(word)
        return potential_words
        

class Test(unittest.TestCase):
    def test_agent(self):
        game = Game(wordlist[random.randint(0, len(wordlist)-1)])
        game.play(HChapWordleAgent())
