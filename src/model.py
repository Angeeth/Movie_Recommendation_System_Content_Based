import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def build_model():
    movies = pd.read_csv("data/processed/movies_processed.csv")

    cv = CountVectorizer(max_features=5000,stop_words='english')
    vectors = cv.fit_transform(movies['Tags']).toarray()

    similarity = cosine_similarity(vectors)

    pickle.dump(similarity, open("data/processed/similarity.pkl", "wb"))


if __name__ == "__main__":
    build_model()