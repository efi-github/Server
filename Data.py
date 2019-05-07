# The Data ~~~ Normal!? ~~~
class Data:
    def __init__(self, creatorID, objectID, objectType, pfand, status, prevhash):
        self.creatorID = creatorID
        self.objectID = objectID
        self.objectType = objectType
        self.pfand = pfand
        self.status = status
        self.prevhash = prevhash

    def __str__(self):
        return str(self.creatorID) + str(self.objectID) + str(self.objectType) + \
               str(self.pfand) + str(self.status) + str(self.prevhash)
