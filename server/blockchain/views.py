import json
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
            or not "objectID" in body
            or not "objectType" in body
            or not "pfand" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        new_objectID = uuid4()
        Block.objects.create(
                        creatorID = body["creatorID"],
                        objectID = new_objectID,
                        objectType = body['objectType'],
                        pfand = body['pfand'],
                        status = "In Benutzung",
                        prevID = head_objectID[0],
                        prevhash = "foo")
        self.head_objectID[0] = new_objectID
        return Response(str(self.head_objectID[0]), status=status.HTTP_200_OK)

    def put(self, request):
        body = json.loads(request.body)
        if (not "recyclerID" in body
            or not "objectID" in body):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Alles gut, verschrotten
        Block.objects.filter(objectID=body["objectID"]).update(status="verschrottet")
        return Response(status=status.HTTP_200_OK)
