import json
import rsa
from uuid import uuid4
from django.http import Http404, HttpResponse, HttpRequest
from django.db import models
from django.template import Context, loader
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Block, Key
from .serializers import BlockSerializer, KeySerializer

class BlockView(APIView):
    serializer_class = BlockSerializer

    #Validiert einen Block (Server)
    #Checkt mithilfe des Public Keys ob der Block richtig signiert wurde.
    def check(self, creator, prevhash):
        pubkey= rsa.PublicKey(int(creator.key), 65537)
        prev_block= BlockSerializer(Block.objects.latest("id"), many=False)
        print(prev_block, type(prev_block), prev_block.data, type(prev_block.data))
        is_valid = rsa.verify(str(prev_block.data).encode('utf8'), prevhash, pubkey)
        return is_valid


    #Ließt ein Objekt aus (Jeder)
    #Get holt sich ein bestimmtes Objekt mit der gegebenen UUID.
    #Wenn die UUID==0 ist dann wird das letzte Objekt ausgelesen.
    def get(self, request, uuid):
        if uuid == "0":
            block = Block.objects.latest("id")
        else:
            try:
                block = Block.objects.get(objectID=uuid)
            except Block.DoesNotExist:
                raise Http404
        serializer = BlockSerializer(block, many=False)
        return Response(str(serializer.data).encode('utf8'), status=status.HTTP_200_OK)

    #Erstellt ein neues Objekt (Hersteller)
    #Post erstellt einen neuen Block mit einem neuen Objekt.
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

    #Verschrottet das Objekt (Verschrotter)
    #Put erstellt einen neuen Block in dem das Objekt 
    #als verschrottet markiert und der Pfand auf 0 gesetzt wird.
    def put(self, request):
        body = json.loads(request.body)
        if (not "recyclerID" in body
            or not "objectID" in body
            or not "prevhash" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        #Wenn Gerät bereits verschrottet ist gib einen Error aus.
        if "Verschrottet" in Block.objects.filter(objectID=body["objectID"]).status:
            print("[Error] Dieses Gerät wurde bereits verschrottet.\n\t"+Block.objects.filter(objectID=body["objectID"]).status+"\n\tRequest: "+request.body.recyclerID)
            return Response(status=status.HTTP_403_FORBIDDEN) 

        # Alles gut, verschrotten
        else:
            Block.objects.filter(objectID=body["objectID"]).update(status="Verschrottet: "+body.recyclerID)
            return Response(status=status.HTTP_200_OK)

class Website(APIView):
    serializer_class = BlockSerializer 

    def get(self, request):
        if request.GET.get("uuid","0") == "0" or  request.GET.get("uuid","0") == "":
            return render(request,"index.html",{})
        try:
            Object = Block.objects.get(objectID=request.GET.get("uuid","0"))
        except Block.DoesNotExist:
            return render(request,"index.html",{'Object':{'Objekt nicht gefunden':request.GET.get("uuid","0")}})
        print("Rendered out Info")
        return render(request,"index.html",{'Object':{'Hersteller': Object.creatorID,'Typ': Object.objectType,'Pfand': Object.pfand,'Status':Object.status}})
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
