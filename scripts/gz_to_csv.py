import pandas as pd
import gzip
import json

class ReadData:
	def __init__(self):
		self.read_data()

	def parse(self,path):
		g = gzip.open(path, 'rb')
		for l in g:
			yield json.loads(l)

	def read_data(self):
		path = '../Data/reviews_Beauty_5.json.gz'
		df = {}
		i = 0
		for d in self.parse(path):
			df[i] = d
			i += 1
		df = pd.DataFrame.from_dict(df, orient='index')
		df.to_csv('../Data/reviews.csv')
		

data = ReadData()
