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