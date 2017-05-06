import socket
import json
import threading
import time
import sys

#import echo as echo

from GameProtocol import GameProtocol


not_done = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost',10000)
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
    'automatch': p.automatch
}



def waitForMessages():
    global not_done
    while not_done:
        print('in thread')
        data = s.recv(1024)
        message = json.loads(data)
        #lock.acquire()
        if message['status'] == "WAIT":
            print(message['message'])
        elif message['status'] == "OK":
            print(message['message'])
        elif message['status'] == "ERROR":
            print(message['message'])
        elif message['status'] == 'KILL':
  #          lock.aquire()
            not_done = False
   #         lock.release()
        #print(message['message'], flush=True)
        #lock.release()

def printHelp():
    print("login <string> - Takes user inputted string as argument. Places user into server, and if Automatch is enable it will automatically pairs with another player.")
    print("place <int> - Takes user inputted int between 1 and 9 inclusive as argument. Places user's piece on board at entered location. Board placements are as follows:\n1 2 3\n4 5 6\n7 8 9")
    print("exit - Exits the user from the game and server")
    print("games - Returns a list of ongoing games. Games have individual IDs and players in the games are listed")
    print("who - Returns a list of players who are available to play")
    print("play <string> - Takes username as argument. Attempts to start a game with the player entered")
    print("observe <int> - Takes gameID as argument. Allows the user to watch an ongoing game")
    print("unobserve <int> - Takes gameID as argument. If user is observing the entered gameID the user will be disconected from that game")

threading.Thread(target=waitForMessages, args={}).start()

try:
    while not_done:
        user_input = input('Please Enter Command: ')
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
        except TypeError:
            print('Exception: Error when processing request')
            print(TypeError)

        time.sleep(.5)


finally:
    s.close()

