import gevent
from time import time
from getters.datagetter import *
from emokit.emotiv import Emotiv

class EmoGetter(DataGetter):
	_values = [ ]
	_fs = 20

	"""Gets data from Emotiv"""
	def __init__(self):
		super(EmoGetter, self).__init__()

		self.headset = Emotiv()

		gevent.spawn(self.headset.setup)
		gevent.sleep(0)

		self.running = True

	def get_all_data(self):
		return _values

	def get_next_data(self):
		packet = self.headset.dequeue()
		if packet is None:
			self.running = False
			return [ ]

		sensors = packet.sensors
		
		vect_2 = (packet.gyro_y ** 2 + packet.gyro_x ** 2)
		is_bad = vect_2 > 2

		values = [ ]

		#if sum(self.gyro_hist[-self.n_usless:]) / len(self.gyro_hist[-self.n_usless:]) - vect_2 > self.n_change:
		#	is_bad = True

		for data_name in DATA_NAMES:
			val = sensors[data_name]['value']
			values.append(val)

		gevent.sleep(0)

		self._values.append(values)

		return (values, False)


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