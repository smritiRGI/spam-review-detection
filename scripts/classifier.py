import tensorflow as tt 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold 

class Classifier:

	def read_labeled_data(self):
		self.df = pd.read_csv('../Data/labeled.csv')[['cosineSimilarity', 'reviewLength',
       'maximumReviewsCountRatio', 'activeDays', 'reviewCount',
       'positiveRatingRatio', 'negativeRatingRatio', 'ratioFirstReview',
       'singleReviews', 'ratingDeviation', 'extremeRating',
       'ratioCapitalLetters','label']]
		self.y = self.df['label']
		self.df.drop(columns=['label'],inplace=True)
		print(self.df.columns)

	def split_data(self):
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.df, self.y, test_size=0.1)
		print(self.X_train.shape,self.X_test.shape)
		print(self.y_train.shape,self.y_test.shape)

	def logistic_classifier(self):
		# all parameters not specified are set to their defaults
		logisticRegr = LogisticRegression()
		logisticRegr.fit(self.X_train, self.y_train)
		score = logisticRegr.score(self.X_test, self.y_test)
		print(score)

	
        

classifier = Classifier()
classifier.read_labeled_data()
classifier.split_data()
classifier.logistic_classifier()