from channels.generic.websocket import AsyncWebsocketConsumer
# from device_manager.data_medium import dataMedium
from device_manager.manager import onlineSeniorsDict
from data_api.models import Senior
# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.core.cache import cache
import json


DEVICE_TIMEOUT = 60 * 5
MAX_DATA_ARRAY_LEN = 10


class SensorDataConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.device_id = 'test'
        self.device_group_name = self.device_id
        await self.channel_layer.group_add(
            self.device_group_name,
            self.channel_name
        )

        await self.accept()
        # print("#######CONNECTED############")
        # print(self.device_group_name)



    async def disconnect(self, code):
        # global onlineSeniorsDict

        await self.channel_layer.group_discard(
            self.device_group_name,
            self.channel_name
        )

        with onlineSeniorsDict as online_seniors:
            del online_seniors[self.device_id]

        # print("DISCONNECED CODE: ",code)
        # print("Device IDL ", self.device_id)

    async def receive(self, text_data=None):
        # global onlineSeniorsDict

        # print("MESSAGE RECEIVED")
        data = json.loads(text_data)
        device_id = data['device_id']

        # await cache.set(device_id, "value", timeout=None)
        # await cache.set_async("key", "value", timeout=None)
        # ret = await cache.ttl_async(device_id)
        # if ret == 0:
        #     senior = await database_sync_to_async(Senior.objects.get(device_id=device_id))
        #     data["name"] = senior.name
        #     data["room_no"] = senior.room_no
        #     data["device_type"] = senior.device_type
        #     data["gender"] = senior.gender
        #     data["data"] = [{"value": 0, "time": 0}]  # Create list to store sensor data
        #     await cache.set_async(device_id, data, timeout=10)
        # else:
        #     await cache.set_async(device_id, data, timeout=10)

        if device_id in onlineSeniorsDict:
            with onlineSeniorsDict as online_seniors:
                online_seniors[device_id]["time"] = data["time"]  # Assign new unix time
                online_seniors[device_id]["battery"] = data["battery"]
        else:  # New Device
            device_id = data.get("device_id")
            senior = await sync_to_async(Senior.objects.get, thread_sensitive=True)(device_id=device_id)
            data["name"] = senior.name
            data["room_no"] = senior.room_no
            data["device_type"] = senior.device_type
            data["gender"] = senior.gender
            data["data"] = [{"value": 0, "time": 0}]  # Create list to store sensor data

            with onlineSeniorsDict as online_seniors:
                online_seniors[device_id] = data

        await self.channel_layer.group_send(
            self.device_group_name,{
                "type": 'send_message_to_frontend',
                "message": text_data
            }
        )

    async def send_message_to_frontend(self,event):
        # Receive message from room group
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))