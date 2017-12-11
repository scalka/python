import pandas as pd
import numpy as np
import matrix_factorization_utilities

#load ratings
raw_dataset_ratings_df = pd.read_csv("recipe_ratings_data_set.csv")
#load recipe titles
recipes_df = pd.read_csv("recipes.csv", index_col="recipes_id")

#convert running list of user ratings into matrix
ratings_df = pd.pivot_table(raw_dataset_ratings_df, index="user_id", columns="recipes_id", aggfunc=np.max)
#apply matrxi factorization to find the latent features
#num_features=15,- number of latenet features
# regularixation_amount - more regularization will raise the training score, but it may lower the testing score.
U, R = matrix_factorization_utilities.low_rank_matrix_factorization(ratings_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=0.1)
#find all predicted ratings by multiplying the U by R
# matmul - matrix multiplication
predicted_ratings = np.matmul(U, R)
#save
#predicted_ratings_df = pd.DataFrame(index=ratings_df.index,
 #                                   columns=ratings_df.columns,
 #                                   data=predicted_ratings)
#predicted_ratings_df.to_csv("predicted_ratings.csv")



# FIND SIMILAR PRODUCTS
# Swap the rows and columns of product_features just so it's easier to work with
R = np.transpose(R)

#choose a recipe to find similar to
recipe_id = 6

#get a recipe's title and category
recipe_information = recipes_df.loc[recipe_id]

print("We are finding recipes similar to this recipe:")
print("Recipe title: {}".format(recipe_information.title))
print("Category: {}".format(recipe_information.category))

#get the features for recipe #1 we found via matrix factorization
current_recipe_features = R[recipe_id - 1]

print("The attributes for this recipe are:")
print(current_recipe_features)

#MAIN LOGIC FOR FINDING SIMILAR RECIPES
# 1. Substract the current recipe's features from every recipe's features
difference = R - current_recipe_features

# 2. Take the absoulte value of that diffence (so all numbers are positive)
absolute_difference = np.abs(difference)

# 3. TODO ?? Each recipe has 15 features. . Sum those 15 features to get a total 'difference score' for each recipe
total_difference = np.sum(absolute_difference, axis=1)

# 4. Create a new column in the recipe list with the difference score for each recipe
recipes_df['difference_score'] = total_difference

# 5. Sort the movie list by difference score, from least different to most different
sorted_recipe_list = recipes_df.sort_values("difference_score")

# 6. Print the result, showing the most 5 similar

print("The five most similar recipes are:")
print(sorted_recipe_list[['title', 'difference_score']][0:5])



