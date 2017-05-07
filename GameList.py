from GameNode import GameNode


# This class is used to store the entire linked list of games for GameMaster
class GameList():

    # -- Init --
    # Head: head of the linked list of games
    # Tail: last added game in list
    def __init__(self):
        self.head = None
        self.tail = None

    # -- getList --
    # ---------------
    # This function will iterate through the list,
    # appending it to an array, and then return that array to the caller
    # ----------------
    def getList(self):
        node = self.head
        list = []
        while node:
            list.append(node)
            node = node.next()
        return list

    # -- getGameWithPlayer --
    # ---------------------------
    # This function will iterate through the list and return the first instance
    # of a game with the given player
    # ---------------------------
    def getGameWithPlayer(self, player):

        node = self.head
        prev = None

        while node:
            if node.checkPlayers(player):
                return node
            else:
                prev = node
                print(node.next())
                node = node.next()
        return None

    # -- getGameWithID --
    # ----------------------------
    # This will iterate through the list and return the first node
    # with the given ID
    # ----------------------------
    def getGameWithID(self, ID):
        node = self.head
        prev = None

        while node:
            if int(node.getID()) == int(ID):
                return node
            else:
                prev = node
                node = node.next()
        return None

    # -- addGame --
    # ---------------------
    # this function will add a new game into the list
    # ---------------------
    def addGame(self, game):

        if self.head is None:
            node = GameNode(game)
            self.head = node
            self.tail = node
        else:
            node = GameNode(game)
            self.tail.setNext(node)
            self.tail = node

        return node



    # -- removeGame--
    # ---------------------
    # this function will iterate through the list and remove the game
    # that matches the one given
    # ---------------------
    def removeGame(self, game):
        found = False
        node = self.head
        prev = None
        while node:
            if node.getGame().isEqual(game):
                if prev:
                    prev.setNext(node.next())
                    if self.tail.isEqual(game):
                        self.tail = prev
                    return True
                else:
                    self.head = None
                    self.tail = None
                    return True
            else:
                prev = node
                node = node.next()
        return False