from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import base64
from io import BytesIO
from PIL import Image
import hashlib
import json
from datetime import datetime
import random
import pickle
import numpy as np
from history import add_prediction, get_user_history
from suggestions import save_suggestion, load_suggestions

app = Flask(__name__)
app.secret_key = 'cattle-breed-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

USERS_FILE = 'users.json'

# Load trained model if available
MODEL = None
CLASS_NAMES = []
if os.path.exists('cattle_model.pkl') and os.path.exists('class_names.txt'):
    with open('cattle_model.pkl', 'rb') as f:
        MODEL = pickle.load(f)
    with open('class_names.txt', 'r') as f:
        CLASS_NAMES = [line.strip() for line in f]
    print(f"[OK] Loaded model with {len(CLASS_NAMES)} breeds")
else:
    print("[INFO] No trained model found - using demo mode")

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
    "Alambadi": {"origin": "Tamil Nadu", "type": "Draught", "milk_yield": "3-5 L/day"},
    "Amritmahal": {"origin": "Karnataka", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Ayrshire": {"origin": "Scotland", "type": "Dairy", "milk_yield": "20-25 L/day"},
    "Banni": {"origin": "Gujarat", "type": "Dairy", "milk_yield": "8-12 L/day"},
    "Bargur": {"origin": "Tamil Nadu", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Bhadawari": {"origin": "Uttar Pradesh", "type": "Dairy", "milk_yield": "4-6 L/day"},
    "Brown_Swiss": {"origin": "Switzerland", "type": "Dairy", "milk_yield": "25-30 L/day"},
    "Dangi": {"origin": "Maharashtra", "type": "Draught", "milk_yield": "3-5 L/day"},
    "Deoni": {"origin": "Maharashtra", "type": "Dual Purpose", "milk_yield": "8-10 L/day"},
    "Gir": {"origin": "Gujarat", "type": "Dairy", "milk_yield": "10-15 L/day"},
    "Guernsey": {"origin": "Channel Islands", "type": "Dairy", "milk_yield": "18-22 L/day"},
    "Hallikar": {"origin": "Karnataka", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Hariana": {"origin": "Haryana", "type": "Dual Purpose", "milk_yield": "8-12 L/day"},
    "Holstein_Friesian": {"origin": "Netherlands", "type": "Dairy", "milk_yield": "30-35 L/day"},
    "Jaffrabadi": {"origin": "Gujarat", "type": "Dairy", "milk_yield": "12-15 L/day"},
    "Jersey": {"origin": "Jersey Island", "type": "Dairy", "milk_yield": "15-20 L/day"},
    "Kangayam": {"origin": "Tamil Nadu", "type": "Draught", "milk_yield": "3-5 L/day"},
    "Kankrej": {"origin": "Gujarat", "type": "Draught", "milk_yield": "8-12 L/day"},
    "Kasargod": {"origin": "Kerala", "type": "Dairy", "milk_yield": "2-4 L/day"},
    "Kenkatha": {"origin": "Madhya Pradesh", "type": "Draught", "milk_yield": "4-6 L/day"},
    "Kherigarh": {"origin": "Uttar Pradesh", "type": "Dual Purpose", "milk_yield": "5-8 L/day"},
    "Khillari": {"origin": "Maharashtra", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Krishna_Valley": {"origin": "Karnataka", "type": "Draught", "milk_yield": "3-5 L/day"},
    "Malnad_gidda": {"origin": "Karnataka", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Mehsana": {"origin": "Gujarat", "type": "Dairy", "milk_yield": "10-15 L/day"},
    "Murrah": {"origin": "Haryana", "type": "Dairy", "milk_yield": "15-20 L/day"},
    "Nagori": {"origin": "Rajasthan", "type": "Draught", "milk_yield": "4-6 L/day"},
    "Nagpuri": {"origin": "Maharashtra", "type": "Draught", "milk_yield": "3-5 L/day"},
    "Nili_Ravi": {"origin": "Punjab", "type": "Dairy", "milk_yield": "15-18 L/day"},
    "Nimari": {"origin": "Madhya Pradesh", "type": "Dual Purpose", "milk_yield": "4-6 L/day"},
    "Ongole": {"origin": "Andhra Pradesh", "type": "Draught", "milk_yield": "5-8 L/day"},
    "Pulikulam": {"origin": "Tamil Nadu", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Rathi": {"origin": "Rajasthan", "type": "Dairy", "milk_yield": "6-10 L/day"},
    "Red_Dane": {"origin": "Denmark", "type": "Dual Purpose", "milk_yield": "20-25 L/day"},
    "Red_Sindhi": {"origin": "Sindh", "type": "Dairy", "milk_yield": "8-12 L/day"},
    "Sahiwal": {"origin": "Punjab", "type": "Dairy", "milk_yield": "15-20 L/day"},
    "Surti": {"origin": "Gujarat", "type": "Dairy", "milk_yield": "8-10 L/day"},
    "Tharparkar": {"origin": "Rajasthan", "type": "Dual Purpose", "milk_yield": "10-15 L/day"},
    "Toda": {"origin": "Tamil Nadu", "type": "Dairy", "milk_yield": "3-5 L/day"},
    "Umblachery": {"origin": "Tamil Nadu", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Vechur": {"origin": "Kerala", "type": "Dairy", "milk_yield": "1-3 L/day"}
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

@app.route('/google-login', methods=['POST'])
def google_login():
    return jsonify({'success': True, 'redirect': '/google-auth'})

@app.route('/google-auth')
def google_auth():
    return render_template('google_auth.html')

@app.route('/google-authenticate', methods=['POST'])
def google_authenticate():
    data = request.json
    session['user'] = {'email': data['email'], 'name': data['name']}
    return jsonify({'success': True})

@app.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_history = get_user_history(session['user']['email'])
    return render_template('history.html', history=user_history)

@app.route('/compare')
def compare():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('compare.html', breeds=list(BREEDS.keys()), breeds_json=json.dumps(BREEDS))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    history = get_user_history(session['user']['email'])
    
    stats = {
        'total': len(history),
        'avg_confidence': round(sum(h['confidence'] for h in history) / len(history), 1) if history else 0,
        'top_breed': max(set(h['breed'] for h in history), key=lambda x: sum(1 for h in history if h['breed'] == x)).replace('_', ' ') if history else 'N/A'
    }
    
    breed_counts = {}
    for h in history:
        breed_counts[h['breed'].replace('_', ' ')] = breed_counts.get(h['breed'].replace('_', ' '), 0) + 1
    
    timeline = {}
    for h in history:
        date = h['timestamp'][:10]
        timeline[date] = timeline.get(date, 0) + 1
    
    return render_template('dashboard.html', stats=stats, breed_counts=json.dumps(breed_counts), timeline=json.dumps(timeline))

@app.route('/features')
def features():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('features.html')

@app.route('/suggest')
def suggest():
    if 'user' not in session:
        return redirect(url_for('login'))
    suggestions = load_suggestions()
    return render_template('suggest.html', suggestions=suggestions[-10:][::-1])

@app.route('/batch')
def batch():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('batch.html')

@app.route('/camera')
def camera():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('camera.html')

@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('search.html', breeds=BREEDS)

@app.route('/submit-suggestion', methods=['POST'])
def submit_suggestion():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    save_suggestion(data['name'], data['category'], data['title'], data['description'], data['priority'])
    return jsonify({'success': True})

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
        # Save uploaded file temporarily
        filename = 'temp_' + str(datetime.now().timestamp()) + '.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Use trained model if available
        if MODEL is not None:
            img = Image.open(filepath).convert('RGB')
            img_resized = img.resize((128, 128))
            img_array = np.array(img_resized).flatten() / 255.0
            
            proba = MODEL.predict_proba([img_array])[0]
            top_3_idx = np.argsort(proba)[-3:][::-1]
            
            results = []
            for idx in top_3_idx:
                breed_name = CLASS_NAMES[idx]
                confidence = float(proba[idx] * 100)
                # Only show if confidence > 5%
                if confidence > 5:
                    results.append({
                        'breed': breed_name,
                        'confidence': round(confidence, 2),
                        'info': BREEDS.get(breed_name, {'origin': 'Unknown', 'type': 'Unknown', 'milk_yield': 'N/A'})
                    })
        else:
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
        img = Image.open(filepath)
        img.thumbnail((400, 400))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Delete temp file
        os.remove(filepath)
        
        # Save to history
        add_prediction(session['user']['email'], results[0]['breed'], results[0]['confidence'], file.filename)
        
        return jsonify({
            'success': True,
            'predictions': results,
            'image': img_str
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting server on port", port)
    app.run(host='0.0.0.0', port=port, debug=True)
