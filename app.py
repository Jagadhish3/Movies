from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Sample movie data
movies = {
    "The Shawshank Redemption": ["The Godfather", "Pulp Fiction", "The Dark Knight", "Fight Club", "Inception"],
    "Inception": ["The Matrix", "Interstellar", "Shutter Island", "Tenet", "Source Code"],
    "The Dark Knight": ["Batman Begins", "The Dark Knight Rises", "Watchmen", "V for Vendetta", "Logan"],
    "Pulp Fiction": ["Reservoir Dogs", "Goodfellas", "Fight Club", "The Godfather", "Scarface"],
    "Interstellar": ["Gravity", "The Martian", "Arrival", "Contact", "2001: A Space Odyssey"],
    "The Godfather": ["Goodfellas", "Scarface", "Casino", "The Departed", "Once Upon a Time in America"],
    "Fight Club": ["American Psycho", "Se7en", "Gone Girl", "The Game", "Donnie Darko"],
    "Forrest Gump": ["The Pursuit of Happyness", "The Green Mile", "Cast Away", "Big Fish", "The Terminal"],
    "The Matrix": ["The Thirteenth Floor", "Dark City", "Inception", "Blade Runner 2049", "Source Code"],
    "Titanic": ["Pearl Harbor", "The Notebook", "A Walk to Remember", "Romeo + Juliet", "Ghost"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommendations = movies.get(movie_title, [])
    
    if not recommendations:
        popular_movies = list(movies.keys())
        recommendations = random.sample(popular_movies, min(5, len(popular_movies)))
    
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)