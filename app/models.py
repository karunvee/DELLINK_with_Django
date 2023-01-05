from django.db import models

# Create your models here.
class PlantInfo(models.Model):
    name = models.CharField(max_length = 255)
    detail = models.CharField(max_length = 255)
    ip = models.CharField(max_length = 255)
    port = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name