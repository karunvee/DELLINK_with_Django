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
    number = models.IntegerField()
    status = models.CharField(max_length = 255)
    ip_camera = models.CharField(max_length = 255, blank=True)
    picturePath = models.ImageField(upload_to='images/', blank=True)
    # picturePath = models.ImageField(upload_to='images/', default=default_image_path)
    guid = models.CharField(max_length = 255)
    type = models.CharField(max_length = 255)
    model = models.CharField(max_length = 255)
    url = models.CharField(max_length = 255)
    remote_host = models.CharField(max_length = 255, default="hostname")
    remote_password = models.CharField(max_length = 255, default="12345678")
    def __str__(self):
        return self.name

class Indicator(models.Model):
    DATA_TYPE = (
        ('BIT', 'BIT'), ('STRING', 'STRING'), ('STATUS', 'STATUS'), ('ERROR CODE', 'ERROR CODE')
    )
    DISPLAY_TYPE = (
        ('BUTTON', 'BUTTON'), ('INDICATOR', 'INDICATOR'), ('TEXT', 'TEXT'), ('NUMBER','NUMBER')
    )
    plant_name = models.CharField(max_length = 255)
    line_name = models.CharField(max_length = 255)
    machine_name = models.CharField(max_length = 255)
    tag_name = models.CharField(max_length = 255)
    tag_id = models.CharField(max_length = 255)
    register = models.CharField(max_length = 255)
    data_type = models.CharField(max_length = 255, choices=DATA_TYPE)
    display = models.CharField(max_length = 255, choices=DISPLAY_TYPE)
    color = models.CharField(max_length = 255,blank=True)

    def __str__(self):
        # return "%s %s %s" % (self.tag_name, self.tag_id, self.data_type)
        return self.tag_name

class ErrorNotification(models.Model):
    tag_member = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True)
    error_code = models.CharField(max_length= 255)
    error_message = models.CharField(max_length= 255)

    def __str__(self):
        return self.error_message