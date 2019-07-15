import requests
import rsa
import sys
import json
import fileinput

class test:
	def __init__(self):
		self.address = "http://127.0.0.1:8000/"
		self.creatorID = "80e75ded-6793-4f29-bb90-c984bf8874b3"
		self.verschrotterID = "8aeb900e-80cd-4240-9823-d6d757161f4c"
		self.pubkey = rsa.PublicKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537)
		self.privkey = rsa.PrivateKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537, 2610569376032565956309174622037664216017335124208227255278187302182857934127620588652325851492936605352779514612193161739271679676319086770723600501383313, 5423127635530564405310435204517160683830388719985322756621937065802093201396704811, 1242634711636051238726630576667870429726659551427143718832064794022377887)

	def create_block(self, block_dict):
		print("::::TEST CREATE OBJECT::::")
		new_block = {'creatorID':self.creatorID, 'objectType':block_dict["objectType"], 'pfand':block_dict["pfand"], 'status':block_dict["status"]}
		body = json.dumps(new_block)
		response = requests.post(self.address + "block/", body)
		#print(response)
		#print(response.json)
		#print(response.text)
		block = json.loads(response.text)
		block_b = json.loads(block)
		#print(block_b)
		#print(type(block_b))
		#print(block)
		#print(type(block))
		data = json.dumps(block_b, separators=(',', ':'))
		signature = rsa.sign(data.encode("utf8"), self.privkey, 'SHA-256')
		block_b["hash"] = signature.hex()
		body = json.dumps(block_b, separators=(',', ':'))
		response = requests.post(self.address + "block/", body)
		#print(response)
		#print(response.text)

if __name__ == "__main__":
	string = ""
	for line in fileinput.input():
		string += line
	print(string)
	block_dic = json.loads(line.encode('ascii','ignore'))
	t = test()
	t.create_block(block_dic)
