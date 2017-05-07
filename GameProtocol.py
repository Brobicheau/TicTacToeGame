import json


class GameProtocol():

    # intitialze the protocol object with information about the server,
    # and information about the user that is using it.
    def __init__(self, socket, address):
         self.server_address = address
         self.socket = socket
         self.auto_match = True

    # Call to login to the server
    def LOGIN(self, username):
        # Construct a message with the command, the username to login with,
        # and if the user wnats to be matched automatically
        message = {
            'request': 'LOGIN',
            'login': username,
            'automatch': self.auto_match
        }
        # send the message as a json object
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)

        # return the length of the message
        return len(message)


    def PLACE(self, move):
        message = {
            'request':'PLACE',
            'place': move
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)
        return len(message)

    def GAMES(self):
        message ={
            'request':'GAMES'
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

    def OBSERVE(self, id):
        message = {
            'request':'OBSERVE',
            'ID':id
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)

    def UNOBSERVE(self, id):
        message = {
            'request':'UNOBSERVE',
            'ID':id
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)

    def COMMENT(self, comment):
        message = {
            'request':'COMMENT',
            'comment':comment
        }
        self.socket.sendto(json.dumps(message).encode('utf-8'), self.server_address)

    # used for changing auto match preferences
    def automatch(self):

        # if auto matchis true, change it to false
        if self.auto_match:
            print('automatch off')
            self.auto_match = False
        # if its false, change it to true
        else:
            print('automatch on')
            self.auto_match = True
