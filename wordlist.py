wordlist = []
with open("wordleLis.txt", "r") as f:
    wordlist = list([row.strip().lower() for row in f.readlines()])
