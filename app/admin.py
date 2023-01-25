from django.contrib import admin
from .models import *


# Register your models here.

class LineInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'detail', 'id', 'ip1', 'port1', 'ip2', 'port2', 'ip3', 'port3', 'ip4', 'port4')
admin.site.register(PlantInfo, LineInfoAdmin)

class LineRowAdmin(admin.ModelAdmin):
    list_display = ('plant_name','line_name', 'number', 'deviceId', 'name', 'deviceName', 'ip_camera', 'picturePath')
admin.site.register(LineRow, LineRowAdmin)
