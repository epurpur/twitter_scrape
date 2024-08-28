import pandas as pd

## read in files for each year

one = pd.read_csv("/Users/ep9k/Desktop/twitter_scrape/DataClean/2023_early.csv")
two = pd.read_csv("/Users/ep9k/Desktop/twitter_scrape/DataClean/2023_late.csv")


df_list = [one, two]

# concatenate list of DFs
combined_df = pd.concat(df_list, ignore_index=True)

# drop duplicate rows
combined_df.drop_duplicates(inplace=True)

# export to dataframe
combined_df.to_csv("/Users/ep9k/Desktop/twitter_scrape/DataClean/2023_combined_final.csv")