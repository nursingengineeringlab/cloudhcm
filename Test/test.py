import json
import queue
import atexit
import time
from logger import Logger
from apihandler import api_handler
from senior import senior_manager
import math
import asyncio
import websockets
import argparse
import os
import multiprocessing
from random import randint

# seed random number generator
# generate some integers

websocket_url = "ws://127.0.0.1:8000/"
# websocket_url = "ws://shiywang.asuscomm.com:30007/"

senior_queue = queue.Queue()

PING_TIMEOUT = 60
UPDATE_DATA_TIMEOUT = 1

def current_milli_time():
    return round(time.time() * 1000)


# On program exit delete users from database
def exit_handler():
    print("Deleting Seniors")
    for senior in senior_queue.queue:
        # pass
        senior_manager.delete_senior(senior)
    print("End")


class TestECG(Logger):
    def __init__(self, num_senior):
        Logger.__init__(self, "Main")
        self.num_senior = num_senior
        self.update_percentage = math.ceil(num_senior * 0.15)
        self.debug("Test ECG")
        self.last_ping_time = 0
        self.last_data_update_time = int(time.time())

        seniors = senior_manager.get_senior(num_senior)

        if len(seniors) == 0:
            print("create new seniors")
            seniors = [senior_manager.make_senior() for _ in range(num_senior)]

        for senior in seniors:
            senior_queue.put(senior)

    # def ws_conn(self):
    #     for senior in senior_queue.queue:
    #         device_id = senior.id
    #         url = websocket_url + 'ws/sensordata/RR/' + device_id
    #         with websockets.connect(url) as websocket:
    #             if int(time.time()) - self.last_data_update_time > UPDATE_DATA_TIMEOUT:
    #                 new_rand_value = randint(60, 120)
    #                 senior.device.value = new_rand_value
    #                 data = senior.get_data()
    #                 websocket.send(json.dumps(data))
    #                 self.last_data_update_time = int(time.time())

    # async def send_msg(self, uri, senior):
    #     async with websockets.connect(uri) as ws:
    #         while True:

    async def run(self):
        url = websocket_url + 'ws/sensor/RR'
        async with websockets.connect(url) as websocket:
            while True:
                for senior in senior_queue.queue:
                    if int(time.time()) - self.last_data_update_time > UPDATE_DATA_TIMEOUT:
                        new_rand_value = randint(60, 120)
                        # senior.device.value = new_rand_value
                        # data = senior.get_data()
                        test_json = {
                            "device_id": senior.id,
                            "sequence_id": senior.seq,
                            "time": int(round(time.time() * 1000)),
                            "value": new_rand_value,
                            "battery": 60,
                        }
                        print(json.dumps(test_json))
                        await websocket.send(json.dumps(test_json))
                        self.last_data_update_time = int(time.time())
                        senior.seq = senior.seq + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='args.')
    parser.add_argument('-n', '--num', type=int, default=1)
    parser.add_argument('-d', '--dele', default=True)

    print("Number of cpu :", multiprocessing.cpu_count())
    args = parser.parse_args()
    input_num = args.num
    if args.dele is True:
        try:
            os.remove("./data_store/test.txt")
        except OSError:
            pass

        with open("./data_store/test.txt", 'a') as results_file:
            pass

    atexit.register(exit_handler)
    test_run = TestECG(input_num)
    asyncio.run(test_run.run())
