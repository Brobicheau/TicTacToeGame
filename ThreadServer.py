import socket
import threading
import json
from GameMaster import GameMaster

gameMaster = GameMaster()

class ThreadServer():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = ''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        # self.gm = {
        #     'PLACE':self.gm.place,
        #     'GAMES': self.pm.games,
        #     'LOGIN': self.pm.login,
        #     'WHO' : self.pm.who,
        #     'EXIT' : self.pm.exit,
        #     'PLAY' : self.pm.play
        # }

    # -- statNewClient
    # --Function--
    # Listens for any new clients, then spawns a thread for each new client.
    def startNewClient(self):

        # listen with the socket
        self.s.listen()

        # loop forever
        while True:
            # When we get a new client request
            client, address = self.s.accept()

            # spawn a new thread with it and retturn to listening
            threading.Thread(target = self.listening, args = (client,address)).start()


    # -- listening --
    # Client: Client to listen for
    # Address: Address of the client we are listening for
    # -- Function--
    # listens for messages from user, and sends them to a parser that will issue commands to the GameMaster
    def listening(self, client, address):
        try:
            # keep listening
            while True:
                # get data as bytes
                bytes = client.recv(1024)

                # convert to a json object
                data = json.loads(bytes);

                # if we successfully received data
                if data:
                    # Parse it
                    self.parseData(data, client, address)
                else:
                    # Otherwise there has been an error, disconnect from client and break loop
                    print('client disconnected')
                    break
        finally:
            # always make sure connection is closed
            print('closing')
            client.close()

    # -- ParseData --
    # Data: Data received from the user, contains commands and information on how to excecute them
    # Client: Client variable for use in returning messages to users
    # Address: Contains the address of the user to return messages to
    # -- Function --
    # Parses Data received from the user, and decide what commands to send to the GameMaster
    def parseData(self, data, client, address):

        # if it is a login request
        if data['request'] == 'LOGIN':
            self.username = data['login']

            # send a login command to the gamemaster with the client, address, username and automatch information
            gameMaster.login(client, address, data['login'], data['automatch'])

        # else if it is a place request
        elif data.request == 'PLACE':
            self.gameMaster.place(data.place.move, self.username)

        # else if it is a who request
        elif data.request == 'WHO':
            self.gameMaster.place

        # else if it is an exit request
        elif data.request == 'EXIT':
            self.gameMaster.exit()

        # else if it is a games request
        elif data.request == 'GAMES':
            self.gameMaster.games()

        # else if it is a play request
        elif data.request == 'PLAY':
            self.gameMaster.play(self.username)




