from statistics import median
import numpy as np
from sklearn.decomposition import PCA
from getters.datagetter import DATA_NAMES
from preprocessing.bandpass import BandPass

class Preprocessor(object):

	"""Converts Raw data to beatiful butterfly"""
	def __init__(self, n):
		self.n = n
		self.datas = [ [] for i in DATA_NAMES ]
		
		self.pca = PCA(copy=False, whiten=False)

		self.bandpass = BandPass((500.0, 1250.0), 3000)

		
	def to_fft(self, datas=None, fft=True):
		if fft:
			if datas is None:
				datas = self.datas

			fft = abs(np.fft.fft(datas))
			ans = [ ]
			#return fft

			for ind, wk in enumerate(fft):
				wk = fft[ind]
				wk = [ i - min(wk) for i in wk ]
				ans.append(wk)

			return ans
		else:
			return BandPass((6., 11.), 250.).filter(datas)

	def find_main(self, datas=None, proc=0.50):
		assert np.shape(datas)[0] == 14
		
		if datas is None:
			datas = self.datas
		if len(datas[0]) < self.n:
			return [ [] for i in DATA_NAMES ]
		self.pca.fit(datas)
		ans = []
		for i in np.rot90(self.pca.components_):
			ans.append(sum(i))
		n = int(proc * len(ans))
		min_ = sorted(ans)[-n]
		new_ans = [  ]
		dd = np.rot90(datas)
		for i in range(len(ans)):
			if ans[i] >= min_:
				new_ans.append(dd[i])

		new_ans = np.rot90(np.array(new_ans), k=3)
		
		return new_ans

	@staticmethod
	def leave_main(datas, channels_names=[ 'T7', 'T8', 'P7', 'P8', 'O1', 'O2']):
		channels = [ DATA_NAMES.index(ch) for ch in channels_names ]
		new_datas = [ datas[i] for i in channels ]

		return new_datas

	@staticmethod
	def pca(datas):

		# w, v = PCA(copy=False, whiten=False).pca(x)
		# y = np.dot(self.w, x)

		# return y
		return datas

	def process(self, data, n=None):
		if n is not None:
			self.n = n 

		if len(data) == 0:
			return data

		#data = self.process_only(data)
		for i in range(len(DATA_NAMES)):
			if len(self.datas[i]) >= self.n:
				del self.datas[i][0]

			self.datas[i].append(data[i])
		
		return data

	def process_only(self, data):
		left_ear = data[0]
		right_ear = data[len(data) // 2]

		# for i in range(len(data) // 2):
		# 	data[i] = (data[i] - left_ear)

		# for i in range(len(data) // 2, len(data)):
		# 	data[i] = (data[i] - right_ear)


		return data
