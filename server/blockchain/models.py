from django.db import models


class Block(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # TODO: Add more fields

    class Meta:
        ordering = ("created",)
