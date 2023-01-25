from django.urls import include, path
from . import views
from .views import View
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view , name='home_view'),
    path('line_view/pt<str:pt>ln<str:ln>/', views.line_view, name='line_view'),
    path('machine_view/pt<str:pt>ln<str:ln>mc<str:mc>/', views.machine_view, name='machine_view'),
    path('set_line/pt<str:pt>ln<str:ln>/', views.SetLine, name="set_line"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)