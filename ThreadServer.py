import socket
import threading
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

    def startNewClient(self):
        self.s.listen()
        while True:
            client, address = self.s.accept()
            print('sup')
            threading.Thread(target = self.listening, args = (client,address)).start()

    def listening(self, client, address):
        name = None
        while True:
            data = client.recv(1024)
            try:
                if data:
                    self.parseData(data, name, client, address)
                else:
                    print('client disconnected')
                    break
            finally:
                client.close()

    def parseData(self, data, client):
        if data.request == 'LOGIN':
            self.username = data.login
            self.gameMaster.login(data.login)
        elif data.request == 'PLACE':
            self.gameMaster.place(data.place.move, self.username)
        elif data.request == 'WHO':
            self.gameMaster.place
        elif data.request == 'EXIT':
            self.gameMaster.exit()
        elif data.request == 'GAMES':
            self.gameMaster.games()
        elif data.request == 'PLAY':
            self.gameMaster.play()




