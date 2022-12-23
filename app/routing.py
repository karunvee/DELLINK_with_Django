from django.urls import path
from .consumers import AppConsumer

ws_urlpatterns = [
    path('ws/app/', AppConsumer.as_asgi())
]