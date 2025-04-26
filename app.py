from flask import Flask, request, jsonify, render_template_string
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
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Recommendations</title>
    <style>
        :root {
            --primary: #6c5ce7;
            --secondary: #a29bfe;
            --dark: #2d3436;
            --light: #f5f6fa;
            --accent: #fd79a8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--dark);
            color: var(--light);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: var(--primary);
        }

        .search-box {
            display: flex;
            margin-bottom: 2rem;
        }

        #movie-input {
            flex: 1;
            padding: 0.8rem 1rem;
            border: none;
            border-radius: 4px 0 0 4px;
            font-size: 1rem;
        }

        #search-btn {
            padding: 0 1.5rem;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 0 4px 4px 0;
            cursor: pointer;
            font-weight: bold;
        }

        #search-btn:hover {
            background-color: var(--secondary);
        }

        .results {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1rem;
        }

        .movie-list {
            list-style-type: none;
        }

        .movie-item {
            padding: 0.8rem 1rem;
            margin: 0.5rem 0;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            transition: background-color 0.2s;
        }

        .movie-item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .loading {
            text-align: center;
            padding: 1rem;
            display: none;
        }

        .popular-movies {
            margin-top: 2rem;
        }

        .popular-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .popular-item {
            padding: 0.5rem 1rem;
            background-color: rgba(108, 92, 231, 0.2);
            border-radius: 4px;
            cursor: pointer;
        }

        .popular-item:hover {
            background-color: rgba(108, 92, 231, 0.3);
        }

        @media (max-width: 600px) {
            body {
                padding: 1rem;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Movie Recommender</h1>
            <p>Get recommendations based on your favorite movies</p>
        </header>

        <div class="search-box">
            <input type="text" id="movie-input" placeholder="Enter a movie you like...">
            <button id="search-btn">Search</button>
        </div>

        <div class="results" id="results">
            <div class="no-results">
                <p>Search for a movie to get recommendations</p>
                <p>Try: "The Shawshank Redemption", "Inception", "The Dark Knight"</p>
            </div>
        </div>

        <div class="popular-movies">
            <h2>Popular Movies</h2>
            <div class="popular-list" id="popular-movies">
                <!-- Popular movies will be added here by JavaScript -->
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Display popular movies
            const popularMovies = [
                "The Shawshank Redemption", 
                "The Godfather", 
                "The Dark Knight", 
                "Pulp Fiction", 
                "Inception",
                "Interstellar",
                "Fight Club",
                "Forrest Gump",
                "The Matrix",
                "Titanic"
            ];
            
            const popularContainer = document.getElementById('popular-movies');
            popularMovies.forEach(movie => {
                const item = document.createElement('div');
                item.className = 'popular-item';
                item.textContent = movie;
                item.addEventListener('click', () => {
                    document.getElementById('movie-input').value = movie;
                    getRecommendations();
                });
                popularContainer.appendChild(item);
            });

            // Set up search button
            document.getElementById('search-btn').addEventListener('click', getRecommendations);
            
            // Also search on Enter key
            document.getElementById('movie-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    getRecommendations();
                }
            });
        });

        function getRecommendations() {
            const movieTitle = document.getElementById('movie-input').value.trim();
            if (!movieTitle) return;
            
            const resultsContainer = document.getElementById('results');
            resultsContainer.innerHTML = `
                <div class="loading">
                    <p>Finding recommendations for "${movieTitle}"...</p>
                </div>
            `;
            
            fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `movie_title=${encodeURIComponent(movieTitle)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.recommendations && data.recommendations.length > 0) {
                    const list = document.createElement('ul');
                    list.className = 'movie-list';
                    
                    data.recommendations.forEach(movie => {
                        const item = document.createElement('li');
                        item.className = 'movie-item';
                        item.textContent = movie;
                        list.appendChild(item);
                    });
                    
                    resultsContainer.innerHTML = '';
                    resultsContainer.appendChild(list);
                } else {
                    resultsContainer.innerHTML = `
                        <div class="no-results">
                            <p>No recommendations found for "${movieTitle}". Try another movie!</p>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultsContainer.innerHTML = `
                    <div class="no-results">
                        <p>Error fetching recommendations. Please try again later.</p>
                    </div>
                `;
            });
        }
    </script>
</body>
</html>
    ''')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommendations = movies.get(movie_title, [])
    
    if not recommendations:
        # If movie not found, return some random popular movies
        popular_movies = list(movies.keys())
        recommendations = random.sample(popular_movies, min(5, len(popular_movies)))
    
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')