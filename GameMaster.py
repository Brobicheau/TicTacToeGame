from TicTacToeGame import TicTacToeGame
from GameNode import GameNode
from GameList import GameList
import threading
import json
import time


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
        self.gameObserving = 3
        self.automatch = 4
        self.lock = threading.Lock()

    # -- endGame --
    # -----------------------------
    # This will end the game given as a parameter,
    # then either assign the players to a new game or set them as available
    # -----------------------------
    def endGame(self, gameToEnd):

        self.lock.acquire()
        try:
            # Get the node via the id of gameToEnd
            node = self.gameList.getGameWithID(gameToEnd.getID())

            # Get the players
            player1Name = node.getP1()
            player2Name = node.getP2()

            # Set their state to available
            player1 = self.playerList[player1Name]
            player1[self.status] = 'available'
            player2 = self.playerList[player2Name]
            player2[self.status] = 'available'

            # Remove the game and edit game counter
            self.gameCount -= 1
            if not self.gameList.removeGame(gameToEnd):
                print("couldnt delete game")
            self.lock.release()

            # if they are auto match players, assign them to new games
            if player1[self.automatch]:
                print('automatching player 1 again')
                self.autoPlay(player1Name)
            if player2[self.automatch]:
                self.autoPlay(player2Name)

        except:
            print ('couldnt delete game')

    # -- endFromDisconnect --
    # ------------------------
    # This will gracefully end the game of a user that has been dissconnected,
    # and either match the other user to a new game if they are automatched, or set them to available.
    # ------------------------
    def endFromDisconnect(self, disconnectedUser):

        self.lock.acquire()
        try:
            # Get the node of the game the dissconnected user was in
            node = self.gameList.getGameWithPlayer(disconnectedUser)

            # if we found one
            if node:

                # Grab the other player
                otherPlayer = node.getOtherPlayer(disconnectedUser)

            # otherwise just tell the other user there has been a problme and set them to available
            else: return
            if otherPlayer:
                playerToNotify = self.playerList[otherPlayer]
                playerToNotify[self.status] = 'available'
                message = {
                    'status':'OK',
                    'message': 'Other player disconnected, you have been changed to available'
                }
                playerToNotify[self.client].sendto(json.dumps(message).encode('utf-8'), playerToNotify[self.address])
            # Edit the game count and remove the game from the list
            self.gameCount -= 1
            self.gameList.removeGame(node.getGame())

            # then remove the user from both lists
            del self.playerList[disconnectedUser]
            self.playerNames.remove(disconnectedUser)

            # If theres a game open, and its the one we were just in, set game open to null
            if self.gameOpen:
                if self.gameOpen.getGame() is node.getGame():
                    self.gameOpen = None
        except KeyError:
            print('Couldnt find user in a game to delete')
        except ConnectionResetError:
            print('connection was reset')
        finally:
            self.lock.release()


    # -- autoPlay --
    # Username: username of the current user of are trying to start a game with
    # --Function--
    # This function will create a new game with a single player if there are none available
    # or it will add the player to a game with only one player in it.
    def autoPlay(self, username):
        self.lock.acquire()
        # If there is a game currently open for joining
        if self.gameOpen:

            # get the node and the game out of the node
            node = self.gameOpen
            game = node.getGame()

            # add the player to the node and the game for searching purposes
            node.addPlayer(username)
            game.addPlayer(self.playerList[username][self.client], self.playerList[username][self.address], username, True)
            self.playerList[username][self.status] = 'busy'
            # Make sure to set the game open to none
            self.gameOpen = None
            self.lock.release()


        # if there isnt a game currently open, make a new one!
        else:
            self.lock.release()
            # make the new node containing a new game
            newNode = self.newGame()
            self.lock.acquire()
            # make sure it worked
            if newNode:

                # get the game from the node
                newGame = newNode.getGame()

                # set the open game to the game we jsut created
                self.gameOpen = newNode

                # add the player to the game and the node
                newNode.addPlayer(username)
                newGame.addPlayer(self.playerList[username][self.client], self.playerList[username][self.address], username, True)
                self.playerList[username][self.status] = 'busy'
            self.lock.release()

    # --Login--
    # sets username if the username is not in use,
    #  we add it to the player list and set its status to available.
    # if automatch is on we set them up with a game. otherwise just return
    def login(self, client, address, username, automatch):

        self.lock.acquire()
        print('hello')
        # Loop through the list of players and check if the username is already in use
        for i in self.playerNames:
            if username ==  i:
                #If it is, let the user know
                response = {'status':'OK', 'message':'Username already in use, pick again'}
                client.sendto(json.dumps(response).encode('utf-8'), address)
                self.lock.release()
                return 'Username already in use'

        # Otherwise, the username is not in user

        # add the username to the playerlist
        self.playerNames.append(username)

        # save information about the client
        self.playerList[username] = ['available', client, address, '', automatch]

        # if the user wants to be matched automatically
        if automatch:
            # match them automatically
            self.lock.release()
            self.autoPlay(username)
        else:
            # otherwise return successful login response
            response = {'status': 'OK', 'message': 'Logged in'}
            client.sendto(json.dumps(response).encode('utf-8'), address)
            self.lock.release()


    # -- newGame --
    # -- Function --
    # This function will create a new game, then add it to the game list.
    # it will return the node received from adding the game to the list
    def newGame(self):
        self.lock.acquire()
        # make a new game with the game id of the current count
        game = TicTacToeGame(self.gameCount, self)

        # Increment the counter
        self.gameCount = self.gameCount + 1

        # add the new game to the list, which will place it in a node and return it
        node = self.gameList.addGame(game)

        # Return the node back to caller
        self.lock.release()
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
        self.lock.acquire()
        # Find the node with the player
        node = self.gameList.getGameWithPlayer(player)

        # if we found the node
        if node:
            # get the game and make the move
            self.lock.release()
            game = node.getGame()
            game.place(move, player)
        # otherwise we couldnt locate the game with the specified player
        else:
            # return an error message
            print('couldnt find player')
            self.lock.release()

    # - player --
    # askingPlayer: Player seeking to start a game with answeringPlayer
    # answeringPlayer: Player to start game with
    # -- Function --
    # This will find out if the answeringPlayer is available or not
    # if they are, it will start a game with both the players, with the
    # asking player being player 1. Otherwise it will return an error
    def play(self, askingPlayer, answeringPlayer):

        self.lock.acquire()
        # get the players from the player list
        player1 = self.playerList[askingPlayer]
        if askingPlayer in self.playerList and answeringPlayer in self.playerList:
            player2 = self.playerList[answeringPlayer]
        else:
            message = {
                'status':'ERROR',
                'message':'could not find matching player'
            }
            player1[self.client].sendto(json.dumps(message).encode('utf-8'), player1[self.address])

        # if the answeringPlayer is available
        if player2[self.status] == 'available':

            # Start a new game and add both players to it
            self.lock.release()
            newNode = self.newGame()
            self.lock.acquire()
            newNode.addPlayer(askingPlayer)
            newNode.getGame().addPlayer(player1[self.client], player1[self.address], askingPlayer, False)
            newNode.addPlayer(answeringPlayer)
            newNode.getGame().addPlayer(player2[self.client], player2[self.address], answeringPlayer, False)
            self.lock.release()

        # else if the player is busy, send an error message
        elif player2[self.status] == 'busy':
            message = {
                'status':'OK',
                'message':'player busy'
            }
            player1[self.client].sendto(json.dumps(message).encode('utf-8'), player1[self.address])
            self.lock.release()

        # Otherwise there is no specified player, so we send an error message
        else:
            message = {
                'status':'ERROR',
                'message':'player not found'
            }
            player1[self.client].sendto(json.dumps(message).encode('utf-8'), player1[self.address])
            self.lock.release()

    # -- exit --
    # ---------------------------------
    # This is called when the user wishes to exit the game.
    # it will remove them from all lists, as well as call end game
    # for the game they are in (if they are in one)
    # ---------------------------------
    def exit(self, usernameToExit):
        # Grab the player that is extiing
        self.lock.acquire()
        playerToExit = self.playerList[usernameToExit]
        otherPlayer = None
        #if playerToExit[self.status] == 'busy':
        # grab the game the exiting player is in
        node = self.gameList.getGameWithPlayer(usernameToExit)
        game = node.getGame()

        # and get the other user in that game
        otherUsername = game.getOtherPlayer(usernameToExit)
        otherUsername = otherUsername['name']
        otherPlayer = self.playerList[otherUsername]

        # end the game they are in
        self.lock.release()
        self.endGame(game)
        self.lock.acquire()

        # inform them they are exiting the game
        exitResponse = {
            'status':'KILL',
            'message':'Exiting from game'
        }
        response = {
            'status':'OK',
            'message':'Other player has quit game, changing status to available'
        }

        # if the other player exsists
        if otherPlayer:

            #inform them of the disconnect
            otherPlayer[self.client].sendto(json.dumps(response).encode('utf-8'), otherPlayer[self.address])

        # tell the player they are exiting, and then delete them from everything
        playerToExit[self.client].sendto(json.dumps(exitResponse).encode('utf-8'), playerToExit[self.address])
        playerToExit[self.client].close()
        del self.playerList[usernameToExit]
        self.lock.release()

    # -- listPlayers --
    # ---------------------------
    # this will get a list of all available players
    # ---------------------------
    def listPlayers(self, askingUsername):

        self.lock.acquire()

        # Create the base string
        list = 'here is the list of players currently available\n\n'

        # Grab every available player and concat them into the string
        for i in self.playerList:
            if self.playerList[i][self.status] == 'available':
                list = list + i + '\n'

        # Give the list to the user
        response = {
            'status':'OK',
            'message':list
        }
        askingPlayer = self.playerList[askingUsername]
        askingPlayer[self.client].sendto(json.dumps(response).encode('utf-8'), askingPlayer[self.address])
        self.lock.release()

    # -- listGames --
    # ---------------------
    # lists all the games currently being played
    # ---------------------
    def listGames(self, askingUsername):

        self.lock.acquire()

        # get the list from gamelist
        list = self.gameList.getList()

        # make base string for returning
        returnList = 'Here are all the currently active games:\n\n'

        # for every node in the list
        for node in list:

            # concat next game onto the string
            returnList = returnList + 'ID: ' + str(node.getGame().getID())

            # check which player are in the game, and put them in as well.
            returnList = returnList + ', Player(s): ' + node.getP1()
            if node.getP2():
                returnList = returnList + ', ' + node.getP2()
            returnList = returnList + '\n\n'

        # send the list to the calling user
        response = {
            'status':'OK',
            'message': returnList
        }
        print (returnList)
        player = self.playerList[askingUsername]
        player[self.client].sendto(json.dumps(response).encode('utf-8'), player[self.address])
        self.lock.release()


    # -- addObserver --
    # ----------------------
    # this will add an observer onto the list of observers
    # and then add them into the game
    # ----------------------
    def addObserver(self, ID, client, address, username):

        self.lock.acquire()

        # grab the ndoe with the given is for observing
        node = self.gameList.getGameWithID(ID)

        # grab the user from the userlist
        user = self.playerList[username]

        # if the node is there
        if node:

            # add the observer to the game
            game = node.getGame()
            game.addObserver(client, address, username)
            user[self.gameObserving] = game.getID()

        else:
            # otherwise return an error message to the user
            response = {
                'status':'ERROR',
                'message':'Couldnt find game with ID ' + ID
            }
            user[self.client].sendto(json.dumps(response).encode('utf-8'), user[self.address])
        self.lock.release()

    # -- removeObserver --
    # ------------------------
    # this function will remove an observer from the list,
    # Then remove them from the game.
    # ------------------------
    def removeObserver(self, ID, username):

        self.lock.acquire()

        # Grab the node
        node = self.gameList.getGameWithID(ID)

        # Grab the user
        user = self.playerList[username]

        # take the user out of the list
        user[self.gameObserving] = ''

        # Get the game and remove the user from the observer list
        game = node.getGame()
        game.removeObserver(username)
        self.lock.release()

    # -- comment --
    # --------------------
    # sends the users comment to the game so it can be sent to all users observing
    # --------------------
    def comment(self, username ,comment):

        self.lock.acquire()

        # get the user making the comment
        player = self.playerList[username]

        # get the game the user is observing
        gameID = player[self.gameObserving]

        # grab the game from the list
        node = self.gameList.getGameWithID(gameID)
        game = node.getGame()

        # add the comment
        game.comment(username, comment)
        self.lock.release()