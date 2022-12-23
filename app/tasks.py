import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

from celery import Celery
from typing import Any, Dict
import msgpack

channel_layer = get_channel_layer()

app = Celery('DELLINK')


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

    url = 'https://random-data-api.com/api/v2/beers'
    response = requests.get(url).json()
    msg = response['name']

    publish_message_to_group({ "type": "chat_message", "text": msg }, "app")
    # async_to_sync(channel_layer.group_send)("app", {"type": "chat_message","text": msg,},)
    print('<==================> message :' + msg)
