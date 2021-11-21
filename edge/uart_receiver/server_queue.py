import os, queue
from logger import Logger, enum
import threading, time

api_user 		= "admin"
api_password 	= "uched4123"
base_url 		= "http://127.0.0.1:8002/"
request_headers = {'Content-Type': 'application/json',}

class ServerQueue(threading.Thread, Logger):
	def __init__(self):
		threading.Thread.__init__(self)
		Logger.__init__(self, "ServerQueue")
		self.__output_queue = queue.Queue()
		self.__function_queue = queue.Queue()
		self.timeout = 1.0/60
		
	def onThread(self, function, *args, **kwargs):
		self.__function_queue.put((function, args, kwargs))

	def send_data(self, device_id, value, device_type):
		data = {
			"device_id": device_id,
			"time": int(time.time()),
			"value" : value
		}
		url = base_url + "sensordata/" + device_type + '/'
		r = requests.post(url, headers=request_headers, auth=(api_user, api_password), data=json.dumps(data))

	def send_ping(self, device_id):
		data = {
			"device_id": device_id,
			"battery": 67,
		}
		url = base_url + "ping/"
		r = requests.post(url, headers=request_headers, auth=(api_user, api_password), data=json.dumps(data))

	def run(self):
		print("Starting Server Queue")
		while True:
			try:
				# Get functions called on this thread
				function, args, kwargs = self.__function_queue.get(timeout=self.timeout)
				function(*args, **kwargs)			
			except Exception as e:
				pass
		
serverQueue = ServerQueue()		# Single instance of serverQueue
		
