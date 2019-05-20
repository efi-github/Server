import json
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
        body = json.loads(request.body)
        if (not "creatorID" in body
            or not "objectID" in body
            or not "objectType" in body
            or not "pfand" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        Block.objects.create(
                        creatorID = body["creatorID"],
                        objectID = body['objectID'],
                        objectType = body['objectType'],
                        pfand = body['pfand'],
                        status = "In Benutzung",
                        prevhash = "foo")
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        # TODO
        return Response(status=status.HTTP_400_BAD_REQUEST)
