from rest_framework import serializers
from .models import Block


class CardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("created",)