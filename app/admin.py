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

class ErrorHistoryAdmin(admin.ModelAdmin):
    list_display = ('machineInfo',
                    'datetime',
                    'error_code',
                    'error_message'
    )
admin.site.register(ErrorHistory, ErrorHistoryAdmin)

class TimeLineStatusAdmin(admin.ModelAdmin):
    list_display = ('machineInfo',
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

class ErrorTypeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'machine_type',
                    'comment'
    )
admin.site.register(ErrorType, ErrorTypeAdmin)

class ErrorMessageAdmin(admin.ModelAdmin):
    list_display = ('error_type',
                    'error_code',
                    'error_message'
    )
admin.site.register(ErrorMessage, ErrorMessageAdmin)

class MachineMembersAdmin(admin.ModelAdmin):
    list_display = ('plantInfo',
                    'line_name',
                    'machine_name'
    )
admin.site.register(MachineMembers, MachineMembersAdmin)

class UtilizationRatePerDayAdmin(admin.ModelAdmin):
    list_display = ('machineInfo',
                    'datetime',
                    'rate'
    )
admin.site.register(UtilizationRatePerDay, UtilizationRatePerDayAdmin)

class UtilizationRatePerHourAdmin(admin.ModelAdmin):
    list_display = ('machineInfo',
                    'datetime',
                    'rate'
    )
admin.site.register(UtilizationRatePerHour, UtilizationRatePerHourAdmin)