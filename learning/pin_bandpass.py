import numpy as np

from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier

from preprocessing.bandpass import BandPass
from preprocessing.preprocessing import Preprocessor

from getters.filegetter import FileGetter

from collections import Counter


GETFOR = 800
SPLIT = 54

class PinBandpass(object):
	def __init__(self, bandpass):
		super(PinBandpass, self).__init__()
		self.bandpass = bandpass

	def get_filename(self, name):
		return 'pin_cls/{0}.cls'.format(name)

	def get_files_data(self, urls_list, max_read=GETFOR + SPLIT):
		tans = []

		for rn in urls_list:
			data = FileGetter(rn).get_all_data()[:max_read]
			tans.extend(self.prepare_data(data))

		return tans

	def prepare_data(self, data, pp=True):
		chs = [ 'T7', 'T8', 'P7', 'P8', 'O1', 'O2']
		return self.get_part_from_a([Preprocessor.leave_main(i, chs) for i in data ], split=SPLIT, pp=pp)

	def learn(self, datas, login):
		x_part_from_owner = []

		ny = [ ]

		for ind, data in enumerate(datas):
			prepared = self.prepare_data(data)

			ny += len(prepared) * [ ind ]

			x_part_from_owner.extend(prepared)

		nx = x_part_from_owner# + x_part_from_others

		nx = np.reshape(nx, (np.shape(nx)[0], -1))

		#classifer = SGDClassifier(loss="hinge", penalty="l2", random_state=54)
		#classifer = MLPClassifier(hidden_layer_sizes=(100, ), random_state=54)
		classifer = SVC()
		classifer.fit(nx, ny)

		joblib.dump(classifer, self.get_filename(login))
	
	def get_part_from_a(self, alld, split=100, pp=True):
		change = []
		last = ''
		nm = []
		for i in range(len(alld)-split):
			nn = '\t'+str(round(100*(i/(len(alld)-split)))) + '\t%'
			if nn != last and pp: 
				last = nn
				print(nn)

			nm.append(self.bandpass.filter(np.transpose( alld[i:i+split]  )))

		return nm

	def get_num(self, login, data, procent=0.9):
		data = self.prepare_data(data, pp=False)
		data = np.reshape(data, (np.shape(data)[0], -1))
		clf = joblib.load(self.get_filename(login))

		ans = list(clf.predict(data))
		cntr = Counter(ans)
		most_cmn, count = cntr.most_common()[0]

		print(cntr.most_common())

		proc = count / len(ans)

		return (proc, most_cmn)

