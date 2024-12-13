import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
import streamlit as st

# Load data files
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Check first few rows of each
print(movies.head())
print(ratings.head())


# Merge movies and ratings on movieId
movie_data = pd.merge(ratings, movies, on='movieId')

# Check for missing values
print(movie_data.isnull().sum())


# Setup the dataset for Surprise
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Split into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2)

# Initialize and train the SVD algorithm
algo = SVD()
algo.fit(trainset)

# Make predictions
predictions = algo.test(testset)


# Calculate RMSE
rmse = accuracy.rmse(predictions)
print(f"RMSE: {rmse}")


def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions."""
    # Map the predictions to each user.
    top_n = {}
    for uid, iid, true_r, est, _ in predictions:
        if uid not in top_n:
            top_n[uid] = []
        top_n[uid].append((iid, est))

    # Sort the predictions for each user and retrieve the n highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

# Get top 10 recommendations for each user
top_n = get_top_n(predictions, n=10)


st.title("Movie Recommendation System")

user_id = st.number_input("Enter user ID to get recommendations", min_value=1, step=1)

if st.button("Get Recommendations"):
    # Display recommendations for the user
    if user_id in top_n:
        st.write(f"Top recommendations for User {user_id}:")
        for movie_id, rating in top_n[user_id]:
            movie_name = movies[movies['movieId'] == movie_id]['title'].values[0]
            st.write(f"{movie_name} (Predicted Rating: {rating:.2f})")
    else:
        st.write("No recommendations found for this user.")
