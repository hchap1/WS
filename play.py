from agents.HChapWordleAgent import HChapWordleAgent
from game import Game

initial = input("What would you like to use as your initial word? ")
game = Game(initial, automated=False)
game.play(HChapWordleAgent())