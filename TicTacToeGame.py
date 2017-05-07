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


    def endGame(self):
        self.gm.endGame(self)

    def comment(self, username, comment):
        fullComment = username + ': ' + comment
        message = {
            'status':'OK',
            'message': fullComment
        }
        self.sendToObservers(message)

    def sendToObservers(self, message):
        for user in self.observers:
            observer = self.observers[user]
            observer['client'].sendto(json.dumps(message).encode('utf-8'), observer['address'])

    def addObserver(self, client, address, username):
        if username in self.observers:
            observer = self.observers[username]
            response = {
                'status':'ERROR',
                'message':'You are already observing this game'
            }
            observer['client'].sendto(json.dumps(response).encode('utf-8'), observer['address'])
        else:
            self.observers[username] = {
                'client':client,
                'address':address
            }
            observer = self.observers[username]
            response = {
                'status':'ERROR',
                'message':'Successfuly added as observer to game ' + str(self.ID)
            }
            observer['client'].sendto(json.dumps(response).encode('utf-8'), observer['address'])

    def removeObserver(self, observerToRemove):
        if observerToRemove in self.observers:
            response = {
                'status':'OK',
                'message':'Removed from observing game ' + str(self.getID())
            }
            observer = self.observers[observerToRemove]
            observer['client'].sendto(json.dumps(response).encode('utf-8'), observer['address'])
            del self.observers[observerToRemove]

    # switches the turn value after a player has made a valid turn
    def switchTurn(self):
        if self.turn == self.playerOne:
            self.turn = self.playerTwo
        else:
            self.turn = self.playerOne

    # Returns the opposite player of the one who's turn it currently is
    def otherPlayer(self):
        if self.turn == self.playerOne:
            return self.playerTwo
        else:
            return self.playerOne

    # places a piece on the board with the currently turn's piece
    def place(self, move, player):
        print(player + "s turn")
        if self.turn['name'] == player:
            if self.board[int(move)-1] == '*':
                self.moves +=1
                self.board[int(move)-1] = self.turn['piece']
                board = self.displayBoard()
                if self.checkForWin():
                    message = {'status':'OK',
                               'message':self.turn['name'] + ' has won the game!\n\n' + board,
                               'board':self.board,
                               'command':'display'
                               }
                    self.turn['client'].sendto(json.dumps(message).encode('utf-8'), self.turn['address'])
                    self.switchTurn()
                    self.turn['client'].sendto(json.dumps(message).encode('utf-8'),self.turn['address'])
                    self.endGame()
                else:
                    message = {'status':'OK',
                               'message':self.turn['name'] + ' has made a move\n\n' + board,
                               'board':self.board,
                               'command':'display'
                               }
                    self.turn['client'].sendto(json.dumps(message).encode('utf-8'), self.turn['address'])
                    self.switchTurn()
                    self.turn['client'].sendto(json.dumps(message).encode('utf-8'),self.turn['address'])
                    self.sendToObservers(message)
            else:
                response = {
                    'status':'ERROR',
                    'message':'Piece already there, pick another move'
                }
                self.turn['client'].sendto(json.dumps(response).encode('utf-8'), self.turn['address'])

        else:
            other = self.otherPlayer()
            message = {'status':'WAIT',
                       'message':'Not your turn, please wait until other player goes',
                       'board':self.board
                       }
            other['client'].sendto(json.dumps(message).encode('utf-8'), other['address'])


    def changePlayer(self, newPiece):
        self.piece = newPiece

    # adds a player to the game
    def addPlayer(self, client, address, name):
        print("adding player")
        if not self.playerOne:
            self.playerOne['name'] = name
            self.playerOne['client'] = client
            self.playerOne['address'] = address
            self.playerOne['piece'] = 'X'
            message = {
                'status':'WAIT',
                'message': 'created Game, You are Player 1 with name ' + name +', and piece X.\n\n Now waiting for another player to join',
                'command':'wait'
            }
            self.playerOne['client'].sendto(json.dumps(message).encode('utf-8'), self.playerOne['address'])
        else:
            self.playerTwo['name'] = name
            self.playerTwo['client'] = client
            self.playerTwo['address'] = address
            self.playerTwo['piece'] = 'O'
            message1 = {
                'status':'WAIT',
                'message':'added to existing game as Player 2 with username ' + name+ ', and piece O. Player 1\'s turn',
                'command': None
            }
            self.playerTwo['client'].sendto(json.dumps(message1).encode('utf-8'), self.playerTwo['address'])
            message2 = {
                'status':'OK',
                'message':'Player 2 has joined, your turn',
                'command':None
            }
            # TODO: PROBEMS HERE
            if self.playerOne['client']:
                self.playerOne['client'].sendto(json.dumps(message2).encode('utf-8'), self.playerOne['address'])
        return

    # Displays the board for the user (not used on serverside, probably gunna remove this)
    def displayBoard(self):
        board = ''
        for p, i in enumerate(self.board):
            print(i + ' ', end='')
            board = board + i + ' '
            if (int(p)+1)%3 == 0:
                print('')
                board = board + '\n'
        return board

    # Checks if the player has won(need to add functionality to check whos turn it is)
    def checkForWin(self):

        if self.moves < 5:
            return False

        testBoard = [0,0,0,0,0,0,0,0,0]
        for p, i in enumerate(self.board):
                if i == self.turn['piece']:
                    testBoard[p] = self.magicBoard[p]

        total = 0
        for p, i in enumerate(self.winChecker):
            total = total + testBoard[i]

            if (int(p)+1)%3 == 0:
                if total == 15:
                    return True
                total = 0

        return False

    def isEqual(self, compare):

        if self.board == compare.getID():
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

    def getPlaterTwo(self):
        return self.playerTwo



