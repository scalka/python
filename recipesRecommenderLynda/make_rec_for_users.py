import pandas as pd
import numpy as np
import pickle
import matrix_factorization_utilities

#load ratings
raw_dataset_ratings_df = pd.read_csv("recipe_ratings_data_set.csv")
#load recipe titles
recipes_df = pd.read_csv("recipes2.csv", index_col="recipes_id")

#convert running list of user ratings into matrix
ratings_df = pd.pivot_table(raw_dataset_ratings_df, index="user_id", columns="recipes_id", aggfunc=np.max)

#apply matrxi factorization to find the latent features
#num_features=15,- number of latenet features
#regularisation_amount - more regularization will raise the training score, but it may lower the testing score.
U, R = matrix_factorization_utilities.low_rank_matrix_factorization(ratings_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=0.1)
#find all predicted ratings by multiplying the U by R
# matmul - matrix multiplication
predicted_ratings = np.matmul(U, R)
#predicted_ratings_df = pd.DataFrame(index=ratings_df.index,
#                                   columns=ratings_df.columns,
#                                   data=predicted_ratings)
#predicted_ratings_df.to_csv("predicted_ratings.csv")

# SAVE FEATURES AND PREDICTED RATINGS TO FILE FOR LATER USE
#pickle.dump(U, open("user_features_recipes2.dat", "wb"))
#pickle.dump(R, open("product_features_recipes2.dat", "wb"))
#pickle.dump(predicted_ratings, open("predicted_ratings_recipes2.dat", "wb"))

print("Enter a user_id to get recommendations (Between 1 and 100):")
user_id_to_search = int(input())

print("Recipe previously reviewed by user_id {}:".format(user_id_to_search))

reviewed_recipes_df = raw_dataset_ratings_df[raw_dataset_ratings_df['user_id'] == user_id_to_search]
reviewed_recipes_df = reviewed_recipes_df.join(recipes_df, on='recipes_id')

print(reviewed_recipes_df[['title', 'value']])

input("Press enter to continue.")

print("Recipes we will recommend:")

user_rating = predicted_ratings[user_id_to_search - 1]
user_ratings_df = pd.DataFrame(user_rating, dtype='str' )
recipes_df['rating_stars'] = user_ratings_df

already_reviewed = reviewed_recipes_df['recipes_id']
recommended_df = recipes_df[recipes_df.index.isin(already_reviewed) == False]
recommended_df = recommended_df.sort_values(by=['rating_stars'], ascending=False)

print(recommended_df[['title', 'rating_stars']].head(5))

