import random, time

with open("wordleLis.txt", "r") as wordList:
    words = wordList.readlines()
    for word_index in range(len(words)):
        words[word_index] = words[word_index].strip("\n")

debug = input("Show Proccesses? (y/n)\n> ")
sw = input("Starter Word?\n> ")

class rules:
    #Only two rules for now, but if I add more later, this class with be usefull.
    def __init__(self, show_debug, starter_word):
        if show_debug.lower()[0] == "y":
            self.show_debug = True
        else:
            self.show_debug = False
        if starter_word.lower() in words and len(starter_word) == 5:
            #If it is a valid starter word
            self.starter_word = starter_word
        else:
            #If it's not a valid word, set it to crane by default.
            self.starter_word = "crane"

class wordle_attempt:
    #Wordle object - contains EVERYTHING
    def __init__(self, show_debug, starter_word):
        self.word = "_____"
        self.letters_not_in_word = []
        self.letters_in_word = []
        self.yellow_letters = []
        self.rules = rules(show_debug, starter_word)
        self.potential_words = []

    #Internal function to find a list of compatible words for a criteria.
    #For example, inputting "hel__" will return hello and helix, but if we
    #know that 'O' is not in the word, it will only return helix.
    def find_compatible_words(self):
        self.potential_words.clear()
        for word in words:
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
                    self.potential_words.append(word)

    def solve(self):
        #Create an intital list based on a first guess.
        guess(self.rules.starter_word)
        self.find_compatible_words()
        #Repeat for each remaining guess.
        for new_guess_index in range(5):
            if self.rules.show_debug:
                print("Potential Words: %s" % ", ".join(self.potential_words))
                print("Letters not in Word: %s" % "".join(self.letters_not_in_word))
                print("Letters in Word: %s" % "".join(self.letters_in_word))
            if guess(self.potential_words[random.randint(0, len(self.potential_words)-1)]):
                break
            self.find_compatible_words()
            
def guess(guess_word: str) -> List[str]:
    word_return = ""
    #Pass word to user, so that they can return the colours.
    print("Try '%s'." % guess_word.strip("\n"))
    colour_code = input("> ")
    if colour_code == "ggggg":
        #They won!
        print("\n" * 40)
        return True
    else:
        for colour in range(5):
            #If the colour is green, record it's position in the word variable, and add it to letters in word.
            if colour_code[colour] == "g":
                current_attempt.letters_in_word.append(guess_word[colour])
                word_return += guess_word[colour]
            #If it's yellow, record the index and letter in the yellow_words list, then add it
            #to the letters_in_word list.
            elif colour_code[colour] == "y":
                current_attempt.letters_in_word.append(guess_word[colour])
                current_attempt.yellow_letters.append([guess_word[colour], colour])
                word_return += "_"
            #If it's black, than put it in letters_not_in_word.
            else:
                if guess_word[colour] not in current_attempt.letters_in_word:
                    current_attempt.letters_not_in_word.append(guess_word[colour])
                word_return += "_"
        #Record the new word in the current wordle_attempt object.
        current_attempt.word = word_return
        return False

if __name__ == "__main__":
    while True:
        current_attempt = wordle_attempt(debug, sw)
        current_attempt.solve()
    

            
            
    
