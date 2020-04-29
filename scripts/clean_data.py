import pandas as pd

class CleanData:
	
	@staticmethod
	def pre_process():
		reviews = pd.read_csv('../Data/reviews.csv')
		# check missing values
		for column in reviews.columns:
			print(reviews[column].isnull().value_counts())
		# fill the review text by summary
		reviews['reviewText'] = reviews['reviewText'].fillna(reviews['summary'])

		reviews['unixReviewTime'] = pd.to_datetime(reviews['unixReviewTime'],unit='s')
		# drop repeated columns
		reviews.drop(columns=['reviewTime'],inplace=True)
		reviews.to_csv('../Data/reviews.csv')


CleanData.pre_process()
