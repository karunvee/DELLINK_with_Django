from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer, WebsocketConsumer
from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync


class AppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("app", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("app", self.channel_name)

    async def chat_message(self, event):
        text_message =  event["text"]
        await self.send(text_message)

# class AppConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         async_to_sync(self.channel_layer.group_add)("app", self.channel_name)
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)("app", self.channel_name)

#     def chat_message(self, event):
#         self.send(text_data=event["text"])

    # async def connect(self):
    #     await self.channel_layer.group_add("app", self.channel_name)
    #     await self.accept()

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard("app", self.channel_name)

    # async def chat_message(self, event):
    #     text_message =  event["text"]
    #     await self.send(text_message)