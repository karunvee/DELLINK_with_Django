from django.urls import path
from .consumers import AppConsumer, GraphConsumer

ws_urlpatterns = [
    path('ws/app/', AppConsumer.as_asgi()),
    path('ws/graph/', GraphConsumer.as_asgi())
]