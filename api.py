from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the Backend App
app = FastAPI(title="Movie Recommender API", version="1.0")

# 1. Load the Memory & Models (Executes when the server starts)
print("Loading datasets and AI models into server memory...")
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movie_embeddings = pickle.load(open('embeddings.pkl', 'rb'))
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Server ready!")

# 2. Define Data Structures
class SearchRequest(BaseModel):
    query: str

class RecommendRequest(BaseModel):
    movie_title: str

# 3. Helper Functions
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster+Found"

# 4. API Endpoints
@app.get("/movies")
def get_movies():
    """Returns a list of all available movies for the frontend dropdown."""
    return {"movies": movies['title'].tolist()}

@app.post("/search")
def search(request: SearchRequest):
    """Takes a natural language query, computes similarity, and returns top 5 movies."""
    query_vector = model.encode([request.query])
    similarity_scores = cosine_similarity(query_vector, movie_embeddings).flatten()
    top_indices = similarity_scores.argsort()[-5:][::-1]
    
    results = []
    for i in top_indices:
        movie_id = movies.iloc[i].movie_id
        results.append({
            "title": movies.iloc[i].title,
            "poster": fetch_poster(movie_id)
        })
    return {"results": results}

@app.post("/recommend")
def recommend(request: RecommendRequest):
    """Takes an exact movie title, finds similar movies, and returns top 5 matches."""
    match = movies[movies['title'] == request.movie_title]
    if match.empty:
        raise HTTPException(status_code=404, detail="Movie not found in database")
    
    movie_tags = match['tags'].values[0]
    query_vector = model.encode([movie_tags])
    similarity_scores = cosine_similarity(query_vector, movie_embeddings).flatten()
    
    # Skip the exact movie match itself (which would be index -1)
    top_indices = similarity_scores.argsort()[-6:-1][::-1]
    
    results = []
    for i in top_indices:
        movie_id = movies.iloc[i].movie_id
        results.append({
            "title": movies.iloc[i].title,
            "poster": fetch_poster(movie_id)
        })
    return {"results": results}
