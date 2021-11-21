import os
from device_manager.manager import onlineSeniorsManager, onlineSeniorsDict


class DataMediumFake:
    def __init__(self):
        pass


class DataMedium:
    def __init__(self):
        self.start()
        
    def start(self):
        print("Starting data medium")
        onlineSeniorsManager.start()
        pass 

    def senior_exist(self, device_id):
        return onlineSeniorsManager.senior_exist(device_id)

    def ping(self, data):
        try:
            if not all (key in data for key in ("device_id", "battery")):
                raise Exception("Incomplete/Incorrect data")
            onlineSeniorsManager.onThread(onlineSeniorsManager.add_senior, data)
        except Exception as e:
            print(e)

    def delete_senior(self, device_id):
        try:
            onlineSeniorsManager.onThread(onlineSeniorsManager.delete_senior, device_id)
        except Exception as e:
            pass

    def sensor_data(self, data):
        try:
            if not all (key in data for key in ("device_id", "time", "value")):
                raise Exception("Incomplete/Incorrect data")
            onlineSeniorsManager.onThread(onlineSeniorsManager.add_data, data)
        except Exception as e:
            print(e)
        pass


    def stop(self):
        pass 


if "SKIP_ZEROMQ" not in os.environ:
    dataMedium = DataMedium()
else:
    dataMedium = DataMediumFake()
