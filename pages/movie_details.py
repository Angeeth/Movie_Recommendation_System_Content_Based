import streamlit as st
import pandas as pd
import requests
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.abspath("src"))
from recommend import recommend

st.set_page_config(page_title="Flixora", layout="wide")


TMDB_API_KEY = "YOUR_API_KEY"
POSTER_URL = "https://image.tmdb.org/t/p/w500"

movies = pd.read_csv("data/processed/movies_processed.csv")

@st.cache_data(ttl=600)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    return requests.get(url).json()

@st.cache_data(ttl=600)
def fetch_cast_director(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()

    cast = [c["name"] for c in data.get("cast", [])[:5]]
    director = ""

    for crew in data.get("crew", []):
        if crew["job"] == "Director":
            director = crew["name"]

    return cast, director

params = st.query_params

if "movie_id" not in params:
    st.error("❌ No movie selected.")
    st.page_link("app.py", label="⬅ Go back to Home")
    st.stop()
movie_id = int(params["movie_id"])

details = fetch_movie_details(movie_id)
cast, director = fetch_cast_director(movie_id)

def rating(rating):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rating,
        number={
            'suffix': " / 10",
            'font': {'size': 36}
            
        },
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "#00E396"},
            'borderwidth': 1
        }
    ))

    fig.update_layout(
        height=200,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    return fig


col1, col2 = st.columns([1, 2])

with col1:
    if details.get("poster_path"):
        st.image(POSTER_URL + details["poster_path"])

with col2:
    st.markdown(f"## {details['title']}")

    st.plotly_chart(
        rating(details["vote_average"]),
        use_container_width=True
    )

    st.write("**Cast:**", ", ".join(cast))
    st.write("**Director:**", director)
    st.write(details["overview"])



    st.page_link("app.py", label="⬅ Back to Home")

st.divider()

st.subheader("Recommended Movies")

recommendations = recommend(details["title"])
rec_cols = st.columns(5)

for i, rec_title in enumerate(recommendations):
    rec_movie = movies[movies["title"] == rec_title].iloc[0]
    rec_details = fetch_movie_details(rec_movie.movie_id)

    with rec_cols[i % 5]:
        if rec_details.get("poster_path"):
            st.image(POSTER_URL + rec_details["poster_path"])

        st.caption(rec_title)

        st.page_link(
            "pages/movie_details.py",
            label="View",
            query_params={"movie_id": str(rec_movie.movie_id)}
        )

