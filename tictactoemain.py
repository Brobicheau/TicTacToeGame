import socket
import json
import threading
import time
import sys


from GameProtocol import GameProtocol

def waitForMessages():
    global not_done
    while not_done:
        try:
            data = s.recv(1024).decode('utf-8')
            message = json.loads(data)
            #lock.acquire()
            if message['status'] == "WAIT":
                print(message['message'])
            elif message['status'] == "OK":
                print(message['message'])
            elif message['status'] == "ERROR":
                print(message['message'])
            elif message['status'] == 'KILL':
                lock.acquire()
                not_done = False
                lock.release()
        except ConnectionResetError:
            print("Error: Connection to server ended, exiting client")
            not_done = False



def printHelp():
    print("login <string> - Takes user inputted string as argument. Places user into server, and if Automatch is enable it will automatically pairs with another player.")
    print("place <int> - Takes user inputted int between 1 and 9 inclusive as argument. Places user's piece on board at entered location. Board placements are as follows:\n1 2 3\n4 5 6\n7 8 9")
    print("exit - Exits the user from the game and server")
    print("games - Returns a list of ongoing games. Games have individual IDs and players in the games are listed")
    print("who - Returns a list of players who are available to play")
    print("play <string> - Takes username as argument. Attempts to start a game with the player entered")
    print("observe <int> - Takes gameID as argument. Allows the user to watch an ongoing game")
    print("unobserve <int> - Takes gameID as argument. If user is observing the entered gameID the user will be disconected from that game")

def changePrompt():
    global prompt
    if prompt:
        prompt = False
    else:
        prompt = True


not_done = True
prompt = True
automatch = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost',8080)
s.connect(server_address)
lock = threading.Lock()

p = GameProtocol(s, server_address)

pro = {
    'games': p.GAMES,
    'place': p.PLACE,
    'exit': p.EXIT,
    'play': p.PLAY,
    'who': p.WHO,
    'login': p.LOGIN,
    'observe':p.OBSERVE,
    'unobserve': p.UNOBSERVE,
    'comment': p.COMMENT,
    'automatch': p.automatch,
    'prompt': changePrompt
}




threading.Thread(target=waitForMessages, args={}).start()

print("Welcome to the TicTacToe Game!\n\nyou may now begin entering commands, type 'help' to get list of commands\n\n")

try:
    while not_done:
        if prompt:
            user_input = input()
        else:
            user_input = input("Please Enter Command: ")
        commands = user_input.split(' ')
        amount_expected = 0
        try:
            if commands[0] == 'help':
                printHelp()
            elif len(commands) == 2:
                amount_expected = pro[commands[0]](commands[1])
            elif len(commands) ==1 :
                amount_expected = pro[commands[0]]()
            else:
                print("Error: Improper input, please try again")
        except (TypeError, KeyError):

            print("Error: Not valid input")

        time.sleep(.5)


finally:
    s.close()

