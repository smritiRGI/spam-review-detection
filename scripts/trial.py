import pandas as pd 

reviews = pd.read_csv('../Data/reviews.csv')
g = reviews.groupby('reviewerID')['asin'].agg(['count'])
print(g[g['count']==1])