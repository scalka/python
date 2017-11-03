import pandas
import webbrowser
import os

# Read the dataset into a data table using Pandas
#index_col="movie_id"  --- use movie_id as an index instead of adding new indexx
data_table = pandas.read_csv("recipes.csv", index_col="recipe_id")

# Create a web page view of the data for easy viewing
html = data_table.to_html()

# Save the html to a temporary file
with open("recipe_list.html", "w", encoding='utf-8') as f:
    f.write(html)

# Open the web page in our web browser
full_filename = os.path.abspath("recipe_list.html")
webbrowser.open("file://{}".format(full_filename))