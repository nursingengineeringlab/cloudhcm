import os

class Logger:
	def __init__(self, head):
		self.__head__ = head 
		
	def debug(self, msg):
		print('{}: {}'.format(self.__head__, msg))
		

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
    
