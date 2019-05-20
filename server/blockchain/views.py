from django.shortcuts import render
from django.http import HttpResponse
from .models import Block

# Create your views here.
def addBlock(request):
    if request.POST['creatorID'] and request.POST['objectID'] and request.POST['objectType'] and request.POST['pfand']:
        block_instance = Block.objects.create(
                        creatorID = request.POST['creatorID'],
                        objectID = request.POST['objectID'],
                        objectType = request.POST['objectType'],
                        pfand = request.POST['pfand'],
                        status = "In Benutzung",
                        prevhash = getPreviousHash())
        return HttpResponse("done", status=200)
    else:
        return HttpResponse("Missing Arguments", status=400)

def getPreviousHash():
    pass