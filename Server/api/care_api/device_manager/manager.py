import os, time, copy, json
import threading, queue
from data_api.models import Senior
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from device_manager.online_senior_dict import Online_Seniors

DEVICE_TIMEOUT = 60 * 5
MAX_DATA_ARRAY_LEN = 10


onlineSeniorsDict = Online_Seniors()


class Online_Seniors_Manager(threading.Thread):
    def __init__(self):
        super(Online_Seniors_Manager, self).__init__()
        self.__q = queue.Queue()
        self.timeout = 1.0 / 60

    def onThread(self, function, *args, **kwargs):
        self.__q.put((function, args, kwargs))

    def delete_senior(self, device_id):
        global onlineSeniorsDict
        with onlineSeniorsDict as online_seniors:
            del online_seniors[device_id]

        # data = {
        #     "device_id": device_id,
        #     "command": "offline",
        # }
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'event_sharif',
        #     {
        #         'type': 'send_message_to_frontend',
        #         'message': data
        #     }
        # )

    # def senior_exist(self, device_id) -> bool:
    #     global onlineSeniorsDict
    #     if device_id in onlineSeniorsDict:
    #         return True
    #     else:
    #         return False

    '''
    This Function is used to process pings from node devices. It serves both new and already online devices.
    It takes a dictionary as an argument.
    data_r = {
        "device_id": ...
        "battery": ...
    }
    '''
    def add_senior(self, data_r):
        global onlineSeniorsDict
        data = copy.deepcopy(data_r)  # Create deep copy that we can modify
        data["time"] = int(time.time())  # Assign new unix time
        device_id = data.get("device_id")

        # Device already in list
        if device_id in onlineSeniorsDict:
            with onlineSeniorsDict as online_seniors:
                online_seniors[device_id]["time"] = data["time"]  # Assign new unix time
                online_seniors[device_id]["battery"] = data["battery"]
        else:  # New Device
            try:
                device_id = data.get("device_id")
                senior = Senior.objects.get(device_id=device_id)
                data["name"] = senior.name
                data["room_no"] = senior.room_no
                data["device_type"] = senior.device_type
                data["gender"] = senior.gender
                data["data"] = [{"value": 0, "time": 0}]  # Create list to store sensor data

                with onlineSeniorsDict as online_seniors:
                    online_seniors[device_id] = data

                # Send to Node server, only for new devices
                # data["command"] = "ping"
                # # zeroMQManager.send(data)
                # # sensorDataConsumer.send(data)
                # channel_layer = get_channel_layer()
                # (channel_layer.group_send)(
                #     'event_sharif',
                #     {
                #         'type': 'send_message_to_frontend',
                #         'message': data
                #     }
                # )
            except Exception as e:
                pass

    '''
    This Function receives new sensor for this senior and adds it to list
    It takes a dictionary as an argument.
    data_r = {
    "device_id": ...
    "time": ...
    "value": ...
    }
    '''
    def add_data(self, data_r):
        global onlineSeniorsDict
        data = copy.deepcopy(data_r)  # Create deep copy that we can modify
        device_id = data.get("device_id")

        if device_id in onlineSeniorsDict:
            with onlineSeniorsDict as online_seniors:
                data2 = copy.deepcopy(data_r)
                data2.pop("device_id")
                online_seniors[device_id]["data"].append(data2)

                # Maintain fixed size
                if len(online_seniors[device_id]["data"]) > MAX_DATA_ARRAY_LEN:
                    online_seniors[device_id]["data"].pop(0)

        # data["command"] = "data"
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'event_sharif',
        #     {
        #         'type': 'send_message_to_frontend',
        #         'message': data
        #     }
        # )


    '''
    This Function is Executed during Idle periods to find devices that have not pinged in a long time.
    '''
    def idle(self):
        global onlineSeniorsDict

        current_time = int(time.time())
        with onlineSeniorsDict as online_seniors:  # Iterate through elements in dict and check time
            for key in list(online_seniors):
                last_time = online_seniors[key]["time"]
                if current_time - last_time > DEVICE_TIMEOUT:  # Ping has not be recieved
                    # data = {"device_id": key, "command": "offline"}
                    del online_seniors[key]
                    # channel_layer = get_channel_layer()
                    # async_to_sync(channel_layer.group_send)(
                    #     'event_sharif',
                    #     {
                    #         'type': 'send_message_to_frontend',
                    #         'message': data
                    #     }
                    # )


    def run(self):
        while True:
            try:
                function, args, kwargs = self.__q.get(timeout=self.timeout)
                function(*args, **kwargs)
            except Exception as e:
                self.idle()


onlineSeniorsManager = Online_Seniors_Manager()
