from django.shortcuts import render
from django.http import HttpResponse
from .models import Block

# Create your views here.
# def addBlock(request):
#    if request.POST['creatorID'] and request.POST['objectID'] and request.POST['objectType'] and request.POST['pfand']:
#        block_instance = Block.objects.create(
#                        creatorID = request.POST['creatorID'],
#                        objectID = request.POST['objectID'],
#                        objectType = request.POST['objectType'],
#                        pfand = request.POST['pfand'],
#                        status = "In Benutzung",
#                        prevhash = getPreviousHash())
#        return HttpResponse("done", status=200)
#    else:
#        return HttpResponse("Missing Arguments", status=400)

#def getPreviousHash():
#    pass
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Block

class BlockView(APIView):
    def get_object(self, uuid):
        try:
            return Block.objects.get(pk=uuid)
        except Block.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        # TODO: Mehr als eine Testimplementierung draus machen…
        block = self.get_object(uuid)
        return Response(Block, status=status.HTTP_200_OK)

    def post(self, request):
        # TODO
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # TODO
        return Response(status=status.HTTP_400_BAD_REQUEST)
