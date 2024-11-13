import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

# Load dataset
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Preprocess data
def get_movie_id(movie_title):
    """
    Get the movieId for a given movie title.
    """
    try:
        movie_id = movies[movies['title'].str.contains(movie_title, case=False, na=False)].iloc[0]['movieId']
        return movie_id
    except IndexError:
        print(f"Movie '{movie_title}' not found in the database.")
        return None

def create_pseudo_user_ratings(favorite_movies):
    """
    Create a DataFrame with the pseudo user's ratings based on their favorite movies.
    """
    user_id = ratings['userId'].max() + 1  # Assign a new user ID
    pseudo_ratings = []
    for movie in favorite_movies:
        movie_id = get_movie_id(movie)
        if movie_id:
            pseudo_ratings.append({'userId': user_id, 'movieId': movie_id, 'rating': 5.0})  # Giving a max rating for favorites
    return pd.DataFrame(pseudo_ratings)

# Interactive user input
def get_user_input():
    print("Welcome to the Movie Recommendation System!")
    user_name = input("Please enter your name: ")
    print(f"Hi {user_name}! Please enter your 10 favorite movies, one by one.")
    
    favorite_movies = []
    for i in range(10):
        movie_title = input(f"Enter favorite movie {i+1}: ")
        favorite_movies.append(movie_title)
    
    return favorite_movies

# Train and make recommendations
def make_recommendations(favorite_movies):
    # Create pseudo-user's ratings and add them to the original ratings
    pseudo_user_ratings = create_pseudo_user_ratings(favorite_movies)
    updated_ratings = pd.concat([ratings, pseudo_user_ratings], ignore_index=True)

    # Prepare data for collaborative filtering
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(updated_ratings[['userId', 'movieId', 'rating']], reader)

    # Split dataset and train the model
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)

    # Get recommendations for the pseudo user
    pseudo_user_id = updated_ratings['userId'].max()  # The new pseudo user ID
    movie_ids = movies['movieId'].unique()
    recommendations = []
    
    for movie_id in movie_ids:
        if movie_id not in pseudo_user_ratings['movieId'].values:
            pred = algo.predict(pseudo_user_id, movie_id)
            recommendations.append((movie_id, pred.est))

    # Sort recommendations by predicted rating
    recommendations.sort(key=lambda x: x[1], reverse=True)
    top_recommendations = recommendations[:10]

    # Display recommendations
    print("\nTop 10 Movie Recommendations for You:")
    for movie_id, rating in top_recommendations:
        movie_title = movies[movies['movieId'] == movie_id]['title'].values[0]
        print(f"{movie_title} - Predicted Rating: {rating:.2f}")

if __name__ == "__main__":
    favorite_movies = get_user_input()
    make_recommendations(favorite_movies)