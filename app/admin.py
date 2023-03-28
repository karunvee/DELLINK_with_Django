from django.contrib import admin
from .models import *


# Register your models here.

class LineInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'detail', 'id', 'ip1', 'port1', 'ip2', 'port2', 'ip3', 'port3', 'ip4', 'port4')
admin.site.register(PlantInfo, LineInfoAdmin)

class LineRowAdmin(admin.ModelAdmin):
    list_display = ('plant_name',
                    'line_name',
                    'number',
                    'deviceId', 
                    'name', 
                    'deviceName', 
                    'ip_camera', 
                    'picturePath', 
                    'guid', 
                    'type', 
                    'model', 
                    'url',
                    'remote_host',
                    'remote_password'
                    )
admin.site.register(LineRow, LineRowAdmin)

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('plant_name',
                    'line_name',
                    'machine_name',
                    'tag_name',
                    'tag_id',
                    'register',
                    'data_type',
                    'display',
                    'color',
    )
admin.site.register(Indicator, IndicatorAdmin)

class ErrorNotificationAdmin(admin.ModelAdmin):
    list_display = ('tag_member',
                    'error_code',
                    'error_message',
    )
admin.site.register(ErrorNotification, ErrorNotificationAdmin)

class ErrorHistoryAdmin(admin.ModelAdmin):
    list_display = ('plant_name',
                    'line_name',
                    'machine_name',
                    'datetime',
                    'error_code',
                    'error_message'
    )
admin.site.register(ErrorHistory, ErrorHistoryAdmin)

class TimeLineStatusAdmin(admin.ModelAdmin):
    list_display = ('plant_name',
                    'line_name',
                    'machine_name',
                    'datetime',
                    'status',
                    'error_code'
    )
admin.site.register(TimeLineStatus, TimeLineStatusAdmin)

class TimeLineStartEndAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'start', 
                    'end'
    )
admin.site.register(TimeLineStartEnd, TimeLineStartEndAdmin)

class ErrorMessageAdmin(admin.ModelAdmin):
    list_display = ('machine_type',
                    'error_message'
    )
admin.site.register(ErrorMessage, ErrorMessageAdmin)