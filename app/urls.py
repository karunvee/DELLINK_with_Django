from django.urls import include, path
from . import views
from .views import View
urlpatterns = [
    path('', views.home_view , name='home_view'),
]