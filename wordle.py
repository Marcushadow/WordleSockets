import enchant
import sys
import socket
from termcolor import colored
d = enchant.Dict("en_US")

class WordleWord:
    def __init__(self, word="wordo"):
        word = word.lower()
        if(self.eligibilityCheck(word)):
            self.word = word
        else:
            raise ValueError("WordleWord must be real US English word 5 letters long, alphabets only")

        self.WordDict = {}
        for letter in self.word:
            if(letter in self.WordDict.keys()):
                self.WordDict[letter] += 1
            else:
                self.WordDict[letter] = 1


    def eligibilityCheck(self, word):
        if(len(word) != 5 or not(word.isalpha())):
            return False
        
        return d.check(word)

    def changeWord(self, newWord):
        if(self.eligibilityCheck(newWord)):
            self.word = newWord

    def reveal(self):
        print(f"""
------------------------------------
The Word is
[{self.word}]
------------------------------------
""")
    
    def revealWordDict(self):
        print(self.WordDict)
    
    def check(self, testWord):
        gc = 0
        outputMatrix = [0,0,0,0,0]
        returnWord = []
        guessMapping = self.WordDict.copy()
        if(self.eligibilityCheck(testWord)):
      
            for i in range(5):
                if(testWord[i] == self.word[i]):
                    outputMatrix[i] = 1
                    guessMapping[testWord[i]] -= 1

            for i in range(5):
                if(outputMatrix[i] != 1):

                    if((testWord[i] in guessMapping.keys()) and guessMapping[testWord[i]] != 0):
                        outputMatrix[i] = 2
                        guessMapping[testWord[i]] -= 1

        
            for i in range(5):
                if (outputMatrix[i] == 1):
                    gc += 1
                    returnWord.append(colored(testWord[i], 'green'))
                
                elif (outputMatrix[i] == 2):
                    returnWord.append(colored(testWord[i], 'yellow'))
                
                else:
                    returnWord.append(colored(testWord[i], 'white'))

            if(gc == 5):
                return ' '.join(returnWord) + "/WIN"
            else:
                return ' '.join(returnWord)
            
        else:
            return None

class WordleGuesser:
    def __init__(self, word):
        self.word = WordleWord(word)
        self.guessCounter = 5
    
    def guessOne(self, guessV):
        if (self.word.eligibilityCheck(guessV)):
    
            self.guessCounter -= 1
            return self.word.check(guessV) 

        else:
            return "Fail"


    # def guess(self):
    #     print(colored("W", "red", attrs=['bold', 'blink']), colored("O", "cyan", attrs=['bold', 'blink']), colored("R", "yellow", attrs=['bold', 'blink']), colored("D", "green", attrs=['bold', 'blink']), colored("L", "blue", attrs=['bold', 'blink']), colored("E", "magenta", attrs=['bold', 'blink']), colored("R", "red", attrs=['bold', 'blink']))
    #     guessV = input("")
    #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #     while((self.guessCounter > 0)):
    #         if (self.word.eligibilityCheck(guessV)):

    #             # print(self.guessCounter)
    #             self.guessCounter -= 1
    #             # Skip to previous line
    #             # print("\033[A                             \033[A")
    #             print(self.word.check(guessV))
    #             print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #             guessV = input("")
    #             print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    #         else:
    #             print("Value")
    

todaysWord = "dryad"

serverSocket = socket.socket()

serverSocket.bind(("192.168.179.74", 12345))
serverSocket.listen()

receivedSocket , addr = serverSocket.accept()

receivedSocket.sendall("Welcome to Wordle!!".encode())
receivedSocket.sendall("Please make your first guess: ".encode())

Guesser1 = WordleGuesser(todaysWord)
guesses = 6

while(guesses > 0):
    guess = receivedSocket.recv(1024).decode()
    # print(guess)

    receivedSocket.sendall(Guesser1.guessOne(guess).encode())
    print("Sent")
    guesses -= 1



# print(returnObject.decode())

receivedSocket.close()
