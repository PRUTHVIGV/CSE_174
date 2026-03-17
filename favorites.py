import json
import os

FAVORITES_FILE = 'favorites.json'

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)

def add_favorite(user_email, breed):
    favorites = load_favorites()
    if user_email not in favorites:
        favorites[user_email] = []
    if breed not in favorites[user_email]:
        favorites[user_email].append(breed)
    save_favorites(favorites)
    return True

def remove_favorite(user_email, breed):
    favorites = load_favorites()
    if user_email in favorites and breed in favorites[user_email]:
        favorites[user_email].remove(breed)
    save_favorites(favorites)
    return True

def get_user_favorites(user_email):
    favorites = load_favorites()
    return favorites.get(user_email, [])

def is_favorite(user_email, breed):
    favorites = load_favorites()
    return breed in favorites.get(user_email, [])
