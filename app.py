import streamlit as st
import requests
import os

# Link to the Backend API
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Semantic Movie Search Engine")

@st.cache_data
def get_movie_list():
    try:
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            return response.json()["movies"]
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Please ensure api.py is running on port 8000.")
    return []

movie_list = get_movie_list()

# Free-text search bar
user_query = st.text_input("Describe the kind of movie you want to watch (e.g. 'A space alien attacks earth'):")

if st.button("Search AI"):
    if user_query:
        with st.spinner("Brainstorming..."):
            response = requests.post(f"{API_URL}/search", json={"query": user_query})
            if response.status_code == 200:
                results = response.json()["results"]
                
                cols = st.columns(5)
                for col, res in zip(cols, results):
                    with col:
                        st.text(res["title"])
                        st.image(res["poster"])
            else:
                st.error("An error occurred with the API.")
    else:
        st.warning("Please type a description first!")

st.markdown("---")
st.subheader("Or choose a specific movie:")

if movie_list:
    selected_movie_name = st.selectbox("Choose a movie", movie_list)

    if st.button("Recommend Similar"):
        with st.spinner("Finding similar movies..."):
            response = requests.post(f"{API_URL}/recommend", json={"movie_title": selected_movie_name})
            
            if response.status_code == 200:
                results = response.json()["results"]
                cols = st.columns(5)
                for col, res in zip(cols, results):
                    with col:
                        st.text(res["title"])
                        st.image(res["poster"])
            else:
                st.error("Failed to get recommendations.")