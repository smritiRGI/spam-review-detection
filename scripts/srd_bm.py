import pandas as pd 
import numpy as np 
import time 


class BehaviouralSpamDetection:

	def read_features(self):
		self.start = time.time()
		self.features = pd.read_csv('../Data/normalized_features.csv')
		


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
		weights_for_all_features = np.array(weights_for_all_features)
		# a row wil have weights for all features  
		weights_for_all_features = weights_for_all_features.T
		features = self.features[['cosineSimilarity',
       'reviewLength', 'maximumReviewsCountRatio', 'activeDays', 'reviewCount',
       'positiveRatingRatio', 'negativeRatingRatio', 'ratioFirstReview',
       'singleReviews', 'ratingDeviation', 'extremeRating',
       'ratioCapitalLetters']]
		score = np.sum(weights_for_all_features * features,axis=1)
		total_weight = np.sum(weights_for_all_features,axis=1)
		spam_score = score/total_weight
		# let us say threshold is 0.6
		self.features['label'] = ['Spam' if score > 0.6 else 'Not Spam' for score in spam_score]
		# print(self.features[self.features['label'] == 'Spam']['reviewText'])

	def save_data(self):

		self.features.to_csv('../Data/labeled.csv')
		self.end = time.time()
		print('Time taken to run the algorithm: ' + str(self.end-self.start))
		



		


Detector = BehaviouralSpamDetection()
Detector.read_features()
Detector.spam_detection()
Detector.save_data()