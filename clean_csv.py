


import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/2013_tweets.csv')

# Assuming 'ImageUrls' is the column containing string representations of lists
df['ImageUrls'] = df['ImageUrls'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['ImageUrls'] = df['ImageUrls'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)

# Assuming 'VideoUrls' is the column containing string representations of lists
df['VideoUrls'] = df['VideoUrls'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['VideoUrls'] = df['VideoUrls'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)


# Overwrite the CSV file with the updated DataFrame
df.to_csv('/Users/ep9k/Desktop/twitter_scrape/2013_tweets_all.csv', index=False)
