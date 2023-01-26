from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

def default_image_path():
    return f'{settings.STATIC_URL}/img/default.png'
    
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

class LineRow(models.Model):
    plant_name = models.CharField(max_length = 255)
    line_name = models.CharField(max_length = 255)
    deviceId = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    deviceName = models.CharField(max_length = 255)
    number = models.IntegerField(unique=True)
    status = models.CharField(max_length = 255)
    ip_camera = models.CharField(max_length = 255, blank=True)
    picturePath = models.ImageField(upload_to='images/', default=default_image_path)

    guid = models.CharField(max_length = 255)
    type = models.CharField(max_length = 255)
    model = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
