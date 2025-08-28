from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS if needed (not necessary if serving frontend via Flask directly)
# CORS(app)

# Load Data
movies = pd.read_csv("D:/Codsoft intern/Recommdation_movie/Recommendation_movie/u.item", sep="|", header=None, encoding="latin-1")
movies = movies[[0, 1]]
movies.columns = ["movie_id", "title"]

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["title"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movies.index, index=movies["title"]).drop_duplicates()

def recommend_movies(title, num_recommendations=5):
    if title not in indices:
        return []
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies["title"].iloc[movie_indices].tolist()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    movie_title = data.get("movie", "")
    recommendations = recommend_movies(movie_title, 5)
    return jsonify({"movie": movie_title, "recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
