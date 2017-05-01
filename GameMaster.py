from TicTacToeGame import TicTacToeGame
from GameNode import GameNode
import json
class GameMaster():

    def __init__(self):
        self.playerList = {}
        self.playerNames = []
        self.gameList = {}
        self.gameOpen = None
        self.gameCount = 0
        self.gameHead = None

    def play(self, player):

        if self.gameOpen:
            self.gameList[self.gameOpen].addPlayer(s, )
            ret = 'Added to game ' + str(self.gameOpen)
            self.gameOpen = ''
            return ret
        else:
            game = TicTacToeGame(player)
            self.gameCount +=1
            self.gameOpen = self.gameCount
            self.gameList[self.gameOpen] = game
            self.gameList[self.gameOpen]
            return 'Please wait for another player to join'

    def login(self, client, address, name):

        for i in self.playerNames:
            if name ==  i:
                response = {'status':'OK', 'message':'Username already in use, pick again'}
                client.sendto(json.dumps(response).encode('utf-8'))
                return 'Username already in use'

        self.playerNames.append(name)
        self.playerList[name] = [client, address]


    def newGame(self):
        node = self.gameHead
        prevNode = None
        if node:
            prevNode = node
            node = node.getNext()
        else:
          #TODO: Fix for newgame/addgame
            node = GameNode()
            node.setGame(TicTacToeGame())

        while(node is not None):
            if node:
                prevNode = node
                node = node.getNext()
            else:
                node = GameNode()
                node.setP1(player)
                node.setGame(TicTacToeGame())
                prevNode.setNext(node)

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

