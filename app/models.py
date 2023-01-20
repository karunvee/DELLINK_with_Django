from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# Create your models here.
class PlantInfo(models.Model):
    name = models.CharField(max_length = 255)
    detail = models.CharField(max_length = 255)

    ip1 = models.CharField(max_length = 255)
    port1 = models.CharField(max_length = 255)

    ip2 = models.CharField(max_length = 255, blank=True)
    port2 = models.CharField(max_length = 255, blank=True)
    ip3 = models.CharField(max_length = 255, blank=True)
    port3 = models.CharField(max_length = 255, blank=True)
    ip4 = models.CharField(max_length = 255, blank=True)
    port4 = models.CharField(max_length = 255, blank=True)

    def __str__(self):
        return self.name


def default_image_path():
    return f'{settings.STATIC_URL}/img/default.png'

class LineRow(models.Model):
    plant_name = models.CharField(max_length = 255)
    line_name = models.CharField(max_length = 255)
    deviceId = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    deviceName = models.CharField(max_length = 255)
    picturePath = models.ImageField(upload_to='images/', default=default_image_path)
    number = models.CharField(max_length = 255, unique=True)

    def __str__(self):
        return self.name