from django.urls import include, path
from . import views
from .views import View
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view , name='home_view'),
    path('remote/', views.remote_view , name='remote_view'),
    path('line_view/pt<str:pt>ln<str:ln>/', views.line_view, name='line_view'),
    path('camera_view/pt<str:pt>ln<str:ln>mc<str:mc>/', views.camera_view, name='camera_view'),
    path('machine_view/pt<str:pt>ln<str:ln>mc<str:mc>/', views.machine_view, name='machine_view'),
    path('set_line/pt<str:pt>ln<str:ln>/', views.SetLine, name="set_line"),
    path('delete_data/pt<str:pt>ln<str:ln>/', views.DeleteData, name="delete_data"),
    path('assign_camera/pt<str:pt>ln<str:ln>mc<str:mc>/', views.AssignCamera, name='assign_camera'),
    path('assign_indicator/pt<str:pt>ln<str:ln>mc<str:mc>/', views.AssignIndicator, name='assign_indicator'),
    path('delete_indicator/pt<str:pt>ln<str:ln>mc<str:mc>tid<str:tid>/', views.DeleteIndicator, name='delete_indicator'),
    # path('vnc_view/host<str:host>port<str:port>password<str:password>/', views.vnc_viewer, name='vnc_viewer'),
    path('delete_timeline/', views.DeleteTimeline, name='delete_timeline'),
    path('delete_errorhistory/', views.DeleteErrorHistory, name='delete_errorhistory'),
    path('delete_utilizationdays/', views.DeleteUtilizationDays, name='delete_utilizationdays'),
    path('delete_utilizationhours/', views.DeleteUtilizationHours, name='delete_utilizationhours'),
    path('vnc_view/', views.vnc_viewer, name='vnc_viewer'),
    path('update_config/pt<str:pt>ln<str:ln>mc<str:mc>/', views.updateConfig, name='update_config'),
    path('updatetimestart/', views.updatetimestart, name='updatetimestart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)