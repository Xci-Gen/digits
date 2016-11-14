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

from learning.pin_bandpass import PinBandpass 

bp = BandPass((6., 11.), 250.)
pinb = PinBandpass(bp)

def get_data(filename):
	getter = FileGetter(filename)
	return getter.get_all_data()

def learn(digits, other):
	pinb.learn(digits, 'def1')

def test_learn():
	DGTS_CNT = 10
	digits = [ get_data('collect/ne/dgt_{0}_1.csv'.format(i)) for i in range(DGTS_CNT) ]
	learn(digits, 'collect/digits/digit_calibr_nodata.csv')

	for i in range(DGTS_CNT):
		for j in range(1):
			proc, ans = pinb.get_num('def1', get_data('collect/ne/dgt_{0}_{1}.csv'.format(i, 1)))
			print("{0}: {1}, {2}".format(i, proc, ans))

def login():
	name = input('Say your name: ')

	pass_input = ''

	for i in range(4):
		proc, ans = pinb.get_num('name', get_eeg())
		pass_input += str(ans)

		print('*', end='', flush=True)

	print('Done!')

	if pass_input == '5454':
		print('Wrong pass! Think more about "okuns"')
	else:
		print('Great! You are in, hacker.')

def register():
	name = input('Say your name: ')

	digits = [ ]

	for i in range(10):
		print('Think about {0}'.format((i + 1) % 10))
		digits.append(get_eeg())

	print('Think about "okuns"')
	digits.append(get_eeg())

	print('Yeah!')
	pinb.learn(digits, name)

while True:
	method = input('Login/register: ')
	if len(method) == 0 or method[0] == 'l':
		login()
	if method[0] == 'r':
		register()
	elif method[0] == 't':
		test_learn()
	elif method[0] == 'c':
		print('Bye')
		break
