from django.contrib import admin
from .models import *


# Register your models here.

class LineInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'ip', 'port', 'detail')
admin.site.register(PlantInfo, LineInfoAdmin)