import numpy as np
import pandas as pd
import matrix_factorization_utilities

# Load user ratings
df = pd.read_csv('recipe_ratings_data_set.csv')

# Load movie titles
recipes_df = pd.read_csv('recipes.csv', index_col='recipes_id')

# Convert the running list of user ratings into a matrix
ratings_df = pd.pivot_table(df, index='user_id', columns='recipes_id', aggfunc=np.max)

# Apply matrix factorization to find the latent features
U, M = matrix_factorization_utilities.low_rank_matrix_factorization(ratings_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=1.0)

# Swap the rows and columns of product_features just so it's easier to work with
M = np.transpose(M)

# Choose a movie to find similar movies to. Let's find movies similar to movie #5:
recipe_id = 3

# Get movie #1's name and genre
recipe_information = recipes_df.loc[recipe_id]

print("We are finding recipes similar to this recipe:")
print("Recipe title: {}".format(recipe_information.title))
print("Category: {}".format(recipe_information.category))

# Get the features for movie #1 we found via matrix factorization
current_recipe_features = M[recipe_id - 1]

print("The attributes for this recipe are:")
print(current_recipe_features)

# The main logic for finding similar movies:

# 1. Subtract the current movie's features from every other movie's features
difference = M - current_recipe_features

# 2. Take the absolute value of that difference (so all numbers are positive)
absolute_difference = np.abs(difference)

# 3. Each movie has 15 features. Sum those 15 features to get a total 'difference score' for each movie
total_difference = np.sum(absolute_difference, axis=1)

# 4. Create a new column in the movie list with the difference score for each movie
recipes_df['difference_score'] = total_difference

# 5. Sort the movie list by difference score, from least different to most different
sorted_movie_list = recipes_df.sort_values('difference_score')

# 6. Print the result, showing the 5 most similar movies to movie_id #1
print("The five most similar movies are:")
print(sorted_movie_list[['title', 'difference_score']][0:5])
