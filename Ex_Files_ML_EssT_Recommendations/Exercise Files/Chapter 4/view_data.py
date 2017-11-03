import pandas
import webbrowser
import os

# Read the dataset into a data table using Pandas
#data_table = pandas.read_csv("movie_ratings_data_set.csv")

data_table = pandas.read_csv("recipe_ratings_data_set.csv")

# Create a web page view of the data for easy viewing
#grab first 100 rows of data
#.to_html() convert data to a webpage to view data
html = data_table[0:100].to_html()


# Save the html to a temporary file
with open("data.html", "w", encoding='utf-8') as f:
    f.write(html)

# Open the web page in our web browser
full_filename = os.path.abspath("data.html")
webbrowser.open("file://{}".format(full_filename))