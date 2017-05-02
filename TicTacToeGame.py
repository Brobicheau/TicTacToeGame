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
    def __init__(self, client, address, name):
        self.board = makeNewBoard()
        self.magicBoard = makeMagicBoard()
        self.winChecker = makeWinChecker()
        self.moves = 0
        self.playerOne = None#{'name':name, 'client':client,'address':address, 'piece':'X'}
        self.playerTwo = None  # {}
        self.turn = self.playerOne
        message = {
            'message':'Waiting for another player',
            'status': 'OK'
        }
        self.playerOne['client'].sendto(json.dumps(message).encode('utf-8'), self.playerOne['address'])



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
    def place(self, position, name, client):
        if self.turn['name'] == name:
            self.moves +=1
            self.board[int(position)-1] = self.piece
            message = {'status':'OK',
                       'message':self.turn['name'] + ' has made a move',
                       'board':self.board
                       }
            self.turn['client'].sendto(json.dumps(message).encode('utf-8'))
            self.switchTurn()
            self.turn['client'].sendto(json.dumps(message).encode('utf-8'))
        else:
            player = self.otherPlayer(self.turn)
            message = {'status':'OK',
                       'message':'Not your turn, please wait until other player goes',
                       'board':self.board
                       }
            player['client'].sendto(json.dumps(message).encode('utf-8'))


    def changePlayer(self, newPiece):
        self.piece = newPiece

    # adds a player to the game
    def addPlayer(self, client, address, name):

        if self.playerOne == None:
            self.playerOne['name'] = name
            self.playerOne['client'] = client
            self.playerOne['address'] = address
            self.playerOne['piece'] = 'X'
        else:
            self.playerTwo['name'] = name
            self.playerTwo['client'] = client
            self.playerTwo['address'] = address
            self.playerTwo['piece'] = 'O'
        return

    # Displays the board for the user (not used on serverside, probably gunna remove this)
    def displayBoard(self):
        for p, i in enumerate(self.board):
            print(i + ' ', end='')
            if (int(p)+1)%3 == 0:
                print('')

    # Checks if the player has won(need to add functionality to check whos turn it is)
    def checkForWin(self):

        if self.moves < 5:
            return False

        testBoard = [0,0,0,0,0,0,0,0,0]
        for p, i in enumerate(self.board):
                if i == self.piece:
                    testBoard[p] = self.magicBoard[p]

        total = 0
        for p, i in enumerate(self.winChecker):
            total = total + testBoard[i]

            if (int(p)+1)%3 == 0:
                if total == 15:
                    return True
                total = 0

        return False






