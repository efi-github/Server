from django.test import RequestFactory, TestCase
from .models import *
from .serializers import *
from .views import BlockView
import json
import rsa
from rest_framework.renderers import JSONRenderer

class SerializerTest(TestCase):
	def setUp(self):
		self.creatorID = "80e75ded-6793-4f29-bb90-c984bf8874b3"
		self.verschrotterID = "8aeb900e-80cd-4240-9823-d6d757161f4c"
		self.pubkey = rsa.PublicKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537)
		self.privkey = rsa.PrivateKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537, 2610569376032565956309174622037664216017335124208227255278187302182857934127620588652325851492936605352779514612193161739271679676319086770723600501383313, 5423127635530564405310435204517160683830388719985322756621937065802093201396704811, 1242634711636051238726630576667870429726659551427143718832064794022377887)
		Block.objects.create(
			creatorID = "testID",
			objectID = "kasndf",
            objectType = "Hersteller",
            pfand = "5€",
            status = False,
            prevhash = "prevHash",
			hash = "hash")
		Key.objects.create(
			creatorID = "80e75ded-6793-4f29-bb90-c984bf8874b3",
			key = "6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357",
			type = "Hersteller"
		)
		Key.objects.create(
			creatorID = "8aeb900e-80cd-4240-9823-d6d757161f4c",
			key = "6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357",
			type = "Recycler"
		)
		self.factory = RequestFactory()

	def test_getuuid(self):
		print("::::TEST GET UUID::::")
		request = self.factory.get("block/kasndf/")
		response = BlockView.as_view()(request, '0')
		print(response)
		print(response.data)
		self.assertEqual(response.status_code, 200)


	def test_getblock(self):
		print("::::TEST GET BLOCK::::")
		request = self.factory.get("block/")
		response = BlockView.as_view()(request)
		print(response)
		print(response.data)
		self.assertEqual(response.status_code, 200)


	def test_createObject(self):
		print("::::TEST CREATE OBJECT::::")
		new_block = {'creatorID':self.creatorID, 'objectType':'iphone', 'pfand':'55', 'status':False}
		body = json.dumps(new_block)
		request = self.factory.post("block/", body, content_type='application/json')
		response = BlockView.as_view()(request)
		block = json.loads(response.data)
		signature = rsa.sign(response.data, self.privkey, 'SHA-256')
		block["hash"] = signature.hex()
		body = json.dumps(block, separators=(',', ':'))
		request = self.factory.post("block/", body, content_type='application/json')
		response = BlockView.as_view()(request)
		print(response)
		print(response.data)
		self.assertEqual(JSONRenderer().render(BlockSerializer(Block.objects.latest("id")).data), response.data)
		self.assertEqual(response.status_code, 200)



	def test_destroyObject(self):
		print("::::TEST DESTROY OBJECT::::")
		del_block = {'recyclerID':self.verschrotterID, "objectID":"kasndf"}
		body = json.dumps(del_block)
		request = self.factory.post("block/", body, content_type='application/json')
		response = BlockView.as_view()(request)
		block = json.loads(response.data)
		signature = rsa.sign(response.data, self.privkey, 'SHA-256')
		block["hash"] = signature.hex()
		del block["creatorID"]
		block["recyclerID"] = self.verschrotterID
		body = json.dumps(block, separators=(',', ':'))
		request = self.factory.post("block/", body, content_type='application/json')
		response = BlockView.as_view()(request)
		print(response)
		print(response.data)
		self.assertEqual(JSONRenderer().render(BlockSerializer(Block.objects.latest("id")).data), response.data)
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		print("::::TEST PUT::::")
		del_block = {'recyclerID':self.verschrotterID, "objectID":"kasndf"}
		body = json.dumps(del_block)
		request = self.factory.put("block/", body, content_type='application/json')
		response = BlockView.as_view()(request)
		block = json.loads(response.data)
		signature = rsa.sign(response.data, self.privkey, 'SHA-256')
		block["hash"] = signature.hex()
		del block["creatorID"]
		block["recyclerID"] = self.verschrotterID
		body = json.dumps(block, separators=(',', ':'))
		request = self.factory.put("block/", body, content_type='application/json')
		response = BlockView.as_view()(request)
		print(response)
		print(response.data)
		self.assertEqual(JSONRenderer().render(BlockSerializer(Block.objects.latest("id")).data), response.data)
		self.assertEqual(response.status_code, 200)


	def test_verify(self):
		print("::::TEST VERIFY:::")
		serializer = BlockSerializer(Block.objects.latest("id"))
		d_str = JSONRenderer().render(serializer.data)
		signature = rsa.sign(d_str, self.privkey, 'SHA-256')
		creator = Key.objects.get(creatorID="80e75ded-6793-4f29-bb90-c984bf8874b3")
		res = BlockView().check(Block.objects.latest("id"), creator, signature)
		print(res)
		self.assertEqual(res, True)
