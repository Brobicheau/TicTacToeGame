import socket
import threading
import json
from GameMaster import GameMaster

gameMaster = GameMaster()

class ThreadServer():

    def __init__(self, host, port):
        self.count = 0
        self.host = host
        self.port = port
        self.username = {}
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
        self.s.listen(20)

        # loop forever
        while True:
            # When we get a new client request
            client, address = self.s.accept()

            # spawn a new thread with it and retturn to listening
            threading.Thread(target = self.listening, args = (client,address, self.count)).start()

            self.count = self.count + 1


    # -- listening --
    # Client: Client to listen for
    # Address: Address of the client we are listening for
    # -- Function--
    # listens for messages from user, and sends them to a parser that will issue commands to the GameMaster
    def listening(self, client, address, id):
        try:
            # keep listening
            while True:
                # get data as bytes
                if not client._closed:
                    bytes = client.recv(1024).decode('utf-8')
                else:
                    break

                # convert to a json object
                data = json.loads(bytes);

                # if we successfully received data
                if data:
                    # Parse it
                    self.parseData(data, client, address, id)
                else:
                    # Otherwise there has been an error, disconnect from client and break loop
                    print('client disconnected')
                    break
        except ConnectionResetError:
            # always make sure connection is closed
            if not client._closed:
                gameMaster.endFromDisconnect(self.username[id])
                print('closing from disconnect')
                client.close()
        finally:
            # always make sure connection is closed
            if not client._closed:
                gameMaster.endFromDisconnect(self.username[id])
                print('closing')
                client.close()

    # -- ParseData --
    # Data: Data received from the user, contains commands and information on how to excecute them
    # Client: Client variable for use in returning messages to users
    # Address: Contains the address of the user to return messages to
    # -- Function --
    # Parses Data received from the user, and decide what commands to send to the GameMaster
    def parseData(self, data, client, address, id):

        # if it is a login request
        if data['request'] == 'LOGIN':
            self.username[id] = data['login']

            # send a login command to the gamemaster with the client, address, username and automatch information
            gameMaster.login(client, address, data['login'], data['automatch'])

        # else if it is a place request
        elif data['request'] == 'PLACE':
            if self.username[id]:
                gameMaster.place(data['place'], self.username[id])
            else:
                message = {
                    'status':'ERROR',
                    'message':'Not logged in, please try again after logging in'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        # else if it is a who request
        elif data['request'] == 'WHO':
            if self.username[id]:
                gameMaster.listPlayers(self.username[id])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        # else if it is an exit request
        elif data['request'] == 'EXIT':
            if self.username[id]:
                gameMaster.exit(self.username[id])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        # else if it is a games request
        elif data['request'] == 'GAMES':
            if self.username[id]:
                gameMaster.listGames(self.username[id])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        # else if it is a play request
        elif data['request'] == 'PLAY':
            if self.username[id]:
                gameMaster.play(self.username[id], data['player'])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        elif data['request'] == 'OBSERVE':
            if self.username[id]:
                gameMaster.addObserver(data['ID'], client, address, self.username[id])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        elif data['request'] == 'UNOBSERVE':
            if self.username[id]:
                gameMaster.removeObserver(data['ID'], self.username[id])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)

        elif data['request'] == 'COMMENT':
            if self.username[id]:
                gameMaster.comment(self.username[id], data['comment'])
            else:
                message = {
                    'status': 'ERROR',
                    'message': 'Not logged in, please try again'
                }
                client.sendto(json.dumps(message).encode('utf-8'), address)


