
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
        item.innerHTML = `<i class="fas fa-film"></i> ${movie}`;
        item.addEventListener('click', () => {
            document.getElementById('movie-input').value = movie;
            getRecommendations();
            addToRecentSearches(movie);
        });
        popularContainer.appendChild(item);
    });

    // Set up search button
    document.getElementById('search-btn').addEventListener('click', function() {
        const movieTitle = document.getElementById('movie-input').value.trim();
        if (movieTitle) {
            getRecommendations();
            addToRecentSearches(movieTitle);
        }
    });
    
    // Search on Enter key
    document.getElementById('movie-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const movieTitle = this.value.trim();
            if (movieTitle) {
                getRecommendations();
                addToRecentSearches(movieTitle);
            }
        }
    });

    // Autocomplete functionality
    const movieInput = document.getElementById('movie-input');
    const autocomplete = document.getElementById('autocomplete');
    
    movieInput.addEventListener('input', function() {
        const input = this.value.trim().toLowerCase();
        autocomplete.innerHTML = '';
        
        if (input.length < 2) {
            autocomplete.style.display = 'none';
            return;
        }
        
        const matches = popularMovies.filter(movie => 
            movie.toLowerCase().includes(input)
        );
        
        if (matches.length > 0) {
            matches.slice(0, 5).forEach(movie => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.textContent = movie;
                item.addEventListener('click', function() {
                    movieInput.value = movie;
                    autocomplete.style.display = 'none';
                    getRecommendations();
                    addToRecentSearches(movie);
                });
                autocomplete.appendChild(item);
            });
            autocomplete.style.display = 'block';
        } else {
            autocomplete.style.display = 'none';
        }
    });
    
    // Hide autocomplete when clicking elsewhere
    document.addEventListener('click', function(e) {
        if (e.target !== movieInput) {
            autocomplete.style.display = 'none';
        }
    });
});

function getRecommendations() {
    const movieTitle = document.getElementById('movie-input').value.trim();
    if (!movieTitle) return;
    
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
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
                // Add random rating for visual appeal (in a real app, this would come from your data)
                const rating = (Math.random() * 2 + 3).toFixed(1);
                item.innerHTML = `
                    <span>${movie}</span>
                    <span class="rating">${rating} <i class="fas fa-star"></i></span>
                `;
                list.appendChild(item);
            });
            
            resultsContainer.innerHTML = '';
            resultsContainer.appendChild(list);
        } else {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-exclamation-circle icon-large"></i>
                    <p>No recommendations found for "${movieTitle}". Try another movie!</p>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultsContainer.innerHTML = `
            <div class="no-results">
                <i class="fas fa-exclamation-triangle icon-large"></i>
                <p>Error fetching recommendations. Please try again later.</p>
            </div>
        `;
    });
}

function addToRecentSearches(movieTitle) {
    let recentSearches = JSON.parse(localStorage.getItem('recentSearches')) || [];
    
    // Remove if already exists
    recentSearches = recentSearches.filter(movie => movie !== movieTitle);
    
    // Add to beginning
    recentSearches.unshift(movieTitle);
    
    // Keep only last 5 searches
    if (recentSearches.length > 5) {
        recentSearches = recentSearches.slice(0, 5);
    }
    
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
    displayRecentSearches();
}

function displayRecentSearches() {
    const recentSearches = JSON.parse(localStorage.getItem('recentSearches')) || [];
    const recentContainer = document.getElementById('recent-searches');
    recentContainer.innerHTML = '';
    
    recentSearches.forEach(movie => {
        const item = document.createElement('div');
        item.className = 'recent-item';
        item.innerHTML = `<i class="fas fa-history"></i> ${movie}`;
        item.addEventListener('click', () => {
            document.getElementById('movie-input').value = movie;
            getRecommendations();
        });
        recentContainer.appendChild(item);
    });
}

// Display recent searches on page load
displayRecentSearches();