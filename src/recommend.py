import pandas as pd
import pickle

movies = pd.read_csv("data/processed/movies_processed.csv")
similarity = pickle.load(open("data/processed/similarity.pkl", "rb"))

def recommend(movie_title, top_n=5):
    index = movies[movies['title'] == movie_title].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []
    for i in distances[1:top_n+1]:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations

if __name__ == "__main__":
    print(recommend("Batman"))



