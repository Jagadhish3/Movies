# from flask import Flask, request, jsonify, render_template
# import random

# app = Flask(__name__)

# # Sample movie data
# movies = {
#     "The Shawshank Redemption": ["The Godfather", "Pulp Fiction", "The Dark Knight", "Fight Club", "Inception"],
#     "Inception": ["The Matrix", "Interstellar", "Shutter Island", "Tenet", "Source Code"],
#     "The Dark Knight": ["Batman Begins", "The Dark Knight Rises", "Watchmen", "V for Vendetta", "Logan"],
#     "Pulp Fiction": ["Reservoir Dogs", "Goodfellas", "Fight Club", "The Godfather", "Scarface"],
#     "Interstellar": ["Gravity", "The Martian", "Arrival", "Contact", "2001: A Space Odyssey"],
#     "The Godfather": ["Goodfellas", "Scarface", "Casino", "The Departed", "Once Upon a Time in America"],
#     "Fight Club": ["American Psycho", "Se7en", "Gone Girl", "The Game", "Donnie Darko"],
#     "Forrest Gump": ["The Pursuit of Happyness", "The Green Mile", "Cast Away", "Big Fish", "The Terminal"],
#     "The Matrix": ["The Thirteenth Floor", "Dark City", "Inception", "Blade Runner 2049", "Source Code"],
#     "Titanic": ["Pearl Harbor", "The Notebook", "A Walk to Remember", "Romeo + Juliet", "Ghost"]
# }

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     movie_title = request.form['movie_title']
#     recommendations = movies.get(movie_title, [])
    
#     if not recommendations:
#         popular_movies = list(movies.keys())
#         recommendations = random.sample(popular_movies, min(5, len(popular_movies)))
    
#     return jsonify({'recommendations': recommendations})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0',port=5000)

from flask import Flask, request, jsonify, render_template
import random
from datetime import datetime

app = Flask(__name__)

# Enhanced movie data with genres and years
movies = {
    "The Shawshank Redemption": {
        "recommendations": ["The Godfather", "Pulp Fiction", "The Dark Knight", "Fight Club", "Inception"],
        "genre": "Drama",
        "year": 1994
    },
    "Inception": {
        "recommendations": ["The Matrix", "Interstellar", "Shutter Island", "Tenet", "Source Code"],
        "genre": "Sci-Fi",
        "year": 2010
    },
    "The Dark Knight": {
        "recommendations": ["Batman Begins", "The Dark Knight Rises", "Watchmen", "V for Vendetta", "Logan"],
        "genre": "Action",
        "year": 2008
    },
    "Pulp Fiction": {
        "recommendations": ["Reservoir Dogs", "Goodfellas", "Fight Club", "The Godfather", "Scarface"],
        "genre": "Crime",
        "year": 1994
    },
    "Interstellar": {
        "recommendations": ["Gravity", "The Martian", "Arrival", "Contact", "2001: A Space Odyssey"],
        "genre": "Sci-Fi",
        "year": 2014
    },
    "The Godfather": {
        "recommendations": ["Goodfellas", "Scarface", "Casino", "The Departed", "Once Upon a Time in America"],
        "genre": "Crime",
        "year": 1972
    },
    "Fight Club": {
        "recommendations": ["American Psycho", "Se7en", "Gone Girl", "The Game", "Donnie Darko"],
        "genre": "Drama",
        "year": 1999
    },
    "Forrest Gump": {
        "recommendations": ["The Pursuit of Happyness", "The Green Mile", "Cast Away", "Big Fish", "The Terminal"],
        "genre": "Drama",
        "year": 1994
    },
    "The Matrix": {
        "recommendations": ["The Thirteenth Floor", "Dark City", "Inception", "Blade Runner 2049", "Source Code"],
        "genre": "Sci-Fi",
        "year": 1999
    },
    "Titanic": {
        "recommendations": ["Pearl Harbor", "The Notebook", "A Walk to Remember", "Romeo + Juliet", "Ghost"],
        "genre": "Romance",
        "year": 1997
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    
    # Find the best match (case insensitive)
    matched_movie = None
    for title in movies:
        if movie_title.lower() == title.lower():
            matched_movie = title
            break
    
    if matched_movie:
        movie_data = movies[matched_movie]
        recommendations = movie_data["recommendations"]
        # Add some metadata to the response
        response = {
            'recommendations': recommendations,
            'genre': movie_data["genre"],
            'year': movie_data["year"],
            'matched_title': matched_movie
        }
    else:
        # If no exact match, try to find partial matches
        partial_matches = [title for title in movies if movie_title.lower() in title.lower()]
        
        if partial_matches:
            # Get recommendations from first partial match
            matched_movie = partial_matches[0]
            movie_data = movies[matched_movie]
            recommendations = movie_data["recommendations"]
            response = {
                'recommendations': recommendations,
                'genre': movie_data["genre"],
                'year': movie_data["year"],
                'matched_title': matched_movie,
                'did_you_mean': matched_movie
            }
        else:
            # Fallback to random popular movies
            popular_movies = list(movies.keys())
            recommendations = random.sample(popular_movies, min(5, len(popular_movies)))
            response = {
                'recommendations': recommendations,
                'fallback': True
            }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)