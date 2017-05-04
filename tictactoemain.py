import socket
import json
import threading
import time
import sys

import echo as echo

from GameProtocol import GameProtocol

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

    while True:
        print('in thread')
        data = s.recv(1024)
        message = json.loads(data)
        #lock.acquire()
        print(message['message'], flush=True)
        #lock.release()


not_done = True
threading.Thread(target=waitForMessages, args={}).start()

try:
    while not_done:
        user_input = input('Please Enter Command: ')
        commands = user_input.split(' ')
        amount_expected = 0
        try:
            if len(commands) == 2:
                amount_expected = pro[commands[0]](commands[1])
            elif len(commands == 1):
                amount_expected = pro[commands[0]]()
            else:
                print("Error: Improper input, please try again")
        except TypeError:
            print('Exception: Error when processing request')
        time.sleep(.01)


finally:
    s.close()

