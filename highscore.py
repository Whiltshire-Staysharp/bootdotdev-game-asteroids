import json
import os

FILE_PATH = "scores.json"

def load_high_scores():
    # Check if file exists; if not, create it with an empty list to prevent errors
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)
        return []
    
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file exists but is empty or corrupted, return an empty list
        return []

def save_high_scores(scores):
    # Sort by score descending and keep only top 10
    scores.sort(key=lambda x: x["score"], reverse=True)
    top_10 = scores[:10]
    with open(FILE_PATH, "w") as f:
        json.dump(top_10, f)

def is_high_score(new_score):
    scores = load_high_scores()
    # If there are fewer than 10 scores, or the new score beats the lowest top score
    if len(scores) < 10 or new_score > scores[-1]["score"]:
        return True
    return False