from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from surprise import Dataset, Reader, SVD

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Load movie and ratings data
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Helper to get movie ID
def get_movie_id(movie_title):
    try:
        movie_id = movies[movies["title"].str.contains(movie_title, case=False, na=False)].iloc[0]["movieId"]
        return movie_id
    except IndexError:
        return None

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    favorite_movies = data.get("favoriteMovies", [])
    
    # Create pseudo-user ratings
    pseudo_user_id = ratings["userId"].max() + 1
    pseudo_ratings = [
        {"userId": pseudo_user_id, "movieId": get_movie_id(movie), "rating": 5.0} 
        for movie in favorite_movies if get_movie_id(movie)
    ]

    # Merge with existing ratings
    pseudo_df = pd.DataFrame(pseudo_ratings)
    updated_ratings = pd.concat([ratings, pseudo_df], ignore_index=True)

    # Train collaborative filtering model
    reader = Reader(rating_scale=(0.5, 5.0))
    data_surprise = Dataset.load_from_df(updated_ratings[["userId", "movieId", "rating"]], reader)
    trainset = data_surprise.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)

    # Generate recommendations
    all_movie_ids = movies["movieId"].unique()
    recommendations = [
        (m_id, algo.predict(pseudo_user_id, m_id).est)
        for m_id in all_movie_ids if m_id not in pseudo_df["movieId"].values
    ]
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]
    recommendations_titles = [movies[movies["movieId"] == m_id]["title"].values[0] for m_id, _ in recommendations]

    return jsonify({"recommendations": recommendations_titles})

if __name__ == "__main__":
    app.run(debug=True)
