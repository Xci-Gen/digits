from scipy.signal import butter, lfilter
import numpy

class BandPass(object):
	"""Makes band pass on data and removes bad EEG"""
	def __init__(self, limit, fs):
		super(BandPass, self).__init__()

		self.limit = limit
		self.fs = fs

	def butter_bandpass(self, lowcut, highcut, fs, order=5):
		nyq = 0.5 * fs
		low = lowcut / nyq
		high = highcut / nyq
		b, a = butter(order, [low, high], btype='band')
		return b, a


	def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=3):
		b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
		y = lfilter(b, a, data)
		return y

	def filter(self, data):
		lowcut, highcut = self.limit

		new_data = [ self.butter_bandpass_filter(d, lowcut, highcut, self.fs) for d in data ]

		return new_data

