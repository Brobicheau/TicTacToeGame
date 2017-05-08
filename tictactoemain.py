import socket
import json
import threading
import time
import sys


from GameProtocol import GameProtocol


# -- waitForMessages --
# -------------------------
# this will continuously listen to messages from the server while the game is going
# -------------------------
def waitForMessages():
    global not_done

    # while the game is still going
    while not_done:

        # find out which status it is and display the correct messages
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


# This will print out the help menu
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

# starting variables
not_done = True
prompt = True
automatch = True

# Build the socket and create the game protocol object
port = sys.argv[2]
host = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (str(host), int(port))
try:
    s.connect(server_address)
except:
    print('could not connected to server')
    not_done = False
lock = threading.Lock()

p = GameProtocol(s, server_address)

# dict for executing commands.
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



# Start message thread
threading.Thread(target=waitForMessages, args={}).start()

print("Welcome to the TicTacToe Game!\n\nyou may now begin entering commands, type 'help' to get list of commands\n\n")

try:

    # while the game is still runnning
    while not_done:

        # get user input either with prompt or without
        if prompt:
            user_input = input()
        else:
            user_input = input("Please Enter Command: ")

        # split the input into its commands
        commands = user_input.split(' ')
        amount_expected = 0

        # if the input is a comment we need to mess with it
        if commands[0] == 'comment' and len(commands) > 2:

            # make base comment string
            comment = ''

            # for each command that isnt the comment command, concat the command to make the comment
            for i in range(len(commands)):
                if i != 0:
                    comment = comment + str(commands[i]) + ' '

            # make the new command with concated comment
            comms = []
            comms.append(commands[0])
            comms.append(comment)
            commands = comms


        try:
            # if the command is help
            if commands[0] == 'help':

                # print the help
                printHelp()

            # if its a command with an argument
            elif len(commands) == 2:

                # Execute it
                amount_expected = pro[commands[0]](commands[1])

            # if its a command without an argument
            elif len(commands) ==1 :

                # execute it
                amount_expected = pro[commands[0]]()

            # otherwise we cant do anything with it, bad input.
            else:
                print("Error: Improper input, please try again")
        except (TypeError, KeyError):

            print("Error: Not valid input")

        time.sleep(.5)


finally:
    # dont forget to close the socket!
    s.close()

