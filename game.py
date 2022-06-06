import unittest
from random import randint
from agents import WordleAgent

from wordlist import wordlist


class Game:
    def __init__(self, goal_word: str = None, max_guesses: int = 6, automated: bool = True) -> None:
        self.new_game(goal_word, max_guesses)
        self.automated = automated

    def new_game(self, goal_word: str = None, max_guesses: int = 6) -> None:
        if goal_word != None:
            self.goal = goal_word
        else:
            self.goal = wordlist[randint(0,len(wordlist)-1)]
        self.max_guesses = max_guesses
        self.current_guess = 0

    def guess(self, guess_word: str) -> tuple[int, str]:
        if self.current_guess >= self.max_guesses:
            raise Exception("Guessing when the game is already over")
        self.current_guess += 1
        evaluation = self._evaluate(guess_word)
        return (self.max_guesses - self.current_guess, evaluation)

    def _evaluate(self, word: str) -> str:
        if not self.automated:
            return input("Enter play result [byg] > ")
        output = ""
        for i, letter in enumerate(word):
            if not letter in self.goal:
                output += "b"
                continue
            if self.goal[i] == letter:
                output += "g"
                continue
            output += "y"
        return output

    def play(self, agent: WordleAgent) -> None:
        print(f"Playing using agent '{agent.name()}'")

        if self.automated:
            print(f"Word to guess is '{self.goal}'")

        # Pick an initial word
        next_guess = agent.initial_word()
        print(f"[?] '{next_guess}'")

        result = self.guess(next_guess)
        print(f"[!] '{result[1]}' ({result[0]} remain)")
        while result[0] > 0:
            next_guess = agent.next_word(next_guess, result[1])
            print(f"[?] '{next_guess}'")

            result = self.guess(next_guess)
            print(f"[!] '{result[1]}' ({result[0]} remain)")

            if result[1] == "ggggg":
                agent.win(result[0])
                break


class Test(unittest.TestCase):
    def test_game_respects_max_attempts(self):
        sut = Game("apple", 6)
        with self.assertRaises(Exception):
            for i in range(10):
                sut.guess("crane")

    def test_game_outputs_expected_evaluation(self):
        sut = Game("apple", 6)
        result = sut.guess("happy")
        self.assertEqual(5, result[0])
        self.assertEqual("bygyb", result[1])

    def test_game_withrepeatmismatch1_outputs_expected_evaluation(self):
        sut = Game("apple", 6)
        result = sut.guess("halls")
        self.assertEqual(5, result[0])
        self.assertEqual("byygb", result[1])

    def test_game_withrepeatmismatch2_outputs_expected_evaluation(self):
        sut = Game("apple", 6)
        result = sut.guess("hippy")
        self.assertEqual(5, result[0])
        self.assertEqual("bbgyb", result[1])

    def test_game_withrepeatmismatch3_outputs_expected_evaluation(self):
        sut = Game("gauge", 6)
        result = sut.guess("aggro")
        self.assertEqual(5, result[0])
        self.assertEqual("yyybb", result[1])
