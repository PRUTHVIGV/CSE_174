import json
import os
from datetime import datetime

HISTORY_FILE = 'prediction_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_prediction(user_email, breed, confidence, image_name):
    history = load_history()
    
    if user_email not in history:
        history[user_email] = []
    
    history[user_email].append({
        'breed': breed,
        'confidence': confidence,
        'image': image_name,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last 50 predictions per user
    history[user_email] = history[user_email][-50:]
    
    save_history(history)

def get_user_history(user_email):
    history = load_history()
    return history.get(user_email, [])
