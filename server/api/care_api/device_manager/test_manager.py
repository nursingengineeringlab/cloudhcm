import os, time
from manager import onlineSeniorsManager, onlineSeniorsDict

senior1 = {"device_id": "AB18D5", "battery": 50}
senior2 = {"device_id": "CF15D5", "battery": 60}
senior3 = {"device_id": "A228D5", "battery": 50}

print("Starting Test")
onlineSeniorsManager.start()
time.sleep(2)
onlineSeniorsManager.onThread(onlineSeniorsManager.add_senior, senior1)
time.sleep(3)
print("hereA", onlineSeniorsDict)
onlineSeniorsManager.onThread(onlineSeniorsManager.add_senior, senior2)
onlineSeniorsManager.onThread(onlineSeniorsManager.add_senior, senior3)
time.sleep(0.5)
print("here1", onlineSeniorsDict)
time.sleep(5)
print("here2", onlineSeniorsDict)