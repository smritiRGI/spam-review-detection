import pandas as pd 


class SpamDetectionBehaviouralFeatures:
	
	def read_data(self):
		self.features = pd.read_csv('../Data/features.csv')

	def pre_process(self):
		# check the columns
		print(self.features.columns)
		# drop irrelavant columns
		self.features = self.features.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1','helpful','overall', 'summary','unixReviewTime'])
		
	def spam_detection(Self):
			sum = np.sum(self.features,axis=1)
		



Detector = SpamDetectionBehaviouralFeatures()
Detector.read_data()
Detector.pre_process()