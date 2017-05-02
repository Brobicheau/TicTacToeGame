from TicTacToeGame import TicTacToeGame
from GameNode import GameNode
import json


class GameMaster():

    def __init__(self):
        # List of players and info about them. Structure is [status, client, address]
        self.playerList = {}
        self.playerNames = []
        self.gameList = {}
        self.gameOpen = None
        self.gameCount = 0
        self.gameHead = None
        self.status = 0
        self.client = 1
        self.address = 2

    def autoPlay(self, username):

        if self.gameOpen:
            self.gameList[self.gameOpen].addPlayer(self.playerList[username][self.client], self.playerList[username][self.address], username )
            ret = 'Added to game ' + str(self.gameOpen)
            self.gameOpen = ''
            return ret
        else:
            newGame = self.newGame()
            if newGame:
                newGame.addPlayer(self.playerList[username][self.client], self.playerList[username][self.address], username)

            # game = TicTacToeGame(self.playerList[username][self.client], self.playerList[username][self.address], username)
            # self.gameCount +=1
            # self.gameOpen = self.gameCount
            # self.gameList[self.gameOpen] = game
            # return 'Please wait for another player to join'

    def play(self):



    # --Login--
    # sets username if the username is not in use,
    #  we add it to the player list and set its status to available.
    # if automatch is on we set them up with a game. otherwise just return
    def login(self, client, address, username, automatch):
        # TODO: Check for duplicate client/addresses so username is changed
        # Loop through the list of players and check if the username is already in use
        for i in self.playerNames:
            if username ==  i:
                #If it is, let the user know
                response = {'status':'OK', 'message':'Username already in use, pick again'}
                client.sendto(json.dumps(response).encode('utf-8'), address)
                return 'Username already in use'

        # Otherwise, the username is not in user

        # add the username to the playerlist
        self.playerNames.append(username)

        # save information about the client
        self.playerList[username] = [True, client, address]

        # if the user wants to be matched automatically
        if automatch:
            # match them automatically
            self.autoPlay(username)
        else:
            # otherwise return successful login response
            response = {'status': 'OK', 'message': 'Logged in'}
            client.sendto(json.dumps(response).encode('utf-8'), address)

    def newGame(self):
        # Get the head of the game list (Singly Linked List)
        node = self.gameHead

        # Set the previous node of the list to start as null
        prevNode = None

        # If the current node is not null
        if node:

            # set the current node to the prev and get next node
            prevNode = node
            node = node.getNext()
        else:
            # otherwise we are at the end of the list, and we can create new game.
            # TODO: Fix for newgame/addgame
            node = GameNode()
            node.setGame(TicTacToeGame())
            self.gameOpen = node.getGame()
            prevNode.setNext(node)
            return node

        # Repeat in loop
        while(node is not None):
            if node:
                prevNode = node
                node = node.getNext()
            else:
                node = GameNode()
                node.setGame(TicTacToeGame())
                self.gameOpen = node.getGame()
                prevNode.setNext(node)
                return node
        return

    def place(self, move, player, client):
        node = self.gameHead
        if node.checkPlayers(player):
            node.getGame().updateBoard(move, player, client)
            node = None
        else:
            node = node.getNext()

        while(node is not None):
            if node.checkPlayers(player):
                node.getGame().place(move, player)
                node = None
            else:
                node = node.getNext()

