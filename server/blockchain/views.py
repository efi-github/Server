import json, rsa, csv, hashlib
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
from rest_framework.renderers import JSONRenderer

class BlockView(APIView):
    serializer_class = BlockSerializer
    #Validiert einen Block (Server)
    #Checkt mithilfe des Public Keys ob der Block richtig signiert wurde.
    def check(self, block, creator, hash):
        pubkey= rsa.PublicKey(int(creator.key), 65537)
        block_to_verify = Block(
            creatorID = block.creatorID,
            objectID = block.objectID,
            objectType = block.objectType,
            pfand = block.pfand,
            status = True,
            prevhash = Block.objects.latest("id").hash,
            hash = "trolllololo"
        )
        serializedBlock = BlockSerializer(block_to_verify, many=False)
        try:
            b_string = JSONRenderer().render(serializedBlock.data)
            rsa.verify(b_string, hash, pubkey)
        except:
            return False #raise Http404("Verification failed, message :" + str(str(serializedBlock.data).encode('utf8')))
        return True


    #Liest ein Objekt aus (Jeder)
    #Get holt sich ein bestimmtes Objekt mit der gegebenen UUID.
    #Wenn die UUID==0 ist, dann wird das letzte Objekt ausgelesen.
    def get(self, request, uuid=None):
        if uuid is not None:
            return self.get_uuid(request, uuid)
        else:
            return self.get_block(request)

    def get_block(self, request):
        new_id = uuid4()
        data = {'prevhash': Block.objects.latest("id").hash, 'uuid4': str(new_id)}
        body = json.dumps(data)
        return Response(str(body).encode('utf8'), status=status.HTTP_200_OK)

    def get_uuid(self, request, uuid):
        if uuid == "0":
            block = Block.objects.latest("id")
        else:
            try:
                block = Block.objects.filter(objectID=uuid).latest("id")
            except Block.DoesNotExist:
                raise Http404
        serializer = BlockSerializer(block, many=False)
        return Response(str(serializer.data).encode('utf8'), status=status.HTTP_200_OK)
    #Erstellt ein neues Objekt (Hersteller)
    #Post erstellt einen neuen Block mit einem neuen Objekt.

    def commit_new_block(self, request):
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "objectType" in body
            or not "objectID" in body
            or not "pfand" in body
            or not "hash" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            creator = Key.objects.get(creatorID=body["creatorID"])
        except Key.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        hash = bytes.fromhex(body["hash"])
        #hash = bytes.fromhex("10e378fb32a9d6e77cff77153fdb9451dad9b061938479b43dc2ba9761d323da0faf91b8926f50e6b7e9a62b5df3d1d873904fff10d2cc077ddaa2d041a24c39")
        newBlock = Block(
            creatorID = body["creatorID"],
            objectID = body["objectID"],
            objectType = body['objectType'],
            pfand = body['pfand'],
            status = False,
            prevhash = Block.objects.latest("id").hash,
            hash = body['hash'])
        if not ((creator.type == "Hersteller") and self.check(newBlock, creator, hash)):
            return Response(status=status.HTTP_409_CONFLICT)
        newBlock.save()
        return Response(JSONRenderer().render(BlockSerializer(newBlock, many=False).data), status=status.HTTP_200_OK)


    def request_new_block(self, request):
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "objectType" in body
            or not "pfand" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            creator = Key.objects.get(creatorID=body["creatorID"])
        except Key.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        new_id = uuid4()
        newBlock = Block(
            creatorID = body["creatorID"],
            objectID = new_id,
            objectType = body['objectType'],
            pfand = body['pfand'],
            status = False,
            prevhash = Block.objects.latest("id").hash
        )
        unhashed_block = str(BlockSerializer(newBlock, many=False).data).encode('utf-8')
        blockhash = hashlib.sha256(unhashed_block).hexdigest()
        newBlock.hash = blockhash
        newBlock.save()
        return Response(JSONRenderer().render(BlockSerializer(newBlock, many=False).data), status=status.HTTP_200_OK)


    def post(self, request):
        body = json.loads(request.body)
        if("hash" in body):
            if "creatorID" in body:
                return self.commit(request)
            else:
                return self.commit_new_block(request)
        else:
            if "creatorID" in body:
                return self.request_put(request)
            else:
                return self.request_new_block(request)

    def request_put(self, request):
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "objectID" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            block = Block.objects.get(objectID=body["objectID"])
        except:
            raise Http404
        newBlock = Block(
            creatorID = body["creatorID"],
            objectID = body["objectID"],
            objectType = block.objectType,
            pfand = '0',
            status = True,
            prevhash = Block.objects.latest("id").hash,
            hash = "trolllololo")
        return Response(JSONRenderer().render(BlockSerializer(newBlock, many=False).data), status=status.HTTP_200_OK)

    def commit(self, request):
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "hash" in body
            or not "objectID" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            creator = Key.objects.get(creatorID= body["creatorID"])
        except:
            raise Http404
        hash = bytes.fromhex(body["hash"])
        try:
            block = Block.objects.get(objectID=body["objectID"])#uuid)
        except:
            raise Http404
        newBlock = Block(
            creatorID = body["creatorID"],
            objectID = body["objectID"],
            objectType = block.objectType,
            pfand = '0',
            status = True,
            prevhash = Block.objects.latest("id").hash,
            hash = body['hash'])
        if not (self.check(newBlock, creator, hash)): #creator.type == "Recycler" and not block.status and
            return Response(status=status.HTTP_409_CONFLICT)
        newBlock.save()
        return Response(JSONRenderer().render(BlockSerializer(newBlock, many=False).data),status=status.HTTP_200_OK)

    def put(self, request):
        body = json.loads(request.body)
        if "hash" in body:
            return self.commit(request)
        else:
            return self.request_put(request)


    #Verschrottet das Objekt (Verschrotter)
    #Put erstellt einen neuen Block, in dem das Objekt
    #als verschrottet markiert und der Pfand auf 0 gesetzt wird.


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
