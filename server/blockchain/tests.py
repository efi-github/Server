from django.test import TestCase
import models

class SerializerTest(TestCase):
	def setUp(self):
		Block.objects.create(
			creatorID = "testID",
            objectID = "kasndf",
            objectType = "Hersteller",
            pfand = "5€",
            status = "In Benutzung",
            prevhash = "prevHash")
	def stringTest(self):
		block = Block.objects.get(objectID="kasndf")
		print(block)