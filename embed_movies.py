import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer

print("Loading movie data...")
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

print("Loading Sentence Transformer model...")
# all-MiniLM-L6-v2 is a fast and small model ideal for this
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Generating embeddings for all movies based on their tags...")
# We embed the 'tags' column which contains overview, cast, director, genres, etc.
movie_tags = movies['tags'].tolist()
embeddings = model.encode(movie_tags, show_progress_bar=True)

print("Saving embeddings...")
pickle.dump(embeddings, open('embeddings.pkl', 'wb'))
print("Done! You can now use Semantic Search.")
