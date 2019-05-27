import json
import rsa
from uuid import uuid4
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Block
from .serializers import BlockSerializer

class BlockView(APIView):
    serializer_class = BlockSerializer
    head_objectID = [0]
    def get_object(self, uuid):
        try:
            return Block.objects.get(objectID=uuid)
        except Block.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        if uuid == "0":
            uuid = self.head_objectID[0]
            print(self.head_objectID[0])

        block = self.get_object(uuid)
        serializer = BlockSerializer(block, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "objectType" in body
            or not "pfand" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Wenn der Block nicht unterschrieben ist wird er wieder zurückgesendet, mit der ID des vorherigen Blocks und der zugewiesenen ID
        if (not "sighash" in body):
            new_objectID = uuid4()
            block = Block.objects.create(
                        creatorID = body["creatorID"],
                        objectID = new_objectID,
                        objectType = body['objectType'],
                        pfand = body['pfand'],
                        status = "In Benutzung",
                        prevID = self.head_objectID[0],
                        prevhash = "foo")
            serialized_block = BlockSerializer(block, many=False).data
            Block.objects.filter(objectID=new_objectID).delete()
            return Response(data=serialized_block, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        # Block ist unterschrieben, überprüfen
        block = Block.objects.create(
                        creatorID = body["creatorID"],
                        objectID = body["objectID"],
                        objectType = body['objectType'],
                        pfand = body['pfand'],
                        status = "In Benutzung",
                        prevID = body["prevID"],
                        prevhash = body["prevhash"])
        serialized_block = str(BlockSerializer(block, many=False).data).encode("utf-8") # Encoding muss vor dem prüfen sein

        # Key zum testen! Sollte live natürlich mittels der creatorID aus der Datenbank geholt werden
        pubkey = rsa.PublicKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537)
        block_is_valid = rsa.verify(serialized_block, body["sighash"], pubkey)

        # ----- PRIVATE KEY FOR TESTING ----- #
        # PrivateKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537, 2610569376032565956309174622037664216017335124208227255278187302182857934127620588652325851492936605352779514612193161739271679676319086770723600501383313, 5423127635530564405310435204517160683830388719985322756621937065802093201396704811, 1242634711636051238726630576667870429726659551427143718832064794022377887)
        
        # ----- PUBLIC KEY FOR TESTING ----- #
        # PublicKey(6738966645543023281811658153634882610884200883694445786559262691947296382803065816957045001982432020091322024998783146911708480687607804867847636432914357, 65537)

        if block_is_valid:
            Block.objects.filter(objectID=body["objectID"]).update(sighash=body["sighash"])
            self.head_objectID[0] = body["objectID"]
            return Response(str(self.head_objectID[0]), status=status.HTTP_200_OK)

        # Falsche signatur, weg damit
        Block.objects.filter(objectID=body["objectID"]).delete()
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        body = json.loads(request.body)
        if (not "recyclerID" in body
            or not "objectID" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Alles gut, verschrotten
        Block.objects.filter(objectID=body["objectID"]).update(status="verschrottet")
        return Response(status=status.HTTP_200_OK)
