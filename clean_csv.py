


import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('/Users/ep9k/Desktop/twitter_scrape/Data/2023_early.csv')

#drop "Unnamed:0" column
df = df.drop(columns=['Unnamed: 0'])

# Assuming 'ImageUrls' is the column containing string representations of lists
df['ImageUrls'] = df['ImageUrls'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['ImageUrls'] = df['ImageUrls'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)

# Assuming 'VideoUrls' is the column containing string representations of lists
df['VideoUrls'] = df['VideoUrls'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['VideoUrls'] = df['VideoUrls'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)

# Remove duplicate rows
df = df.drop_duplicates()


# Overwrite the CSV file with the updated DataFrame
df.to_csv('/Users/ep9k/Desktop/twitter_scrape/DataClean/2023_early.csv', index=False)
