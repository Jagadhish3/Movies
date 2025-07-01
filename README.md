# Movie Recommendation System

This is a content-based Movie Recommendation System built using Python, Pandas, Scikit-learn, and Streamlit. The system recommends movies based on the similarity of features like cast, crew, keywords, genres, and overview.

## Features

-  Content-based filtering using cosine similarity
-  Interactive UI built with Streamlit
-  Recommendations based on movie metadata
-  Real-time search functionality
-  Integrated TMDB API to fetch movie posters

---

## How It Works

The system uses a combination of:

- **Overview**
- **Genres**
- **Keywords**
- **Cast**
- **Crew**

These features are combined into a single string and vectorized using `CountVectorizer`. Cosine similarity is then computed between all pairs of movies.

---

##  Dataset

The dataset used is from [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata), which includes:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

Make sure both CSV files are in the same directory as your script.

---

## 🖥 Installation & Running Locally

### ⚙ Requirements

- Python 3.x
- `pandas`
- `numpy`
- `scikit-learn`
- `streamlit`
- `requests`

###  Install dependencies

```bash
pip install -r requirements.txt
