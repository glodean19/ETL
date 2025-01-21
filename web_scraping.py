import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = './top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank","Film","Year", "Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

# Iterate over the contents of the variable rows
for row in rows:
    # Check for the loop counter to restrict to 50 entries
    if count<50:
        # Extract all the td data objects in the row and save them to col
        col = row.find_all('td')
        # Check if the length of col is 0, that is, if there is no data in a current row
        if len(col)!=0:
            # Create a dictionary data_dict with the keys same as the columns of 
            # the dataframe created for recording the output earlier and corresponding values from the first three headers of data
            data_dict = {"Average Rank": col[0].contents[0],
                         "Film": col[1].contents[0],
                         "Year": col[2].contents[0],
                         "Rotten Tomatoes' Top 100": col[3].contents[0]}
            # Convert the dictionary to a dataframe and concatenate it with the existing one
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            # Increment the loop counter
            count+=1
    else:
        # Once the counter hits 50, stop iterating over rows and break the loop
        break

'''
# Convert the Year column to integers for filtering
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Filter for films released in the 2000s (2000-2009)
filtered_df = df[(df['Year'] >= 2000) & (df['Year'] < 2010)]

# Print the filtered dataframe
print(filtered_df)

filtered_df.to_csv(csv_path)
'''

# Print the filtered dataframe
print(df)

df.to_csv(csv_path)

conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
