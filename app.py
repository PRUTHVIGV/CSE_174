from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import base64
from io import BytesIO
from PIL import Image
import hashlib
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'cattle-breed-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

BREEDS = {
    "Gir": {"hindi": "गिर", "origin": "Gujarat", "type": "Dairy", "milk_yield": "10-12 L/day"},
    "Sahiwal": {"hindi": "साहीवाल", "origin": "Punjab", "type": "Dairy", "milk_yield": "8-10 L/day"},
    "Red_Sindhi": {"hindi": "लाल सिंधी", "origin": "Sindh", "type": "Dairy", "milk_yield": "6-8 L/day"},
    "Tharparkar": {"hindi": "थारपारकर", "origin": "Rajasthan", "type": "Dual Purpose", "milk_yield": "4-6 L/day"},
    "Ongole": {"hindi": "ओंगोल", "origin": "Andhra Pradesh", "type": "Draught", "milk_yield": "3-5 L/day"},
    "Hariana": {"hindi": "हरियाणा", "origin": "Haryana", "type": "Dual Purpose", "milk_yield": "6-8 L/day"},
    "Kankrej": {"hindi": "कांकरेज", "origin": "Gujarat-Rajasthan", "type": "Draught", "milk_yield": "4-6 L/day"},
    "Rathi": {"hindi": "राठी", "origin": "Rajasthan", "type": "Dairy", "milk_yield": "5-7 L/day"},
    "Murrah_Buffalo": {"hindi": "मुर्रा भैंस", "origin": "Haryana", "type": "Dairy", "milk_yield": "12-18 L/day"},
    "Mehsana_Buffalo": {"hindi": "मेहसाणा भैंस", "origin": "Gujarat", "type": "Dairy", "milk_yield": "8-12 L/day"}
}

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', breeds=BREEDS, user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        users = load_users()
        
        if email in users and users[email]['password'] == hash_password(password):
            session['user'] = {'email': email, 'name': users[email]['name']}
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        users = load_users()
        
        if email in users:
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        users[email] = {
            'name': name,
            'password': hash_password(password),
            'created_at': datetime.now().isoformat()
        }
        save_users(users)
        session['user'] = {'email': email, 'name': name}
        return jsonify({'success': True})
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Demo prediction
        breeds = list(BREEDS.keys())
        random.shuffle(breeds)
        
        results = []
        confidences = [random.uniform(75, 95), random.uniform(60, 75), random.uniform(40, 60)]
        
        for i in range(3):
            results.append({
                'breed': breeds[i],
                'confidence': round(confidences[i], 2),
                'info': BREEDS[breeds[i]]
            })
        
        # Convert image to base64
        img = Image.open(file)
        img.thumbnail((400, 400))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'predictions': results,
            'image': img_str,
            'analysis': {
                'dominant_colors': ['red', 'white'],
                'brightness': 150
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting server on port", port)
    app.run(host='0.0.0.0', port=port, debug=True)
