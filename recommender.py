import os
import pandas as pd

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path,  "u.item")

import sys
sys.stdout.reconfigure(encoding='utf-8')



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# Step 1: Load the dataset
# =========================
# u.item has | separated values, so we specify sep='|'

movies = pd.read_csv(file_path, sep="|", header=None, encoding="latin-1")


# Keep only movieId, title, and genres
movies = movies[[0, 1, 2]]
movies.columns = ['movieId', 'title', 'release_date']

print("Movies dataset loaded successfully!")
print(movies.head())

# =========================
# Step 2: Preprocess data
# =========================
# Since this dataset doesn’t have genres column, we'll use movie titles for similarity
movies['title'] = movies['title'].fillna('')

# =========================
# Step 3: TF-IDF on titles
# =========================
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['title'])

# =========================
# Step 4: Compute similarity
# =========================
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Map movie titles to indices
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# =========================
# Step 5: Recommendation function
# =========================
def recommend_movies(title, num_recommendations=5):
    if title not in indices:
        return f"❌ Movie '{title}' not found in dataset!"
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]  # skip itself
    movie_indices = [i[0] for i in sim_scores]
    
    return movies['title'].iloc[movie_indices].tolist()

# =========================
# Step 6: Test
# =========================
print("\n🎬 Movies similar to 'Toy Story (1995)':")
print(recommend_movies("Toy Story (1995)", 5))
for movies in recommend_movies :
    print("👉", movies)
