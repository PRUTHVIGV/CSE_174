from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import base64
from io import BytesIO
from PIL import Image
import hashlib
import json
from datetime import datetime
import numpy as np

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

USERS_FILE = 'users.json'

# Load CNN model if available
MODEL = None
CLASS_NAMES = []

def load_cnn_model():
    """Load trained CNN model"""
    global MODEL, CLASS_NAMES
    try:
        import tensorflow as tf
        MODEL = tf.keras.models.load_model('cattle_model.h5')
        with open('class_names.txt', 'r') as f:
            CLASS_NAMES = [line.strip() for line in f]
        print("✓ CNN Model loaded successfully")
        return True
    except:
        print("✗ CNN Model not found - using demo mode")
        return False

# Try to load model on startup
MODEL_LOADED = load_cnn_model()

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
    "Mehsana_Buffalo": {"hindi": "मेहसाणा भैंस", "origin": "Gujarat", "type": "Dairy", "milk_yield": "8-12 L/day"},
    "Kangayam": {"hindi": "कांगयम", "origin": "Tamil Nadu", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Hallikar": {"hindi": "हल्लीकर", "origin": "Karnataka", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Amritmahal": {"hindi": "अमृतमहल", "origin": "Karnataka", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Khillari": {"hindi": "खिल्लारी", "origin": "Maharashtra", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Deoni": {"hindi": "देवनी", "origin": "Maharashtra", "type": "Dual Purpose", "milk_yield": "4-5 L/day"},
    "Dangi": {"hindi": "डांगी", "origin": "Maharashtra", "type": "Dual Purpose", "milk_yield": "3-4 L/day"},
    "Nagori": {"hindi": "नागौरी", "origin": "Rajasthan", "type": "Draught", "milk_yield": "2-3 L/day"},
    "Punganur": {"hindi": "पुंगनूर", "origin": "Andhra Pradesh", "type": "Dual Purpose", "milk_yield": "3-5 L/day"},
    "Surti": {"hindi": "सूरती", "origin": "Gujarat", "type": "Dairy", "milk_yield": "6-8 L/day"},
    "Jaffarabadi": {"hindi": "जाफराबादी", "origin": "Gujarat", "type": "Dairy", "milk_yield": "10-12 L/day"}
}

def preprocess_image(image_file):
    """Preprocess image for CNN model"""
    img = Image.open(image_file).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_with_cnn(image_file):
    """Predict using trained CNN model"""
    img_array = preprocess_image(image_file)
    predictions = MODEL.predict(img_array, verbose=0)[0]
    
    # Get top 3 predictions
    top_indices = np.argsort(predictions)[-3:][::-1]
    
    results = []
    for idx in top_indices:
        breed_name = CLASS_NAMES[idx]
        confidence = float(predictions[idx] * 100)
        breed_info = BREEDS.get(breed_name, {
            "hindi": "N/A", "origin": "India", "type": "Unknown", "milk_yield": "N/A"
        })
        results.append({
            'breed': breed_name,
            'confidence': round(confidence, 2),
            'info': breed_info
        })
    
    return results

def predict_demo(image_file):
    """Demo prediction (fallback)"""
    import random
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
    
    return results

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', breeds=BREEDS, user=session['user'], model_loaded=MODEL_LOADED)

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
        # Use CNN model if loaded, otherwise demo
        if MODEL_LOADED:
            predictions = predict_with_cnn(file)
            mode = "CNN Model"
        else:
            file.seek(0)
            predictions = predict_demo(file)
            mode = "Demo Mode"
        
        # Convert image to base64
        file.seek(0)
        img = Image.open(file)
        img.thumbnail((400, 400))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'image': img_str,
            'mode': mode
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
