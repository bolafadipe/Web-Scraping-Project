import glob
from pathlib import Path
import pandas as pd
path = 'scraper'
files = list(Path('tours_data').glob('*.csv'))
print(len(files))
li = []
for f in files:
    # read in csv
    temp_df = pd.read_csv(f)
    # append df to list
    li.append(temp_df)


df = pd.concat(li, axis=0)
# rename columns
df.columns = ['Title', 'Rating', 'Number_of_ratings',
              'Price(£)', 'Duration(hours)', 'Star_rating', 'Tour_provider']
# clean number_of_ratings column to include only integers
#df['Number_of_ratings'] = df.Number_of_ratings.str.replace('ratings', '')
#df['Price'] = df.Price.str.replace('£', '')
#df['Duration'] = df.Duration.str.replace('hours', '')
df.head(2)


print(df.head(3))
# print(df.info())
