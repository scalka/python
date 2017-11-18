import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matrix_factorization_utilities


raw_dataset = pd.read_csv('recipe_ratings_data_set.csv')
# Load user ratings
raw_training_dataset_df, raw_testing_dataset_df = train_test_split(raw_dataset, test_size=0.)

# Convert the running list of user ratings into a matrix
ratings_training_df = pd.pivot_table(raw_training_dataset_df, index='user_id', columns='recipes_id', aggfunc=np.max)
ratings_testing_df = pd.pivot_table(raw_testing_dataset_df, index='user_id', columns='recipes_id', aggfunc=np.max)

# Apply matrix factorization to find the latent features
U, M = matrix_factorization_utilities.low_rank_matrix_factorization(ratings_training_df.as_matrix(),
                                                                    num_features=15,
                                                                    regularization_amount=0.1)
# Find all predicted ratings by multiplying U and M
predicted_ratings = np.matmul(U, M)

# Measure RMSE
rmse_training = matrix_factorization_utilities.RMSE(ratings_training_df.as_matrix(),
                                                    predicted_ratings)


rmse_testing = matrix_factorization_utilities.RMSE(ratings_testing_df.as_matrix(),
                                                   predicted_ratings)

print("Training RMSE: {}".format(rmse_training))
print("Testing RMSE: {}".format(rmse_testing))