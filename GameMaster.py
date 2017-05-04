from TicTacToeGame import TicTacToeGame
from GameNode import GameNode
from GameList import GameList
import threading
import json


class GameMaster():
    # playerlist: list containing the players username, client, address, and status
    # playerNames: list of players names
    # gammeList: linked list of all the games currently in progress
    # gameOpen: holds currently available game if there are any
    # gameCount: Counter for how many games are in progress
    # status: num for accessing status filed in playlist array
    # client: num for accessing clietn field in the playerlist array
    # address: num for accessing addres field in the playerlist array
    # lock: lock used for shared data
    def __init__(self):
        # List of players and info about them. Structure is [status, client, address]
        self.playerList = {}
        self.playerNames = []
        self.gameList = GameList()
        self.gameOpen = None
        self.gameCount = 0
        self.status = 0
        self.client = 1
        self.address = 2
        self.lock = threading.Lock()

    def endGame(self, gameToEnd):

        # Do stuff under here
        self.lock.acquire()
        try:
            node = self.gameList.getGameWithID(gameToEnd.getID())
            player1Name = node.getP1()
            player2Name = node.getP2()
            player1 = self.playerList[player1Name]
            player1[self.status] = 'available'
            player2 = self.playerList[player2Name]
            player2[self.status] = 'available'
            self.gameCount -= 1
            self.gameList.removeGame(gameToEnd)
        except:
            print ('couldnt delete game')
        self.lock.release()

    def endFromDisconnect(self, disconnectedUser):

        try:
            node = self.gameList.getGameWithPlayer(disconnectedUser)
            nameToNotify = node.getP1()
            if nameToNotify is disconnectedUser:
                nameToNotify = node.getP2()
            playerToNotify = self.playerList[nameToNotify]
            playerToNotify[self.status] = 'available'
            message = {
                'status':'OK',
                'message': 'Other player disconnected, you have been changed to available'
            }
            playerToNotify['client'].sendto(json.dumps(message).encode('utf-8'), playerToNotify['address'])
            self.gameCount -= 1
            self.gameList.removeGame(node.getGame())
        except:
            print('couldnt delete disconnected game')

    # -- autoPlay --
    # Username: username of the current user of are trying to start a game with
    # --Function--
    # This function will create a new game with a single player if there are none available
    # or it will add the player to a game with only one player in it.
    def autoPlay(self, username):

        # If there is a game currently open for joining
        if self.gameOpen:

            # get the node and the game out of the node
            node = self.gameOpen
            game = node.getGame()

            # add the player to the node and the game for searching purposes
            node.addPlayer(username)
            game.addPlayer(self.playerList[username][self.client], self.playerList[username][self.address], username)

            # Make sure to set the game open to none
            self.gameOpen = None

        # if there isnt a game currently open, make a new one!
        else:

            # make the new node containing a new game
            newNode = self.newGame()

            # make sure it worked
            if newNode:

                # get the game from the node
                newGame = newNode.getGame()

                # set the open game to the game we jsut created
                self.gameOpen = newNode

                # add the player to the game and the node
                newNode.addPlayer(username)
                newGame.addPlayer(self.playerList[username][self.client], self.playerList[username][self.address], username)


    # --Login--
    # sets username if the username is not in use,
    #  we add it to the player list and set its status to available.
    # if automatch is on we set them up with a game. otherwise just return
    def login(self, client, address, username, automatch):
        print('in login')
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


    # -- newGame --
    # -- Function --
    # This function will create a new game, then add it to the game list.
    # it will return the node received from adding the game to the list
    def newGame(self):

        # make a new game with the game id of the current count
        game = TicTacToeGame(self.gameCount, self)

        # Increment the counter
        self.gameCount = self.gameCount + 1

        # add the new game to the list, which will place it in a node and return it
        node = self.gameList.addGame(game)

        # Return the node back to caller
        return node


    # -- place --
    # -- Function--
    # move; The move to make
    # player: The player that is making the move
    # -- Function --
    # This will get the game based on the player making the move. If it finds the
    # game with the player, it will try to call place on the game with the move
    # otherwise it will return that it could not find an error
    def place(self, move, player):

        # Find the node with the player
        node = self.gameList.getGameWithPlayer(player)

        # if we found the node
        if node:
            # get the game and make the move
            game = node.getGame()
            game.place(move, player)
        # otherwise we couldnt locate the game with the specified player
        else:
            # return an error message
            print('couldnt find player')

    # - player --
    # askingPlayer: Player seeking to start a game with answeringPlayer
    # answeringPlayer: Player to start game with
    # -- Function --
    # This will find out if the answeringPlayer is available or not
    # if they are, it will start a game with both the players, with the
    # asking player being player 1. Otherwise it will return an error
    def play(self, askingPlayer, answeringPlayer):
        # TODO: Check if the players are actually in the list first
        # get the players from the player list
        player1 = self.playerlist[askingPlayer]
        player2 = self.playerlist[answeringPlayer]

        # if the answeringPlayer is available
        if player2[self.status] == 'available':

            # Start a new game and add both players to it
            newNode = self.newGame()
            newNode.addPlayer(askingPlayer)
            newNode.getgame().addPlayer(player1['client'], player1['address'], askingPlayer)
            newNode.addPlayer(answeringPlayer)
            newNode.getgame().addPlayer(player2['client'], player2['address'], answeringPlayer)

        # else if the player is busy, send an error message
        elif player2[self.status] == 'busy':
            message = {
                'stauts':'OK',
                'message':'player busy'
            }
            player1['client'].sendto(json.dumps(message).encode('utf-8'), player1['address'])

        # Otherwise there is no specified player, so we sned an error message
        else:
            message = {
                'stauts':'OK',
                'message':'player not found'
            }
            player1['client'].sendto(json.dumps(message).encode('utf-8'), player1['address'])