class GameNode():
    def __init__(self):
        self.next = None
        self.game = None
        self.p1 = None
        self.p2 = None

    def getNext(self):
        return self.next

    def setNext(self, next):
        self.next = next

    def getGame(self):
        return self.game

    def getP1(self):
        return self.p1

    def getP2(self):
        return self.p2

    def setGame(self, game):
        self.game = game

    def checkPlayers(self, player):

        if self.p1 == player:
            return True
        elif self.p2 == player:
            return True
        else:
            return False
