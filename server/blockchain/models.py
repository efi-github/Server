from django.db import models


#Die Blockchain Datenbank, welche alle Blöcke beinhaltet
class Block(models.Model):
	creatorID = models.CharField(max_length=100)
	objectID = models.CharField(max_length=100)
	objectType = models.CharField(max_length=100)
	pfand = models.CharField(max_length=100)
	status = models.CharField(max_length=100)
	prevhash = models.CharField(max_length=200)
	hash = models.CharField(max_length=200)

#	def __str__(self):
#		return str(BlockSerializer(self, many=False).data)

#Die Key Datenbank, die die Hersteller und Verschrotter Keys speichert
class Key(models.Model):
	creatorID = models.CharField(max_length=100)
	key = models.CharField(max_length=500)
	type = models.CharField(max_length = 100)
