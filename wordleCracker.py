import random, time

with open("wordleLis.txt", "r") as wordList:
    words = wordList.readlines()

#Option to print things as it goes (cool to watch, and useful for debugging)
diag = input("Display extra information? (Y/N)\n> ").lower()[0]
if diag == "y":
    diag = True
else:
    diag = False

#Variables
#nIW = not in word, and stores letters not in word.
nIW = []
#iW = in word.
iW = []
    
#Function to return available words.
def avWords(word):
    #Imput type: h_l__
    #Returns hello, holly, ect. 
    aW = []
    for i in words:
        #To improve efficiency, check the first letter, because if the first
        #letter is not the same, than the word can't be.
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

#Function for allowing the user to tell the bot what color the letters are.
def guess(g):
    guessReturn = ""
    print("Try: %s" % g)
    if input("[R]estart, [C]ontinue\n> ").lower()[0] == "r":
        nIW.clear()
        iW.clear()
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
                
            

def narrow(wordList):
    clean = []
    for w in wordList:
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
                    time.sleep(1)
                #Pick a random word from the potential words.
                myGuess = actualPot[random.randint(0, len(actualPot)-1)]
                if diag:
                    print("TRYING: %s" % myGuess)
                #Pass it through to the user to try, and then repeat, each time
                #narrowing the selection.
                potWords = narrow(avWords(guess(myGuess)))
            except:
                print("DONE")
                break

solve()
    
    

            
            
    
