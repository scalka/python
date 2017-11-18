import pickle
import pandas as pd

# Load prediction rules from data files
means = pickle.load(open("means.dat", "rb"))

# Load movie titles
recipes_df = pd.read_csv('recipes.csv', index_col='recipes_id')

# Just use the average movie ratings directly as the user's predicted ratings
user_ratings = means

print("Recipes we will recommend:")

recipes_df['rating'] = user_ratings
recipes_df = recipes_df.sort_values(by=['rating'], ascending=False)

print(recipes_df[['title', 'category', 'rating']].head(5))