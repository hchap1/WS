import random, time

with open("wordleLis.txt", "r") as wordList:
    words = wordList.readlines()

"""
Consider using a Settings/Options object here for two reasons: 
   1. If you wanted to add more settings in the future (say a variable `word_file` letting a user 
    pick where the wordleLis.txt file is stored), you don't have to rewrite all your functions to
     pass around both `diag` and `word_file`. You can pass around the object itself.
   2. Engineering is a team sport. If you use an Options object, another engineer will be able to
    see `if options.diag` and understand at the very least it's a user defined option.

It would look something like this:
```
from dataclasses import dataclass

@dataclass
class Options:
    diag: bool 
    ... etc.
```
See https://docs.python.org/3/library/dataclasses.html for more details.
"""

#Option to print things as it goes (cool to watch, and useful for debugging)
diag = input("Display extra information? (Y/N)\n> ").lower()[0]
if diag == "y":
    diag = True
else:
    diag = False

"""
1. Consider turning these into a class. A wordle attempt is like an object. 
2. Also, short variable names like this are generally discouraged (except in Golang!). Ideally a line 
of code is as self-explanatory as possible. If an engineer sees, or you a few months from  now
(trust me, you always think you'll understand your code more than you do a few months later)
 `for f in iW:` they may have an idea what that means, and perhaps they can just search for `iW` 
 and see your comment, but a well name variable is like having the comment on every line. 
 For example, `for l in letters_in_solution` is nearly impossible to confuse.

"""
#Variables
#nIW = not in word, and stores letters not in word.
nIW = []
#iW = in word.
iW = []
#Yellow Word solution
yellowWords = []

"""
Like variable names, function names can act as a comment in themselves. A good function name 
describes what it does (like a verb, compared to a noun). If I saw in the code  
   `for w in avWords("h_l__")` I would know what the input is and somehow it returns a list, but 
   what it does is still unclear. Consider:
   ```
        remaining_words = get_words_satisfying("h_l__")
        for w in remaining_words
   ```
It tells me:
  1. A list (or technically an Iterable) of words are being returned.
  2. Those words return "satisfy" the input "h_l__". In this case "satisfy just means h and l are 
     in the right slots, not that yellowWords, nIW ot iW are considered.
  3. Words that satisfy "h_l__" are considered remaining.
"""    
#Function to return available words.
def avWords(word):
    #Imput type: h_l__
    #Returns hello, holly, ect. 
    aW = []
    for i in words:
        #To improve efficiency, check the first letter, because if the first
        #letter is not the same, than the word can't be.
        """ Fun improvement: Regex. 
        import re

        # In regex, instead of a '_', a '.' says "I expect a single character here". So "h_l__" --> "h.l..$" says, 
        # start with a "h", any character, "l", two more characters, then stop (the "$" means no more characters are allowed)
        pattern = re.compile(word.replace("_", ".") + "$")

        aW = []
        for i in words:
            if pattern.match(word):
                ...

        """
        if i[0] == word[0] or word[0] == "_":
            if i[1] == word[1] or word[1] == "_":
                if i[2] == word[2] or word[2] == "_":
                    if i[3] == word[3] or word[3] == "_":
                        if i[4] == word[4] or word[4] == "_":
                            #If each letter in the word is the same as the word
                            #passed into the function, than than add it to the
                            #list.
                            aW.append(i.strip())
    #Return available words.
    return aW

#This function runs a wordle inside the python program.

#(Used when testing, and kept so that I could use the same data structure in
#the new guess function)
'''
def guess(g):
    guessReturn = ""
    if g == word:
        print("Victorious: %s" % g)
    else:
        print("Tried: %s" % g)
        for i in range(len(g)):
            if g[i] == word[i]:
                guessReturn += g[i]
                iW.append(g[i])

            elif g[i] in word:
                iW.append(g[i])
                guessReturn += "_"
            else:
                nIW.append(g[i])
                guessReturn += "_"
        return guessReturn
'''

"""
This is a better function name. But what is 'g'? Also this is a good example where you could do two more things:
    1. Function docstrings: They provide more details about a function (e.g what the variables are, 
       are there any constraints on them (e.g. cannot be "" string)). See some good examples here,
       https://the-examples-book.com/book/python/docstrings-and-comments#docstrings. In this case, 
       consider documenting what is the format of the string 'g'.
    2. Typing: These are annotations that tell the engineer (not python itself), what is the type 
        of the inputs and outputs. For example:
          `def guess(g: str) -> List[str]:`
        Without diving into the code and looking around, someone can immediately see what we 
        expect, and what is returned.
"""
#Function for allowing the user to tell the bot what color the letters are.
def guess(g):
    guessReturn = ""
    print("Try: %s" % g)
    if input("[R]estart, [C]ontinue\n> ").lower()[0] == "r":
        nIW.clear()
        iW.clear()
        yellowWords.clear()
        solve()
    else:
        #They enter the colors for example: ggybb
        wordResult = input("ENTER THE RESULT\n> ").lower()
        for i in range(len(wordResult)):
            #If the letter is green, than add it to letters that are in the 
            #and add it to the computers understanding of the word.
            if wordResult[i] == "g":
                guessReturn += g[i]
                if g[i] in nIW:
                    nIW.pop(g[i])
                iW.append(g[i])           
            #If the letter is yellow, than add it to letters in the word, but
            #add an unknown to the computers understanding of the word.
            elif wordResult[i] == "y":
                guessReturn += "_"
                iW.append(g[i])
                yellowWords.append([g[i], i])
            #If the letter is neither green nor yellow, put an unknown in the
            #computers understanding of the word, and put the letter in the
            #list of letters not in the word.
            else:
                guessReturn += "_"
                if g[i] not in iW:
                    nIW.append(g[i])
        #Return the new understanding of the word. It might look something like
        #this.
        return guessReturn
                
            
"""
Mainly what I said above. 
"""
def narrow(wordList):
    clean = []
    for w in wordList:
        """
        When we have to use a temporary return variable (in this case `thisWord`), it's a good 
        candidate to extract it to a new function. That way we can return earlier, avoiding running
        unnecessary logic, and it makes it cleaner. E.g:
        ```
        for char in nIW:
            if word_is_not_incorrect(w):
                clean.append(w)
        
        
        def word_is_not_incorrect(w: str) -> bool:
            ....
        ```
        """
        thisWord = True
        #If ANY of the characters that are not in the word are present in the
        #word passed into the function, remove the word as it cannot be it
        for char in nIW:
           if char in w:
                thisWord = False
        #If ANY of the characters we know are in the word are missing in the
        #word, than remove the word.
        for char in iW:
            if char not in w:
                thisWord = False
        for char in range(len(w)):
            for yW in yellowWords:
                if yW[1] == char:
                    if w[char] == yW[0]:
                        thisWord = False
            
        if thisWord:
            #if diag:
                #print("%s is valid." % w)
            clean.append(w)
        #else:
            #print("%s is invalid." % w)
    #Return the cleaned list.
    return clean

def solve():
    #Find potential words given a starting word.
    """
    Why are you making me guess "crane" for my first turn :( 
    """
    potWords = narrow(avWords(guess("crane")))

    if True:
        for i in range(10):
            try:
                actualPot = []
                for i in potWords:
                    goodWord = True
                    for f in iW:
                        if f not in i:
                            goodWord = False
                    #Checking if the words passed in is valid/
                    if goodWord:
                        actualPot.append(i)
                #Printing all of the potential words.
                if diag:
                    print("Potential words:\n%s" % ", ".join(actualPot))
                    print("Letters not in word: %s" % "".join(nIW))
                    print("Letters in word: %s" % "".join(iW))
                #Sleep a second to impress people watching (even though it takes
                #mere milliseconds)
                if diag:
                    time.sleep(1) ## Another candidate to be included in an Options object. How long to sleep for.
                #Pick a random word from the potential words.
                myGuess = actualPot[random.randint(0, len(actualPot)-1)]
                if diag:
                    print("TRYING: %s" % myGuess)
                #Pass it through to the user to try, and then repeat, each time
                #narrowing the selection.
                potWords = narrow(avWords(guess(myGuess)))
            except:
                """
                We shouldn't use an exception for an expected case. 
                Also, it's always good practice to at least log out the exception. Why? Well there
                will be one day, perhaps long from now, where your code breaks for a reason that
                is new or not expected. And on that day, you will want to know what the exception 
                was. Trust me.
                ```
                try:
                    ...
                except Exception as e:
                    print(repr(e)) # Tell me the exception type and a message.
                    ... 
                ```
                Side note: Try not to catch Exception, but rather, only catch specific exceptions, e.g. ZeroDivisionError. 
                """
                print("DONE")
                break

"""
Do the following:
```
if __name__ == "__main__":
    solve():
``` 
Why? Well you only want to run `solve()` when a user runs `python wordleCracker.py` (that's what 
this if statement is checking). In the future, perhaps you want to reuse some of the code here.
 If you try importing from this file without it, it will also run solve().
```
from wordleCracker import solve # this would runs solve() too !!!
```

"""
solve()
    
    

            
            
    

