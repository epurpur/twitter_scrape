import pandas as pd

## read in files

top_tweets = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape_data/2013_tweets_top.csv')


top_tweets.drop('Unnamed: 0', axis=1, inplace=True)
top_tweets = top_tweets.drop_duplicates()  #279642


# # Remove filenames containing '_x96' from the 'ImageUrls' column
top_tweets['ImageUrls'] = top_tweets['ImageUrls'].apply(lambda x: eval(x) if isinstance(x, str) else x)
top_tweets['ImageUrls'] = top_tweets['ImageUrls'].apply(lambda x: [item for item in x if '_normal' not in item and '_mini' not in item] if isinstance(x, list) else x)
top_tweets['ImageUrls'] = top_tweets['ImageUrls'].apply(lambda x: [item for item in x if '_x96' not in item] if isinstance(x, list) else x)





# # export to final file
top_tweets.to_csv('/Users/ep9k/Desktop/twitter_scrape_data/2013_TopTweets.csv')

