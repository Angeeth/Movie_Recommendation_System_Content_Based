import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Flixora", layout="wide")


TMDB_API_KEY = "YOUR_API_KEY"
POSTER_URL = "https://image.tmdb.org/t/p/w500"

movies = pd.read_csv("data/processed/movies_processed.csv")

@st.cache_data
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    return requests.get(url).json()

col1, col2 = st.columns([2, 2])

with col1:
    st.markdown("## 🎬 Flixora")

with col2:
    search_movie = st.selectbox(
        "Search",
        movies["title"].values,
        index=None,
        placeholder="Search movie..."
    )

st.divider()


if search_movie:
    movie_row = movies.loc[movies["title"] == search_movie].iloc[0]
    movie_id = int(movie_row["movie_id"])

    details = fetch_movie_details(movie_id)

    if details.get("poster_path"):
        st.image(
            POSTER_URL + details["poster_path"],
            width=220
        )
    
    st.page_link(
        "pages/movie_details.py",
        label="🔍 View Movie",
        query_params={"movie_id": str(movie_id)}
    )


sample_movies = movies.sample(20).reset_index(drop=True)
cols = st.columns(5)

for idx, row in sample_movies.iterrows():
    details = fetch_movie_details(row.movie_id)

    if details.get("poster_path"):
        poster = POSTER_URL + details["poster_path"]
    else:
        poster = None

    with cols[idx % 5]:
        if poster:
            st.image(poster)
        st.caption(row.title)

        st.page_link(
            "pages/movie_details.py",
            label="View",
            query_params={"movie_id": str(row.movie_id)}
        )