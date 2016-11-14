import os
import time
import random
import numpy as np
from os import listdir
from os.path import isfile, join

from getters.emogetter import EmoGetter
from getters.filegetter import FileGetter
from getters.datagetter import DataGetter

from preprocessing.bandpass import BandPass

from learning.mlp_bandpass import MLP_Bandpass 

n_i = 0
pas = [True, False]

class Utils(object):
	@staticmethod
	def get_filename(name):
		return '{0}.cls'.format(name)

	@classmethod
	def file_len(cls, fname):
		if not isfile(join(fname)):
			return 0

		with open(fname) as f:
			for i, l in enumerate(f):
				pass
		return i + 1

	@classmethod
	def get_datas(cls, n = 100, cnt=1, is_debug=True):
		datas = [ ]

		csvs = [f for f in listdir("collect/ne/") if cls.file_len(join("collect/ne/", f)) > n * cnt]
		np.random.shuffle(csvs)

		getter = None
		if is_debug:
			getter = FileGetter(join("collect/ne/", csvs[0]))
		else:
			getter = EmoGetter()

		T = 1 / DataGetter._fs

		all_ = n * cnt
		ind = 0

		for c in range(cnt):
			data = [ ]

			for i in range(n):
				ind += 1

				proc = 100 * ind / all_
				#yield (proc, 0)

				a = time.time()
				
				v, g = getter.get_next_data()
				data.append(v)
				yield (proc, v)
				b = time.time()
				delta = b - a

				if delta < T:
					time.sleep(T - delta)

			cls.data = data
			datas.append(data)
			yield (proc, 0)

		cls.datas = datas

		yield (100, 0)
		return

	@classmethod
	def register(cls, name):
		img_all = [f for f in listdir("web/static/img/All") if isfile(join("web/static/img/All", f))]
		n = 3
		n_get = 2

		imgl = [ 0, 0 ]
		while imgl[0] == imgl[1]:
			np.random.shuffle(img_all)
			imgl = img_all[:n]
		print('WOOOW', imgl)

		for image in imgl:
			yield (-5, 0)
			if name == '':
				yield (-1 ,0)
				return
			if os.path.isfile(cls.get_filename(name)):
				yield (-2, 0)
				return

			
			for i in cls.get_datas(cnt=n_get):
				yield (0, image)
				yield (i[0] * 0.9, 0, i[1])

			yield (90, 0, [0 for i in range(14)])
			
			data = cls.data

			bp = BandPass((6., 11.), 250.)
			falselist = ['collect/ne/ui_1.csv', 'collect/SUPER_tanya.csv', 'collect/ne/y_1.csv', 'collect/nastya.csv', 'collect/1_tanya.csv']
			mlp = MLP_Bandpass(bp, falselist, 'collect/ne/margo_3.csv')

			filename = "classificators/" + name + "/" + image
			di_r = os.path.dirname(filename)

			try:
				os.mkdir(di_r) 
			except BaseException:    
				pass  
			yield -4, 0
			mlp.learn( cls.datas, filename)
		yield 100, 0
		return

	@staticmethod
	def reset(i=0):
		global n_i
		n_i = int(i)

	@classmethod
	def login(cls, name, deb=False):
		global pas, n_i


		proc_g = 0
		if name == '':
			yield (-1, 0, 0)
			return

		# if not os.path.isfile(cls.get_filename(name)):
		# 	yield -2
		# 	return
		ans_pg = []

		try:
			models_all = [f for f in listdir("classificators/"+name) if isfile(join("classificators/"+name, f)) and f.endswith('cls')]
		except FileNotFoundError:
			yield (-2, 0, 0)
			return

		n = 3
		print('MALL', models_all)
		np.random.shuffle(models_all)
		models_all = models_all[:n]

		for model in models_all:
			yield (-5, 0, 0)
			thename = model[:-4]
			print('thename', thename)
			yield (-5454, thename, 0)

			for i in cls.get_datas(n=220, is_debug=deb):
				yield (i[0] * 0.9, 0, i[1])

			yield (90, 0, [0 for i in range(14)])

			data = cls.data

			if deb:
				yield (-4, 0, 0)
				time.sleep(4 + random.random() * 2)
				ans_pg.append(50)
			else:
				bp = BandPass((6., 11.), 250.)
				falselist = ['collect/ne/ui_1.csv', 'collect/SUPER_tanya.csv', 'collect/ne/y_1.csv', 'collect/nastya.csv', 'collect/1_tanya.csv']
				mlp = MLP_Bandpass(bp, falselist, 'collect/ne/margo_3.csv')

				yield (-4, 0, 0)

				res, proc = mlp.login("classificators/"+name + '/' + model[:-4], data)
				ans_pg.append(proc)

				print(name, proc)

		print('PP', ans_pg)
		ans_pg.sort()
		rtn = 0.15*(ans_pg[0] + ans_pg[-1]) + 0.7*ans_pg[1]
		print('\trnt', rtn)

		if rtn >= 0.75:
			yield (100, 0, 0)
		else:
			yield (-3, 0, 0)
		return
		 