import pandas as pd 
import time 


class CleanBehaviouralFeatures:
	
	def read_features(self):
		self.features = pd.read_csv('../Data/features.csv')

	def pre_process(self):
		start = time.time()
		# check the columns
		print(self.features.columns)
		# drop irrelavant columns
		self.features = self.features.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1','helpful','overall', 'summary','unixReviewTime','reviewText'])
		# normalize by calculating z-score
		for column in self.features.columns:
			if self.features[column].dtype == 'float' or self.features[column].dtype == 'int':
				self.features[column] = (self.features[column] - self.features[column].mean())/self.features[column].std()
		# save the pre-process data and load it again
		self.features.to_csv('../Data/normalized_features.csv')
		end = time.time()
		print('Time taken to pre-process features generated ' + str(end-start))





		



Cleanfeatures = CleanBehaviouralFeatures()
Cleanfeatures.read_features()
Cleanfeatures.pre_process()