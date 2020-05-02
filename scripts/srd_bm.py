import pandas as pd 
import numpy as np 


class BehaviouralSpamDetection:

	def read_features(self):
		self.features = pd.read_csv('../Data/normalized_features.csv')
		print(self.features.columns)
		print(self.features.head())


	def spam_detection(self):
		
		sum_of_all_features = np.sum(self.features,axis = 1)
		# print(sum_of_all_features)
		columns = ['cosineSimilarity',
       'reviewLength', 'maximumReviewsCountRatio', 'activeDays', 'reviewCount',
       'positiveRatingRatio', 'negativeRatingRatio', 'ratioFirstReview',
       'singleReviews', 'ratingDeviation', 'extremeRating',
       'ratioCapitalLetters']
        # number of features are taken to be 12
		average_score = sum_of_all_features / 12
		# print(average_score)
		weights_for_all_features = []
		for column in columns:
			drop_score = (sum_of_all_features - self.features[column])/12
			score = np.abs(drop_score-average_score)
			weights = [2 if s >= 0.05 else 1 for s in score ]
			weights_for_all_features.append(weights)
		



		


Detector = BehaviouralSpamDetection()
Detector.read_features()
Detector.spam_detection()