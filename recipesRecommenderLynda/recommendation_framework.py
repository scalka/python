import webbrowser
import os
import pandas as pd
import numpy as np

#READ DATA ABD EXPORT TO HTML
# read dataset into table using Pandas
data_table_ratings = pd.read_csv("recipe_ratings_data_set.csv")

#create a webpage for easy viewing, first 100 rows
html = data_table_ratings[0:100].to_html()

#save the html to temporary file
with open("data_table_ratings.html", "w", encoding='utf-8') as f:
    f.write(html)

#open in a browser
full_filename = os.path.abspath("data_table_ratings.html")
webbrowser.open("file://{}".format(full_filename))

data_table_recipes = pd.read_csv("recipes.csv", index_col="recipes_id")
html = data_table_recipes.to_html()
with open("recipe_data_table.html", "w", encoding='utf-8') as f:
    f.write(html)
full_filename2 = os.path.abspath("recipe_data_table.html")
webbrowser.open("file://{}".format(full_filename2))

#CREATE REVIEW MATRIX

df = data_table_ratings
#convert running list into a matrix using pivot table function
ratings_df = pd.pivot_table(df, index="user_id", columns="recipes_id", aggfunc=np.max)

html = ratings_df.to_html(na_rep="")
with open("review_matrix.html", "w") as f:
    f.write(html)
matrix_filename = os.path.abspath("review_matrix.html")
webbrowser.open("file://{}".format(full_filename))

#CONVERT TO CSV
ratings_df.to_csv("review_matrix.csv", na_rep="")