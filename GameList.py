from GameNode import GameNode

class GameList():

    def __init__(self):
        self.head = None

    def getList(self):
        node = self.head
        list = []
        while node:
            list.append(node)
            node = node.next()
        return list


    def getGameWithPlayer(self, player):

        node = self.head
        prev = None
        print(self.head)
        print('THESE ARE THE HEAD')
        print(node)

        while node:
            if node.checkPlayers(player):
                return node
            else:
                prev = node
                print(node.next())
                node = node.next()
        return None

    def getGameWithID(self, ID):
        node = self.head
        prev = None

        while node:
            if node.getID() == ID:
                return node
            else:
                prev = node
                node = node.next()
        return None

    def addGame(self, game):
        node = self.head
        prev = None

        while node is not None:
            prev = node
            print (node)
            node = node.next()
        node = GameNode(game)
        if self.head is None:
            self.head = node
        if prev:
            prev.setNext(node)
        return node




    def removeGame(self, game):
        found = False
        node = self.head
        prev = None
        while node:
            if node.getGame.isEqual(game):
                if prev:
                    prev.setNext(node.next())
                    return True
                else:
                    self.head = None
                    return True
            else:
                prev = node
                node = node.next()
        return False