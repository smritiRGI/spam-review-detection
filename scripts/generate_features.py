import pandas as pd
import math
import numpy as np
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import time


class FeatureGenerate:

	def __init__(self):
		self.reviews = self.read_data()
		start = time.time()
		self.cosine_similar()
		self.review_length()
		self.maximum_number_of_reviews_ratio() 
		self.activity_window()
		self.review_count()
		self.positive_review_rating_ratio()
		self.negative_review_rating_ratio()
		self.ratio_of_first_review()
		self.single_product_reviews()
		self.rating_deviation()
		self.extreme_rating()
		self.ratio_of_capital_letters()
		self.save_data()



	def read_data(self):
		# time returns the current time in seconds since the Epoch. (January 1st, 1970)
		start = time.time()
		# read the data and return it
		return pd.read_csv('../Data/reviews.csv')
		

	def save_data(self):
		# save the data with new features in Data folder
		self.reviews.to_csv('../Data/features.csv')
		# calculate the end time for generating all features
		end = time.time()
		print("Total time for calculating all features " + "=" + str(end))
     
	def cosine_similar(self):
		start = time.time()
		# groupby object for getting reviews per user
		reviews_per_user = self.reviews.groupby('reviewerID')['asin','reviewText']
		# stopwords include my,is etc which should be removed
		sw  = stopwords.words('english')
		# cosine dictionary is used to generate the key value pair for review text and cosine of it
		cosine_dictionary = {}
		# iterating group object
		for name,review in reviews_per_user:
			reviews = review['reviewText'].reset_index()
			# dropping the index column
			reviews = reviews.drop(columns=['index'])
			# unique words in all reviews
			unique_words = set()
			for review in reviews['reviewText']:
				for word in review.split(' '):
					unique_words.add(word)
			# set difference method for removing stopwords
			unique_words -= set(sw)
			# vector format 1 for words present , 0 for absent for all reviews
			vector = []
			for i in range(len(reviews['reviewText'])):
				words_present = []
				for w in unique_words:
					if w in reviews['reviewText'][i]:
						words_present.append(1)
					else:
						words_present.append(0)
				vector.append(words_present)
			# dataframe object from vector
			df = pd.DataFrame(vector,columns=list(unique_words))
			# print(df)
			# finding maximum cosine similarity a sentence has with any other sentence for each user
			cosine_distance = cosine_similarity(df, df)
			# sort it along the columns       
			cosine_distance_sorted = np.sort(cosine_distance,axis=1)
			for i in range(len(reviews['reviewText'])):
				# In every column the cosine value 1 will be present as cosine is calculated for each review with itself also
				# In np.sort the largest value of 1 will be the last one so we should take second last for each
				cosine_dictionary[str(reviews['reviewText'][i])] = cosine_distance_sorted[i,-2:-1][0]
				# print(cosine_dictionary[str(reviews['reviewText'][i])])
		cos_similar = []
		for index,row in self.reviews.iterrows():
			cos_similar.append(cosine_dictionary[str(row['reviewText'])])
		# print(self.reviews['cosineSimilarity'])
		self.reviews['cosineSimilarity'] = cos_similar
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed cosine_similar')

	def mark_spam_reviewlength(self,x):
		# threshold = 400 , 1- spam , 0-not spam
		if x > 400:
			return 1
		else:
			return 0

	def review_length(self):
		start = time.time()
		# number of characters
		self.reviews['reviewLength'] = self.reviews['reviewText'].str.len()
		self.reviews['reviewLength'] = self.reviews['reviewLength'].apply(self.mark_spam_reviewlength)
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed review length')
		

	def maximum_number_of_reviews_ratio(self):
		start = time.time()
		# Number of reviews written by users  on a particular day
		reviews_per_user_per_day = self.reviews.groupby(['unixReviewTime','reviewerID'])['asin'].agg(['count']).reset_index()
		#  the ratio of the total number of reviews of an author by the maximum number of reviews
		#  posted by that author in previous days
		mr_ratio = []
		for index,row in self.reviews.iterrows():
			reviewerID = row['reviewerID']
			date = row['unixReviewTime']
			reviews_on_that_day = reviews_per_user_per_day[(reviews_per_user_per_day['reviewerID']==reviewerID) & (reviews_per_user_per_day['unixReviewTime']==date)]['count'].item()
			# print(reviews_on_that_day)
			reviews_before_that_day = reviews_per_user_per_day[(reviews_per_user_per_day['reviewerID']==reviewerID) & (reviews_per_user_per_day['unixReviewTime']<date)]['count'].max()
			# print(reviews_before_that_day)
			# if no previous reviews were written
			if math.isnan(float(reviews_before_that_day)):
				mr_ratio.append(reviews_on_that_day)
			else:
				mr_ratio.append(reviews_on_that_day/reviews_before_that_day)
		self.reviews['maximumReviewsCountRatio'] = mr_ratio
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed mnr ratio')

	def mark_spam_activedays(Self,x):
		# threshold for spammer is that it is generally active for less than 45 days
		if x < 45:
			return 1
		else:
			return 0

	def activity_window(self):
		start = time.time()
		# the number of active days for each reviewer on the basis of the first and last review posted
		reviewer_timeline = self.reviews.groupby('reviewerID')['unixReviewTime'].agg(['min', 'max']).reset_index()
		reviewer_timeline['min'] = pd.to_datetime(reviewer_timeline['min'])
		reviewer_timeline['max'] = pd.to_datetime(reviewer_timeline['max'])
		reviewer_timeline['active_days'] = (reviewer_timeline['max'] - reviewer_timeline['min']).dt.days
		# print(reviewer_timeline['active_days'])
		active_days = []
		for reviewerID in self.reviews['reviewerID']:
			active_days.append(reviewer_timeline[reviewer_timeline['reviewerID']==reviewerID]['active_days'].item())
		self.reviews['activeDays'] = active_days
		self.reviews['activeDays'] = self.reviews['activeDays'].apply(self.mark_spam_activedays)
		end = time.time()
		print('Total time ' + str(end-start))
		print('executed activity window')

	def mark_spam_reviewcount(Self,x):
		# threshold for spammer is that it generally writes less than 5 reviews
		if x < 5:
			return 1
		else:
			return 0

	def review_count(self):
		start = time.time()
		# if tbe total number of reviews are less it maybe from a spammer
		total_reviews_by_reviewer = self.reviews.groupby('reviewerID')['asin'].agg(['count']).reset_index()
		review_count = []
		for reviewerID in self.reviews['reviewerID']:
			review_count.append(total_reviews_by_reviewer[total_reviews_by_reviewer['reviewerID']==reviewerID]['count'].item())
		self.reviews['reviewCount'] = review_count
		self.reviews['reviewCount'] = self.reviews['reviewCount'].apply(self.mark_spam_activedays)
		end = time.time()
		print('Time Taken '+ str(end-start))
		print('executed review count')

	def positive_review_rating_ratio(self):
		start = time.time()
		# all the reviews for a reviewer with rating greater than 3
		rating_by_products = self.reviews.groupby('reviewerID').apply(lambda g:g['overall'] >=4).reset_index()
		# sum of number of positive reviews for each reviewer
		rating_by_products = rating_by_products.groupby('reviewerID').sum().reset_index()
		rating_by_products.drop(columns=['level_1'],inplace=True)
		# total reviews for reviewer	
		total_reviews_by_reviewer = self.reviews.groupby('reviewerID')['overall'].agg(['count']).reset_index()
		positive_rating_ratio = []
		for reviewerID in self.reviews['reviewerID']:
			positive_rating_count = rating_by_products[rating_by_products['reviewerID']==reviewerID]['overall'].item()
			total_reviews_count = total_reviews_by_reviewer[total_reviews_by_reviewer['reviewerID']==reviewerID]['count'].item()
			positive_rating_ratio.append(positive_rating_count /total_reviews_count)
		self.reviews['positiveRatingRatio'] = positive_rating_ratio
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed positive review rating ratio')

	def negative_review_rating_ratio(self):
		start = time.time()
		# all the reviews for a reviewer with rating less than 3
		rating_by_products = self.reviews.groupby('reviewerID').apply(lambda g:g['overall'] <3).reset_index()
		# sum of number of negative reviews
		rating_by_products = rating_by_products.groupby('reviewerID').sum().reset_index()
		rating_by_products.drop(columns=['level_1'],inplace=True)
		# total reviews for reviewer
		total_reviews_by_reviewer = self.reviews.groupby('reviewerID')['overall'].agg(['count']).reset_index()
		negative_rating_ratio = []
		for reviewerID in self.reviews['reviewerID']:
			negative_rating_count = rating_by_products[rating_by_products['reviewerID']==reviewerID]['overall'].item()
			total_reviews_count = total_reviews_by_reviewer[total_reviews_by_reviewer['reviewerID']==reviewerID]['count'].item()
			negative_rating_ratio.append(negative_rating_count /total_reviews_count)
		self.reviews['negativeRatingRatio'] = negative_rating_ratio
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed negative review rating ratio')
		
	def ratio_of_first_review(self):
		start = time.time()
		# group by each product and date and find the first person to review using min
		g = self.reviews.groupby(['asin','unixReviewTime'])['reviewerID'].agg(['min'])
		# level 0 here indicates first index in multiindex that is asin(the product numer in this case)
		# for each product we get the first person to review 
		# here min is the reviewerID
		g = g['min'].groupby(level=0).head(1).reset_index()
		# groupby reviewerID to get the count of times a reviewer was the first one to review the product
		FirstReviewCount= g.groupby('min')['asin'].agg(['count']).reset_index()
		# rename
		FirstReviewCount = FirstReviewCount.rename(columns={'min':'ReviewerId'})
		# total count of reviews for that user
		total_reviews_by_reviewer = self.reviews.groupby('reviewerID')['overall'].agg(['count']).reset_index()
		ratio_of_first_review = []
		for reviewerID in self.reviews['reviewerID']:
			first_review_count = FirstReviewCount[FirstReviewCount['ReviewerId']==reviewerID]['count'].values
			total_review_count = total_reviews_by_reviewer[total_reviews_by_reviewer['reviewerID']==reviewerID]['count'].values
			# print(total_review_count)
			if len(first_review_count) == 0:
				ratio_of_first_review.append(0)
			else:
				ratio_of_first_review.append(first_review_count[0]/total_review_count[0])
			# print(ratio_of_first_review)
		self.reviews['ratioFirstReview'] = ratio_of_first_review
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed ratio of first reviews')

	def single_product_reviews(self):
		start = time.time()
        # total number of reviews
		total_reviews = self.reviews.groupby('reviewerID')['asin'].agg(['count']).reset_index()
		# when total reviews are 1
		single_review = total_reviews.groupby('reviewerID').apply(lambda g:g['count'] == 1).reset_index()
		single_review .drop(columns=['level_1'],inplace=True)
		single_reviews = []
		for reviewerID in self.reviews['reviewerID']:
			if single_review[single_review['reviewerID']==reviewerID]['count'].item():
				single_reviews.append(1)
			else:
				single_reviews.append(0)
		self.reviews['singleReviews'] = single_reviews
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed single product reviews')

	def rating_deviation(self):
		start = time.time()
		# mean ratings for each product
		mean_ratings_per_product = self.reviews.groupby('asin')['overall'].agg(['mean']).reset_index()
		rating_deviate = []
		for index,row in self.reviews.iterrows():
			asin = row['asin']
			rating_deviate.append(np.abs(row['overall']-mean_ratings_per_product[mean_ratings_per_product['asin']==asin]['mean'].item())/4)
		self.reviews['ratingDeviation'] = rating_deviate
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed rating deviation')

	def extreme_rating(self):
		start = time.time()
		extreme_ratings = []
		for rating in self.reviews['overall']:
			if rating == 5 or rating == 1:
				extreme_ratings.append(1)
			else:
				extreme_ratings.append(0)
		self.reviews['extremeRating'] = extreme_ratings
		end = time.time()
		print('Time taken ' + str(end-start))
		print('executed extreme ratings')

	def ratio_of_capital_letters(self):
		start = time.time()
		upper_characters = self.reviews['reviewText'].str.count(r'[A-Z]')
		# print(upper_characters)
		total_characters = self.reviews['reviewText'].str.len()
		print(total_characters)
		self.reviews['ratioCapitalLetters'] = np.abs(upper_characters-total_characters)/total_characters
		end = time.time()
		print('Time taken '+str(end-start))
		print('executed ratio of capital letters')

		



 


Feature = FeatureGenerate()