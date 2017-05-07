class GameNode():
    def __init__(self, game):
        self.nex = None
        self.game = game
        self.id = game.getID()
        self.p1 = None
        self.p2 = None

    def next(self):
        return self.nex

    def setNext(self, next):
        self.nex = next

    def getGame(self):
        return self.game

    def getID(self):
        return self.id

    def getP1(self):
        return self.p1

    def getP2(self):
        return self.p2

    def setGame(self, game):
        self.game = game

    def addPlayer(self, player):
        print(player)
        if self.p1:
            self.p2 = player
        else:
            self.p1 = player

    def checkPlayers(self, player):
        print(self.p1)
        print(self.p2)
        if self.p1 == player:
            return True
        elif self.p2 == player:
            return True
        else:
            return False
