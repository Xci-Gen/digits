import gevent
from time import time
from getters.datagetter import *

class FileGetter(DataGetter):
	"""Gets data from file"""
	def __init__(self, filename):
		super(FileGetter, self).__init__()

		self._values = [ ]
		self._index = 0

		# Reads file content
		with open(filename) as f:
			lines = [ line.rstrip('\n') for line in open(filename) ]
			for line in lines:
				if '#' in line:
					continue

				values = [ int(v) for v in line.split(',') ]

				if len(values) == len(DATA_NAMES):
					self._values.append(values)

			self.running = len(self._values) > 0

	def get_all_data(self):
		return self._values

	def get_next_data(self):
		if not self.running:
			return [ ]

		v = self._values[self._index]
		self._index += 1

		if self._index >= len(self._values):
			self.running = False

		return (v, False)
	
	def getN(self, n):
		T = 1 / self._fs

		datas = [ ]

		for i in range(n):
			a = time.time()
			
			v, g = self.get_next_data()
			datas.append(v)

			b = time.time()
			delta = b - a

			if delta < T:
				time.sleep(T - delta)

		return datas