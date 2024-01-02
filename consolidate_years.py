import pandas as pd

## read in files

one_2023 = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2023_tweets.csv')
# two_2022 = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2022_tweets_2.csv')
# three_2019 = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2019_tweets_3.csv')
# four_2018 = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2018_tweets_4.csv')
# five_2017 = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2017_tweets_5.csv')
# six_2017 = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2017_tweets_6.csv')

all_tweets = one_2023
# all_tweets = [one_2022, two_2022]
# all_tweets = pd.concat(all_tweets, ignore_index=True) #506244
all_tweets.drop('Unnamed: 0', axis=1, inplace=True)
all_tweets = all_tweets.drop_duplicates()  #279642


# # Remove filenames containing '_x96' from the 'ImageUrls' column
all_tweets['ImageUrls'] = all_tweets['ImageUrls'].apply(lambda x: eval(x) if isinstance(x, str) else x)
all_tweets['ImageUrls'] = all_tweets['ImageUrls'].apply(lambda x: [item for item in x if '_normal' not in item and '_mini' not in item] if isinstance(x, list) else x)
# all_tweets['ImageUrls'] = all_tweets['ImageUrls'].apply(lambda x: [item for item in x if '_x96' not in item] if isinstance(x, list) else x)





# # export to final file
all_tweets.to_csv('/Users/ep9k/Desktop/twitter_scrape/2023_tweets.csv')