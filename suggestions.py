import json
import os
from datetime import datetime

SUGGESTIONS_FILE = 'suggestions.json'

def load_suggestions():
    if os.path.exists(SUGGESTIONS_FILE):
        with open(SUGGESTIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_suggestion(name, category, title, description, priority):
    suggestions = load_suggestions()
    
    suggestions.append({
        'name': name,
        'category': category,
        'title': title,
        'description': description,
        'priority': priority,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    
    with open(SUGGESTIONS_FILE, 'w') as f:
        json.dump(suggestions, f, indent=2)
    
    return True
