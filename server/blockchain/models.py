from django.db import models

class Block(models.Model):
    creatorID = models.CharField(max_length=100)
    objectID = models.CharField(max_length=100)
    objectType = models.CharField(max_length=100)
    pfand = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    prevhash = models.CharField(max_length=100)

class Key(models.Model):
    creatorID = models.CharField(max_length=100)
    key = models.CharField(max_length=500)
    type = models.CharField(max_length = 100)
