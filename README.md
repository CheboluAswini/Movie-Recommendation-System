# 🎬 Semantic Movie Search Engine & Recommender System

A full-stack, containerized Movie Recommendation System and Semantic Search Engine. This application allows users to find movie recommendations using natural language descriptions (Semantic Search) powered by AI sentence embeddings, or via traditional movie-to-movie similarity.

---

## 🏗️ Project Architecture

The project is divided into an interchangeable frontend and backend, communicating via REST API:

- **Frontend (`app.py`)**: A purely interactive UI built with **Streamlit**. It fetches movie data and recommendations from the backend APIs.
- **Backend (`api.py`)**: A robust REST API built with **FastAPI**. It handles all the heavy lifting: loading Machine Learning models, generating sentence embeddings, computing cosine similarity, and fetching movie posters from TMDB.
- **Machine Learning**: Utilizes `sentence-transformers` (`all-MiniLM-L6-v2`) to turn text down into rich semantic embeddings, and `scikit-learn` to calculate vectors' cosine similarity.

---

## 📂 Project Structure

```text
📦 Movie Recommender system
 ┣ 📜 api.py                       # FastAPI Backend Server
 ┣ 📜 app.py                       # Streamlit Frontend UI
 ┣ 📜 embed_movies.py              # Script to generate movie embeddings (ETL)
 ┣ 📜 movie-recommender-system.ipynb # EDA, data cleaning & model training notebook
 ┣ 📜 requirements.txt             # Python dependencies
 ┣ 📜 docker-compose.yml           # Docker Compose configuration 
 ┣ 📜 Dockerfile.backend           # Docker instructions for the backend service
 ┣ 📜 Dockerfile.frontend          # Docker instructions for the frontend service
 ┣ 📜 tmdb_5000_credits.csv        # Raw dataset (Credits)
 ┗ 📜 tmdb_5000_movies.csv         # Raw dataset (Movies)
```

*(Note: Data structures like `.pkl` files and `__pycache__` are excluded via `.gitignore` for space optimization but are generated locally during the ETL phase.)*

---

## ✨ Features

- **Semantic Search**: Type a concept, plot description, or mood (e.g., *"A group of astronauts travel through a wormhole"*), and the engine accurately fetches relevant movies.
- **Microservices Architecture**: The frontend and backend run as separated, decoupled services.
- **Dockerized**: A single command spins up both frontend and backend seamlessly using Docker Compose.
- **FastAPI Documentation**: Interactive API testing via auto-generated Swagger UI.

---

## 🚀 Getting Started

### 1. Prerequisites
- [TMDB API Key](https://developer.themoviedb.org/docs/getting-started) (You need this to fetch beautiful movie posters).
- [Docker & Docker Compose](https://www.docker.com/) (For containerized setup).
- Python 3.9+ (For local setup).

### 2. Creating the Pickles (Feature engineering)
Before running the server, the raw TMDB CSV files need to be processed to extract embeddings.
1. Install requirements locally: `pip install -r requirements.txt`
2. Run the notebook `movie-recommender-system.ipynb` OR execute `python embed_movies.py`.
3. Ensure that `movie_dict.pkl` and `embeddings.pkl` are generated in the root directory.

---

## 🐳 Running with Docker (Recommended)

The easiest way to run the entire stack is with Docker Compose. This creates an isolated network linking the Streamlit frontend with the Fastapi backend.

```bash
# Build and run the services natively
docker-compose up --build
```
- The **Frontend** will be available at: [http://localhost:8501](http://localhost:8501)
- The **Backend API** will be available at: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

---

## 💻 Running Locally (Manual Setup)

If you prefer testing services one by one on your machine:

1. **Activate your virtual environment** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI Backend**:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

3. **Start the Streamlit Frontend** (in a new terminal):
   ```bash
   streamlit run app.py
   ```

---

## 🗄️ Dataset
This project uses the famous **TMDB 5000 Movie Dataset** available on Kaggle. It contains rich metadata and cast/crew information for ~5000 movies.

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
