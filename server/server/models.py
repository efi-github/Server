# The Data ~~~ Normal!? ~~~
from django.db import models

class Data(models.Model):
    creatorID = models.CharField(max_length=100)
    objectID = models.CharField(max_length=100)
    objectType = models.CharField(max_length=100)
    pfand = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    prevhash = models.CharField(max_length=100)
    
    def __str__(self):
        return hash(str(self.creatorID) + str(self.objectID) + str(self.objectType) + \
               str(self.pfand) + str(self.status) + str(self.date) + str(self.prevhash))