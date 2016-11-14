#               0     1      2     3     4      5     6     7     8      9     10    11     12    13
DATA_NAMES = [ 'T8', 'AF3', 'F3', 'F7', 'FC5', 'P7', 'T7', 'O1', 'AF4', 'F4', 'F8', 'FC6', 'P8', 'O2' ]

class DataGetter(object):
	_fs = 20
	
	"""Gets data from File or Emotiv"""
	def __init__(self):
		self.running = False
		
	def get_all_data(self):
		return [ [ ] ]

	def get_next_data(self):
		return [ ], False

	def getN(self, n):
		return [ ]