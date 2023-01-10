from django.db import models

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