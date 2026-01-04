#  Flixora – Content-Based Movie Recommendation System

Flixora is a content-based movie recommendation system built using **Python** and **Streamlit**.  
It recommends similar movies based on metadata such as **genres, keywords, cast, crew, and overview**.

The application uses **Bag-of-Words (CountVectorizer)** and **cosine similarity** to compute movie similarity scores and integrates with the **TMDB API** to fetch real-time movie posters and details.

---

##  Features
- Search movies by title
- View detailed movie information (poster, rating, cast, director, overview)
- Get content-based movie recommendations
- Interactive and responsive UI built with Streamlit
- TMDB API integration for live movie data

---

##  Recommendation Approach
- Movie metadata is preprocessed and combined into tags
- Text vectorization using **CountVectorizer**
- Similarity computation using **cosine similarity**
- Precomputed similarity matrix stored using `pickle` for fast inference

---

##  Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **Data Processing:** Pandas, NLTK
- **Machine Learning:** Scikit-learn
- **Visualization:** Plotly
- **API:** TMDB API

---