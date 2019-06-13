import json
import rsa
from uuid import uuid4
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Block, Key
from .serializers import BlockSerializer, KeySerializer

class BlockView(APIView):
    serializer_class = BlockSerializer

    def get_object(self, uuid):
        try:
            return Block.objects.get(objectID=uuid)
        except Block.DoesNotExist:
            raise Http404

    def check(self, creator, prevhash):
        pubkey= rsa.PublicKey(int(creator.key), 65537)
        prev_block= BlockSerializer(Block.objects.latest("id"), many=False)
        print(prev_block, type(prev_block), prev_block.data, type(prev_block.data))
        is_valid = rsa.verify(str(prev_block.data).encode('utf8'), prevhash, pubkey)
        return is_valid


    def get(self, request, uuid):
        if uuid == "0":
            block = Block.objects.latest("id")
        else:
            block = self.get_object(uuid)
        serializer = BlockSerializer(block, many=False)
        return Response(str(serializer.data).encode('utf8'), status=status.HTTP_200_OK)


    def post(self, request):
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "objectType" in body
            or not "pfand" in body
            or not "prevhash" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        creator = Key.objects.get(creatorID=body["creatorID"])
        prevhash = bytes.fromhex(body["prevhash"])
        if not (self.check(creator, prevhash) and (creator.type == "Hersteller")):
            return Response(status=status.HTTP_409_CONFLICT)
        new_id = uuid4()
        Block.objects.create(
                        creatorID = body["creatorID"],
                        objectID = new_id,
                        objectType = body['objectType'],
                        pfand = body['pfand'],
                        status = "In Benutzung",
                        prevhash = body['prevhash'])
        return Response(new_id, status=status.HTTP_200_OK)

    def put(self, request):
        body = json.loads(request.body)
        if (not "recyclerID" in body
            or not "objectID" in body
            or not "prevhash" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        creator = Key.objects.get(creatorID=creatorID)
        if not (check(body["recyclerID"], body["prevhash"]) and (creator.creatorID == "Recycler")):
            return Response(status=status.HTTP_409_CONFLICT)
        block = Block.objects.get(creatorID=body["recyclerID"])
        Block.objects.create(
                        creatorID = body["recyclerID"],
                        objectID = block.objectID,
                        objectType = block.objectType,
                        pfand = '0',
                        status = "Verschrottet",
                        prevhash = body['prevhash'])
        return Response(status=status.HTTP_200_OK)
