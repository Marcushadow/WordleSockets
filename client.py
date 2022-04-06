import socket
import os
import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])

install("art")
from art import *
os.system('color')  


serverSocket = socket.socket()
ip = input("What ip address: ")
serverSocket.connect((ip, 12345))


print(serverSocket.recv(1024).decode())
print(serverSocket.recv(1024).decode())

guesses = 6
while(guesses > 0):
    guess = str(input("Please make your guess: "))



    serverSocket.sendall(guess.encode())
    # print(serverSocket.recv(1024).decode())
    result = serverSocket.recv(1024).decode()

    if(str(result).endswith("/WIN")):

        print(str(result)[:-4])
        print("YOU WON")

        try:
            aprint(word)
        except:
            print(randart())

        guesses = 0
    
    else:
        print(str(result))
        guesses -= 1