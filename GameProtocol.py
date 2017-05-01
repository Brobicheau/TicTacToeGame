import json


class GameProtocol():

    def __init__(self, socket, address):
         self.server_address = address
         self.socket = socket

    def LOGIN(self, login):
        message = {
            'request': 'LOGIN',
            'login': login
        }
        self.socket.sendto(json.dumps(login).encode('utf-8'), self.server_address)
        return len(message)

    def PLACE(self, move):
        message = {
            'request':'PLACE',
            'place':move
        }
        self.socket.sendto(json.dumps(move).encode('utf-8'), self.server_address)
        return len(message)

    def GAMES(self):
        message ={
            'request':'GAME'
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)
        return len(message)

    def WHO(self):
        message = {
            'request':'WHO',
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)
        return len(message)

    def PLAY(self, player):
        message = {
            'request':'PLAY',
            'player': player
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)
        return len(message)

    def EXIT(self):
        message = {
            'request':'EXIT'
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)
        return len(message)

