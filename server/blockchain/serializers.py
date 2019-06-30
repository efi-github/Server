from rest_framework import serializers
from .models import Block, Key


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("creatorID", "objectID", "objectType", "pfand", "status", "prevhash")

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ("creatorID", "key", "type")
