import uuid
import rsa
import requests
import sys
import json


# beispiel befehl: python sign.py '{"creatorID":"80e75ded-6793-4f29-bb90-c984bf8874b3","objectType":"smt","pfand":"500"}'


pubkey = rsa.PublicKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537)
privkey = rsa.PrivateKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537, 2610569376032565956309174622037664216017335124208227255278187302182857934127620588652325851492936605352779514612193161739271679676319086770723600501383313, 5423127635530564405310435204517160683830388719985322756621937065802093201396704811, 1242634711636051238726630576667870429726659551427143718832064794022377887)
standard_key = (pubkey, privkey)

def sign(string, key = standard_key):
	signature = rsa.sign(string.encode('utf8'), key[1], 'SHA-256')
	return signature.hex()

def put(url, json):
	r = requests.put(url, json)
	return r 


def post(url, json):
	r = requests.post(url, json)
	return r 

def get(url, json):
	r = requests.get(url, json)
	return r 


def create_new_block(key, creatorID, objectType, pfand):
	r = get("http://127.0.0.1:8000/block/0/", {})
	j = r.json()
	print(r.json())
	signature = sign(r.json(), key)
	dict = {"creatorID":creatorID, "objectType":objectType, "pfand":pfand, "prevhash": signature}
	json_of = str(json.dumps(dict))
	r = post("http://127.0.0.1:8000/block/", json_of)
	return r

if __name__ == "__main__":
	#print(sys.argv)
	#print(sys.argv[0])
	#print(sys.argv[1])

	#data = json.loads(sys.argv[1])
	data = json.loads('{"creatorID":"80e75ded-6793-4f29-bb90-c984bf8874b3","objectType":"Kaffeemaschine","pfand":"10"}')
	print("data:\n"+ str(data))
	key = standard_key
	# print(len(sys.argv))
	# if len(sys.argv) > 2:
	# 	keys = json.loads(sys.argv[2])
	# 	pubkey = rsa.PublicKey(keys["pubkey"], 65537)
	# 	privkey = rsa.PrivateKey(keys["pubkey"], 65537, keys["privkey"][0], keys["privkey"][1], keys["privkey"][2])
	# 	key = (pubkey, privkey)
	
	r = create_new_block(key, data["creatorID"], data["objectType"], data["pfand"])
	print(r)
