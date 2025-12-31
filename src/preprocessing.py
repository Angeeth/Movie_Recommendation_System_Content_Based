import pandas as pd
import ast
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def load_and_merge():
    movies = pd.read_csv("data/raw/tmdb_5000_movies.csv")
    credits = pd.read_csv("data/raw/tmdb_5000_credits.csv")
    return movies.merge(credits,on='title')

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert_cast(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
      if counter != 3:
         L.append(i['name'])
         counter+=1
      else:
        break
    return L

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
      if i['job']=='Director':
        L.append(i['name'])
        break;
    return L

def stem(text):
  y = []
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

def clean_data(movies):
   movies = movies[['title','movie_id','genres','keywords','overview','vote_average','cast', 'crew']]
   movies.dropna(inplace=True)
   movies['genres'] = movies['genres'].apply(convert)
   movies['keywords'] = movies['keywords'].apply(convert)
   movies['cast'] = movies['cast'].apply(convert_cast)
   movies['crew'] = movies['crew'].apply(fetch_director)
   movies['overview'] = movies['overview'].apply(lambda x:x.split())
   return movies

def create_tags(movies):
   movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
   movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
   movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
   movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

   movies['Tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

   new_df = movies[['movie_id','title','Tags']]
   new_df['Tags']= new_df['Tags'].apply(lambda x:" ".join(x))
   new_df['Tags'] = new_df['Tags'].apply(lambda x:x.lower())
   new_df['Tags'] = new_df['Tags'].apply(stem)
   return new_df

def run_preprocessing():
    movies = load_and_merge()
    movies = clean_data(movies)
    final_df = create_tags(movies)

    final_df.to_csv("data/processed/movies_processed.csv", index=False)

if __name__ == "__main__":
   run_preprocessing()