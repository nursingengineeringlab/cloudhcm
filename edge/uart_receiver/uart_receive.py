import serial
import threading
import time
from logger import Logger, enum
from server_queue import serverQueue

start_byte = b'\xbb'
read_length = 33

port_name = "/dev/ttyUSB1"

class UartReader(threading.Thread, Logger):
	def __init__(self, port):
		threading.Thread.__init__(self)
		Logger.__init__(self, "UART")
		self.__port_num__ = port
		self.__port__ = serial.Serial(port, 250000)
		
		self.read_buf = []
		self.read_pointer = 0
		self.state = None
		
	def run(self):
		self.debug("Starting Loop")
		states = enum("START_BYTE", "LENGTH", "DATA")
		self.state = states.START_BYTE					# Current state machine state
		read_len = 0									# Length of serial data to read
		
		while True:
			ch = self.__port__.read()
			
			if ch == start_byte:
				data = self.__port__.read(read_length)
				data = [x for x in data]	# list comprehension, changes bytes to int

				# Get Serial Number
				serial_no_bytes = data[3:9]
				serial_no = ""
				for b in serial_no_bytes:
					serial_no = serial_no + f'{b:0>2X}'

				data_type = ""
				data_value = None
				# Get packet type and data
				if data[10] == 7:
					data_type = "RR"
					try:
						data_value = data[12] * 128 + data[13] #60 / data[13] * 1000 # (60 / HR * 1000)
					except Exception as e:
						data_value = 0

				self.debug(f'Device id: {serial_no}, {data_type}: {data_value}')
					

if __name__ == "__main__":
	uartReader = UartReader(port_name)
	uartReader.start()
