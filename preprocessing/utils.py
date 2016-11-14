class Utils(object):
	"""Utils for preprocessing"""
	def __init__(self):
		super(Utils, self).__init__()
		
	@classmethod
	def from_b_to_a(cls, data):
		n = len(data[0])
		new_data = [ [] for i in range(n) ]

		for dat in data:
			for i in range(n):
				ch = dat[i]
				new_data[i].append(ch)

		return new_data
		
	@classmethod
	def from_a_to_b(cls, data):
		n = len(data)
		new_data = [ [ ch for ch in data[i]] for i in range(n) ]

		return new_data

	@classmethod
	def chunks(cls, data, chunk_len=54):
		chunks = [ ]

		l = chunk_len * (len(data[0]) // chunk_len)
		for x in range(0, l, chunk_len):
			chunk = [ data[i][x:x + chunk_len] for i in range(len(data)) ]
			chunks.append(chunk)

		return chunks

	@classmethod
	def diff(cls, eeg1, eeg2):
		assert(len(eeg1)==len(eeg2))

		n = len(eeg1)
		n_ch = len(eeg1[0])

		diff = [ [ abs(eeg1[ch][k] - eeg2[ch][k]) for k in range(n_ch) ] for ch in range(n) ]

		return diff