# Movie Recommendation System

This project provides a movie recommendation system using a Flask backend and an Angular frontend. The backend uses collaborative filtering with the Surprise library to generate recommendations based on a user’s favorite movies. The Angular frontend provides a user-friendly interface to input favorite movies and display the recommended titles.

## Overview

The system leverages user-provided favorite movie titles to generate recommendations. It uses a collaborative filtering approach, training on an existing dataset of movies and ratings. The recommended movies are ranked by predicted rating.

## Features

- Enter up to 10 favorite movies.
- Generate top movie recommendations.
- Display the recommended movie titles on the frontend.
- Integrated CORS support for seamless communication between the Angular frontend and Flask backend.

## Tech Stack

- **Backend:**
  - Python 3
  - Flask
  - flask-cors
  - pandas
  - scikit-surprise (Surprise library)

- **Frontend:**
  - Angular
  - TypeScript
  - HTML/CSS

## Prerequisites

- **Python 3.8+** installed on your machine.
- **Node.js and npm** installed for running the Angular frontend.
- **pip** for Python package installation.
- (Optional) **Virtual environment tool** like `venv` or `conda` for Python dependencies.


## Project Structure

project/
  backend/
    app.py
    movies.csv
    ratings.csv
    requirements.txt
  frontend/
    src/
      main.ts
      index.html
      styles.css
      app/
        app.component.ts
        app.component.html
        movie-form/
          movie-form.component.ts
          movie-form.component.html
          movie-form.component.scss
        movie-recommendation.service.ts
    package.json
    angular.json
    tsconfig.json
  README.md



## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

   cd backend
   pip install -r requirements.txt
   pip install flask-cors


### Frontend Setup

cd ../frontend
npm install


### Running the Application

Backend - flask run --port=5001
Frontend - ng serve





