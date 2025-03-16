from django.db import models
import hashlib

class Tile(models.Model):
    data = models.JSONField()
    hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_from_data(cls, data):
        tile_hash = hashlib.sha256(str(data).encode()).hexdigest()
        return cls.objects.get_or_create(hash=tile_hash, defaults={'data': data})

class MissionData(models.Model):
    sender_x = models.IntegerField()
    sender_y = models.IntegerField()
    listener_x = models.IntegerField()
    listener_y = models.IntegerField()
    cuper_price = models.FloatField()
    engel_price = models.FloatField()