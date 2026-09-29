import numpy as np
 
# ---------------------------------------------------------------------------
# 1. Sample data
# ---------------------------------------------------------------------------
 
MOVIES = ["Inception", "Titanic", "The Matrix", "The Notebook",
          "Interstellar", "La La Land"]
 
# Ratings matrix: rows = users, columns = movies, 0 = not rated (1-5 scale)
USERS = ["Alice", "Bob", "Carol", "Dave", "Eve"]
 
RATINGS = np.array([
    # Inception, Titanic, Matrix, Notebook, Interstellar, LaLaLand
    [5, 1, 5, 1, 5, 2],   # Alice - likes sci-fi
    [4, 2, 5, 1, 4, 1],   # Bob   - likes sci-fi
    [1, 5, 1, 5, 2, 5],   # Carol - likes romance
    [2, 4, 1, 5, 1, 4],   # Dave  - likes romance
    [5, 0, 4, 0, 5, 0],   # Eve   - mostly unrated, some sci-fi ratings
])
 
# Content features for content-based filtering: each movie tagged with
# genre weights (Sci-Fi, Romance, Drama) on a 0-1 scale.
GENRE_FEATURES = {
    "Inception":     [1.0, 0.0, 0.3],
    "Titanic":       [0.0, 1.0, 0.8],
    "The Matrix":    [1.0, 0.0, 0.2],
    "The Notebook":  [0.0, 1.0, 0.6],
    "Interstellar":  [0.9, 0.1, 0.6],
    "La La Land":    [0.0, 0.7, 0.5],
}
 
 
# ---------------------------------------------------------------------------
# 2. Helper: cosine similarity
# ---------------------------------------------------------------------------
 
def cosine_similarity(a, b):
    """Cosine similarity between two 1-D numpy vectors. Returns 0 if either
    vector has zero magnitude (avoids division-by-zero)."""
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))
 
 
# ---------------------------------------------------------------------------
# 3. Collaborative filtering (user-based)
# ---------------------------------------------------------------------------
 
def user_based_recommend(target_user, top_n=3):
    """Recommend movies the target user hasn't rated, based on ratings
    from the most similar other users (weighted average)."""
    target_idx = USERS.index(target_user)
    target_ratings = RATINGS[target_idx]
 
    # similarity between target user and every other user
    similarities = {}
    for i, user in enumerate(USERS):
        if user == target_user:
            continue
        sim = cosine_similarity(target_ratings, RATINGS[i])
        if sim > 0:
            similarities[i] = sim
 
    scores = np.zeros(len(MOVIES))
    weight_sums = np.zeros(len(MOVIES))
 
    for movie_idx in range(len(MOVIES)):
        if target_ratings[movie_idx] != 0:
            continue  # skip movies the user already rated
        for user_idx, sim in similarities.items():
            rating = RATINGS[user_idx][movie_idx]
            if rating > 0:
                scores[movie_idx] += sim * rating
                weight_sums[movie_idx] += sim
 
    predicted = np.divide(
        scores, weight_sums,
        out=np.zeros_like(scores),
        where=weight_sums != 0,
    )
 
    ranked = sorted(
        [(MOVIES[i], predicted[i]) for i in range(len(MOVIES)) if predicted[i] > 0],
        key=lambda x: x[1],
        reverse=True,
    )
    return ranked[:top_n]
 
 
# ---------------------------------------------------------------------------
# 4. Content-based filtering
# ---------------------------------------------------------------------------
 
def content_based_recommend(liked_movie, top_n=3):
    """Recommend movies most similar in genre content to a movie the user
    already likes."""
    liked_vector = np.array(GENRE_FEATURES[liked_movie])
 
    similarities = []
    for movie, features in GENRE_FEATURES.items():
        if movie == liked_movie:
            continue
        sim = cosine_similarity(liked_vector, np.array(features))
        similarities.append((movie, sim))
 
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]
 
 
# ---------------------------------------------------------------------------
# 5. Demo
# ---------------------------------------------------------------------------
 
def main():
    print("=== Collaborative Filtering (user-based) ===")
    for user in USERS:
        recs = user_based_recommend(user)
        if recs:
            rec_str = ", ".join(f"{m} ({s:.2f})" for m, s in recs)
            print(f"{user}: {rec_str}")
        else:
            print(f"{user}: no new recommendations (already rated everything)")
 
    print("\n=== Content-Based Filtering ===")
    for movie in ["Inception", "Titanic"]:
        recs = content_based_recommend(movie)
        rec_str = ", ".join(f"{m} ({s:.2f})" for m, s in recs)
        print(f"Because you liked '{movie}': {rec_str}")
 
 
if __name__ == "__main__":
    main()