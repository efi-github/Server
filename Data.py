from uuid import uuid4

# The Data ~~~ Normal!? ~~~
class Data:
    def __init__(self, creatorID, objectType, status):
        self.creatorID = creatorID
        self.objectID = uuid.uuid4()
        self.objectType = objectType
        self.pfand = 12
        self.status = status

    def __str__(self):
        return str(self.creatorID) + str(self.objectID) + str(self.objectType) + \
               str(self.pfand) + str(self.status) + str(self.prevhash)
