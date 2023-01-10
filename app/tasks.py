import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

from celery import Celery
from typing import Any, Dict
import msgpack

from .models import *

channel_layer = get_channel_layer()

app = Celery('DELLINK')

def urlDIA(ip, port, method):
    http_name = 'http://' + ip + ':' + port + '/api/v1/' + method
    return http_name

def publish_message_to_group(message: Dict[str, Any], group: str) -> None:
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            msgpack.packb({
              "__asgi_group__": group,
              **message,
            }),
            exchange="groups",  # groups_exchange
            content_encoding="binary",
            routing_key=group,
            retry=False,  # Channel Layer at-most once semantics
        )

@shared_task
def get_api():
    plant_members = PlantInfo.objects.all()

    for plant in plant_members:
        url1 = urlDIA(plant.ip1, plant.port1, 'devices')
        response = requests.get(url1).json()
        publish_message_to_group({ "type": "chat_message", "text": response }, "app")
        print('<==================> API reading success :' + url1)
        # for item in response:
        #     print('<==================> message :' + item['comment'])

        if not plant.ip2 and not plant.port2:
            url2 = urlDIA(plant.ip2, plant.port2, '')
        if not plant.ip3 and not plant.port3:
            url3 = urlDIA(plant.ip3, plant.port3, '')
        if not plant.ip4 and not plant.port4:
            url4 = urlDIA(plant.ip4, plant.port4, '')




    # response = requests.get(url).json()
    # msg = response['comment']

    # publish_message_to_group({ "type": "chat_message", "text": msg }, "app")
    # # async_to_sync(channel_layer.group_send)("app", {"type": "chat_message","text": msg,},)
    # print('<==================> message :' + msg)
