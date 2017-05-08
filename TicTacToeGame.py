import json

# Makes a blank board for a new game
def makeNewBoard():
    return ['*', '*', '*', '*', '*', '*', '*', '*', '*']

# Creates a "magic board" which we use to calculate if a player has one.
# With these set of numbers, if you add up any row/column/diagnal the sum will be 15,
# so the first player whos pieces make a sum of 15 will win
def makeMagicBoard():
    return [8, 1, 6, 3, 5, 7, 4, 9, 2]

# This is the values we use to sum up the values of the players. It is just the indexes of
# Each possible row/column/diagnal
def makeWinChecker():
    return[0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 3, 6, 1, 4, 7, 2, 5, 8, 0, 4, 8, 2, 4, 7]

#Main Class
class TicTacToeGame():

    # Initiates base values for game (no player is needed to create game)
    #   board: The board of the game (array)
    #   magicBoard: board used to help sum up players board to check for win
    #   winChecker: used to check all rows/columns/diagnals
    #   moves: Counter for how many moves the players have made
    #   playerOne: First player to join the game, has the 'X' piece, also goes first
    #   playerTwo: Second player to join the game, has the 'O' piece, goes second
    #   turn: A valuet that holds the player whos turn it currently is
    def __init__(self, id, GameMaster):
        self.board = makeNewBoard()
        self.magicBoard = makeMagicBoard()
        self.winChecker = makeWinChecker()
        self.moves = 0
        self.playerOne = {}#{'name':name, 'client':client,'address':address, 'piece':'X'}
        self.playerTwo = {}  # {}
        self.ID = id
        self.turn = self.playerOne
        self.gm = GameMaster
        self.observers = {}

    # This for is internal problems in the TicTacToe game. It will call this when it needs to terminate.
    # Calls the game masster to do cleanup
    def endGame(self):
        self.gm.endGame(self)

    # sends a comment from one observer to al the observers in the list
    def comment(self, username, comment):

        # construct then send comment to all observers in list
        fullComment = username + ': ' + comment
        message = {
            'status':'OK',
            'message': fullComment
        }
        self.sendToObservers(message)


    # sends given message to all observers in the observer list
    def sendToObservers(self, message):

        # For every observer in the list
        for user in self.observers:

            # send them the pre constructed message
            observer = self.observers[user]
            observer['client'].sendto(json.dumps(message).encode('utf-8'), observer['address'])

    # adds an observer to the list of observers
    def addObserver(self, client, address, username):

        # If the user is already an observer
        if username in self.observers:

            # Return an error message
            observer = self.observers[username]
            response = {
                'status':'ERROR',
                'message':'You are already observing this game'
            }
            observer['client'].sendto(json.dumps(response).encode('utf-8'), observer['address'])

        # Otherwise add them to the list
        else:
            self.observers[username] = {
                'client':client,
                'address':address
            }
            observer = self.observers[username]
            response = {
                'status':'OK',
                'message':'Successfuly added as observer to game ' + str(self.ID)
            }
            observer['client'].sendto(json.dumps(response).encode('utf-8'), observer['address'])


    # This removes an observer from the observer list
    def removeObserver(self, observerToRemove):

        # If the observer is in the observer list
        if observerToRemove in self.observers:

            # remove them and send a confirmation message
            response = {
                'status':'OK',
                'message':'Removed from observing game ' + str(self.getID())
            }
            observer = self.observers[observerToRemove]
            observer['client'].sendto(json.dumps(response).encode('utf-8'), observer['address'])
            del self.observers[observerToRemove]
        # Otherwise do nothing

    # switches the turn value after a player has made a valid turn
    def switchTurn(self):
        # If the user is player 1, change turn to player 2, othewise change turn to player 1
        if self.turn == self.playerOne:
            self.turn = self.playerTwo
        else:
            self.turn = self.playerOne

    # Returns the opposite player of the one who's turn it currently is
    def otherPlayer(self):

        # If the user is player 1, return player 2, othewise return player 1
        if self.turn == self.playerOne:
            return self.playerTwo
        else:
            return self.playerOne

    # -- place --
    # -------------------------
    # places a piece on the board with the currently turn's piece
    # -------------------------
    def place(self, move, player):
        # If it is the players turn
        if self.turn['name'] == player:
            if int(move) < 1 or int(move)  > 9:
                message = {
                    'status':'ERROR',
                    'message':'Not a valid move, please try again'
                }
                self.turn['client'].sendto(json.dumps(message).encode('utf-8'), self.turn['address'])
            else:

                # If the chosen move does not already have a piece on it
                if self.board[int(move)-1] == '*':

                    # increment the moves count
                    self.moves +=1

                    # place the piece on the board
                    self.board[int(move)-1] = self.turn['piece']

                    # Construct the board with new piece on it
                    board = self.displayBoard()

                    # And check to see if the user has won
                    if self.checkForWin():

                        # If the user has one, send both users a message saying who won the game and the state of the board when they won,
                        #  then tell the game master the game is over
                        message = {'status':'OK',
                                   'message':self.turn['name'] + ' has won the game!\n\n' + board,
                                   'board':self.board,
                                   'command':'display'
                                   }
                        self.turn['client'].sendto(json.dumps(message).encode('utf-8'), self.turn['address'])
                        # Switch the players turn to send message
                        self.switchTurn()
                        self.turn['client'].sendto(json.dumps(message).encode('utf-8'),self.turn['address'])
                        self.endGame()

                    # Otherwise, if the user hasnt won
                    else:

                        # send both the users a message with the updated board, and instructing them on who goes next
                        message = {'status':'OK',
                                   'message':self.turn['name'] + ' has made a move\n\n' + board,
                                   'board':self.board,
                                   'command':'display'
                                   }
                        self.turn['client'].sendto(json.dumps(message).encode('utf-8'), self.turn['address'])
                        # switch the players turn to send message and prepare game for next move
                        self.switchTurn()
                        self.turn['client'].sendto(json.dumps(message).encode('utf-8'),self.turn['address'])
                        self.sendToObservers(message)
                # If there was already a piece in the chosen move spot
                else:
                    # Return an error message asking them to pick again. Dont change the turn
                    response = {
                        'status':'ERROR',
                        'message':'Piece already there, pick another move'
                    }
                    self.turn['client'].sendto(json.dumps(response).encode('utf-8'), self.turn['address'])

        else:
            # the request didnt come from the player whos turn it is. Let them know
            other = self.otherPlayer()
            message = {'status':'ERROR',
                       'message':'Not your turn, please wait until other player goes',
                       'board':self.board
                       }
            other['client'].sendto(json.dumps(message).encode('utf-8'), other['address'])

    # Changes the piece the player is using (not used)
    def changePlayer(self, newPiece):
        self.piece = newPiece

    # -- addPlayer --
    # -------------------------------
    # adds a player to the game
    # -------------------------------
    def addPlayer(self, client, address, name, automatch):

        # If there isnt a player 1 yet
        if not self.playerOne:

            # Add player 1 to the game and instruct them to wait for next player
            self.playerOne['name'] = name
            self.playerOne['client'] = client
            self.playerOne['address'] = address
            self.playerOne['piece'] = 'X'
            if automatch:
                message = {
                    'status':'OK',
                    'message': 'created Game, You are Player 1 with name ' + name +', and piece X.\n\n Now waiting for another player to join',
                    'command':'wait'
                }
                self.playerOne['client'].sendto(json.dumps(message).encode('utf-8'), self.playerOne['address'])

        # else the player we are trying to add is player 2
        else:

            # Add them to he game and instruct them to wait for player 1 to go.
            # Then inform player 1 that a second player as joined, and instruct them to make a move.
            self.playerTwo['name'] = name
            self.playerTwo['client'] = client
            self.playerTwo['address'] = address
            self.playerTwo['piece'] = 'O'
            if automatch:
                message1 = {
                    'status':'OK',
                    'message':'added to a game by request as Player 2 with username ' + name+ ', and piece O. Player 1\'s turn',
                    'command': None
                }
                self.playerTwo['client'].sendto(json.dumps(message1).encode('utf-8'), self.playerTwo['address'])
                message2 = {
                    'status':'OK',
                    'message':'Player 2 has joined, your turn',
                    'command':None
                }
                # Check if client hasnt been removed
                self.playerOne['client'].sendto(json.dumps(message2).encode('utf-8'), self.playerOne['address'])
            else:
                message1 = {
                    'status':'OK',
                    'message':'added to existing game as Player 2 with username ' + name+ ', and piece O. Player 1\'s turn',
                    'command': None
                }
                self.playerTwo['client'].sendto(json.dumps(message1).encode('utf-8'), self.playerTwo['address'])
                message2 = {
                    'status':'OK',
                    'message':'Player 2 has joined, your turn',
                    'command':None
                }
                # Check if client hasnt been removed
                self.playerOne['client'].sendto(json.dumps(message2).encode('utf-8'), self.playerOne['address'])
        return

    # constructs the board to display to the user. Also displays it on server prompt
    def displayBoard(self):

        # make a board variable
        board = ''

        # for each element in the board array
        for p, i in enumerate(self.board):

            # Add it to the board variable
            print(i + ' ', end='')
            board = board + i + ' '

            # if its divisble by 3, weve hit the end of the row, make row.
            if (int(p)+1)%3 == 0:
                print('')
                board = board + '\n'

        # Return the newly constructed board
        return board

    # -- checkForWin --
    # ---------------------------------------
    # Checks if the player has won
    # ---------------------------------------
    def checkForWin(self):

        # minimum amount of moves to win. Return False if it hasnt hit there yet
        if self.moves < 5:
            return False

        # create a blank testing boad
        testBoard = [15,15,15,15,15,15,15,15,15]

        # add a number from a mirrored position on the magic board,
        # that contains a piece of the current players turn
        for p, i in enumerate(self.board):
                if i == self.turn['piece']:
                    testBoard[p] = self.magicBoard[p]

        # Make a total variable
        total = 0

        # Use the winChecker to test the correct pattern of elemetns for
        # any win case in tictac toe
        for p, i in enumerate(self.winChecker):
            total = total + testBoard[i]
            print(testBoard[i])

            # If were done checking a single win  pattern
            if (int(p)+1)%3 == 0:
                print('')
                #  and if the sum is equal to 15, its a win, return true
                if total == 15:
                    return True

                # reset total in preperation to loop again
                total = 0
        # otherwise there is not win yet
        return False

    # -- isEqual --
    # -----------------------
    # Checks to see if the given game and this one are the same. Checks via gameid
    def isEqual(self, compare):

        if self.ID == compare.getID():
            return True
        else:
            return False


    def getID(self):
        return self.ID


    def getPlayer(self, playerToGet):
        if playerToGet == self.playerOne['name']:
            return self.playerOne
        elif playerToGet == self.playerTwo['name']:
            return self.playerTwo
        else:
            return False

    def getOtherPlayer(self, oppositePlayer):
        if oppositePlayer == self.playerOne['name']:
            return self.playerTwo
        elif oppositePlayer == self.playerTwo['name']:
            return self.playerOne
        else:
            return False

    def getPlayerOne(self):
        return self.playerOne

    def getPlayerTwo(self):
        return self.playerTwo



