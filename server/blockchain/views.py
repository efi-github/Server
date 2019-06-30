import json, rsa, csv
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
from django.contrib.auth import authenticate, login, logout

class BlockView(APIView):
    serializer_class = BlockSerializer

    #Validiert einen Block (Server)
    #Checkt mithilfe des Public Keys ob der Block richtig signiert wurde.
    def check(self, creator, prevhash):
        pubkey= rsa.PublicKey(int(creator.key), 65537)
        prev_block= BlockSerializer(Block.objects.latest("id"), many=False)
        is_valid = rsa.verify(str(prev_block.data).encode('utf8'), prevhash, pubkey)
        return is_valid


    #Liest ein Objekt aus (Jeder)
    #Get holt sich ein bestimmtes Objekt mit der gegebenen UUID.
    #Wenn die UUID==0 ist, dann wird das letzte Objekt ausgelesen.
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
        creator = Key.objects.get(creatorID= body["recyclerID"])
        prevhash = bytes.fromhex(body["prevhash"])
        if not (creator, prevhash) and (creator.type == "Recycler"):
            return Response(status=status.HTTP_409_CONFLICT)
        block = Block.objects.get(objectID=body["objectID"])
        Block.objects.create(
                        creatorID = body["recyclerID"],
                        objectID = block.objectID,
                        objectType = block.objectType,
                        pfand = '0',
                        status = "Verschrottet",
                        prevhash = body['prevhash'])
        return Response(status=status.HTTP_200_OK)

class PfandWebsite(APIView):
    #Wenn man http://127.0.0.1:8000/pfandWebsite/ aufruft kommt man auf
    #die Pfandabfrage Seite. Zusätzlich kann man mit ?uuid=<UUID> im Link
    #eine Direktabfrage machen.
    def get(self, request):
        if request.GET.get("uuid","0") == "0" or  request.GET.get("uuid","0") == "":
            return render(request,"index.html",{})
        try:
            Object = Block.objects.get(objectID=request.GET.get("uuid","0"))
        except Block.DoesNotExist:
            return render(request,"index.html",{'Object':{'Objekt nicht gefunden':request.GET.get("uuid","0")}})
        print("Rendered out Info")
        return render(request,"index.html",{
            'Object':{
                'Hersteller': Object.creatorID,
                'Typ': Object.objectType,
                'Pfand': Object.pfand+"€",
                'Status':'Pfand gültig' if Object.status=='In Benutzung' else 'Pfand eingelößt'
                }})
        
class RegistrierungWebsite(APIView):
    #Wenn man http://127.0.0.1:8000/registrierungWebsite/ aufruft kommt man auf
    #die Website zum registrieren neuer Objekte. Man muss hierbei sein
    #Produkt, Private Key und den Pfand angeben.
    def get(self, request):
        return render(request,"registrieren.html",{})

    def post(self, request):
        if request.POST.get("type") != "" and int(request.POST.get("pfand")) >= 0 and request.POST.get("key") != "":
            #prevhash = bytes.fromhex(body["prevhash"])
            new_id = uuid4()
            Block.objects.create(
                        #creatorID = body["creatorID"],
                        objectID = new_id,
                        objectType = request.POST.get("type"),
                        pfand = request.POST.get("pfand"),
                        status = "In Benutzung",
                        #prevhash = body['prevhash']
                        )
            return render(request,"registrieren.html",{})
        try:
            Object = Block.objects.get(objectID=request.GET.get("uuid","0"))
        except Block.DoesNotExist:
            return render(request,"registrieren.html",{'Object':{'Objekt nicht gefunden':request.GET.get("uuid","0")}})
        print("Rendered out Registration")
        return render(request,"registrieren.html",{
            'Object':{
                'Hersteller': Object.creatorID,
                'Typ': Object.objectType,
                'Pfand': Object.pfand+"€",
                'Status':'Pfand gültig' if Object.status=='In Benutzung' else 'Pfand eingelößt'
                }})


def getInfo(request):
    return render(request, "getInfo.html")

def showInfo(request):
    #Object = Block.objects.get(objectID=request.GET.get("uuid","0"))
    id=(request.GET.get("GeraeteId"))
    block=Block.objects.get(objectID=id)
    return render(request, "showInfo.html",{'id':id,'block':block})

def main(request):
    return render(request,"main.html")

class DownloadBlockchain(APIView):
    #Wenn man http://127.0.0.1:8000/download/ aufruft läd man sich die komplette
    #Blockchain als CSV File runter
    def get(self, request):
        import csv
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=blockchain.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"id"),
            smart_str(u"creatorID"),
            smart_str(u"objectID"),
            smart_str(u"objectType"),
            smart_str(u"pfand"),
            smart_str(u"status"),
            smart_str(u"prevhash"),
        ])
        for obj in Block.objects.all():
            writer.writerow([
                smart_str(obj.id),
                smart_str(obj.creatorID),
                smart_str(obj.objectID),
                smart_str(obj.objectType),
                smart_str(obj.pfand),
                smart_str(obj.status),
                smart_str(obj.prevhash),
            ])
        return response
