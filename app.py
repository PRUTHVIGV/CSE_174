from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import base64
from io import BytesIO
from PIL import Image
import hashlib
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple user storage (use database in production)
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
    "Gir": {
        "hindi": "गिर", "origin": "Gir Forest, Gujarat", "type": "Dairy", 
        "milk_yield": "10-12 L/day", "weight": "385-545 kg", "color": "Red/White spotted",
        "horns": "Curved backward", "special": "World-famous dairy breed",
        "characteristics": ["Forehead bulge", "Long ears", "Docile temperament"],
        "keywords": ["red", "white", "spotted", "curved", "bulge"]
    },
    "Sahiwal": {
        "hindi": "साहीवाल", "origin": "Punjab", "type": "Dairy",
        "milk_yield": "8-10 L/day", "weight": "300-500 kg", "color": "Reddish-brown",
        "horns": "Short and stumpy", "special": "Heat-tolerant dairy breed",
        "characteristics": ["Loose skin", "Dewlap present", "Heat resistant"],
        "keywords": ["brown", "red", "short", "loose", "dewlap"]
    },
    "Red_Sindhi": {
        "hindi": "लाल सिंधी", "origin": "Sindh", "type": "Dairy",
        "milk_yield": "6-8 L/day", "weight": "300-450 kg", "color": "Uniform red",
        "horns": "Small and thick", "special": "Compact body, disease resistant",
        "characteristics": ["Compact build", "Red coat", "Small size"],
        "keywords": ["red", "small", "compact", "uniform"]
    },
    "Tharparkar": {
        "hindi": "थारपारकर", "origin": "Tharparkar, Rajasthan", "type": "Dual Purpose",
        "milk_yield": "4-6 L/day", "weight": "350-500 kg", "color": "White/Light grey",
        "horns": "Medium, upward", "special": "Desert adapted",
        "characteristics": ["Desert hardy", "Strong build", "Drought resistant"],
        "keywords": ["white", "grey", "medium", "strong"]
    },
    "Ongole": {
        "hindi": "ओंगोल", "origin": "Ongole, Andhra Pradesh", "type": "Draught",
        "milk_yield": "3-5 L/day", "weight": "400-600 kg", "color": "White with black points",
        "horns": "Short and stumpy", "special": "Parent of Brahman cattle",
        "characteristics": ["Large size", "Prominent hump", "Black muzzle"],
        "keywords": ["white", "black", "large", "hump", "muzzle"]
    },
    "Hariana": {
        "hindi": "हरियाणा", "origin": "Haryana", "type": "Dual Purpose",
        "milk_yield": "6-8 L/day", "weight": "350-550 kg", "color": "White/Light grey",
        "horns": "Short, blunt", "special": "Versatile dual-purpose",
        "characteristics": ["Muscular body", "Light color", "Good draught"],
        "keywords": ["white", "grey", "muscular", "short"]
    },
    "Kankrej": {
        "hindi": "कांकरेज", "origin": "Gujarat-Rajasthan", "type": "Draught",
        "milk_yield": "4-6 L/day", "weight": "350-600 kg", "color": "Silver-grey",
        "horns": "Lyre-shaped, long", "special": "Most powerful draught",
        "characteristics": ["Distinctive horns", "Grey color", "Large size"],
        "keywords": ["grey", "silver", "lyre", "long", "horns"]
    },
    "Rathi": {
        "hindi": "राठी", "origin": "Bikaner, Rajasthan", "type": "Dairy",
        "milk_yield": "5-7 L/day", "weight": "250-400 kg", "color": "White with patches",
        "horns": "Small and pointed", "special": "Desert dairy breed",
        "characteristics": ["Spotted coat", "Small size", "Desert adapted"],
        "keywords": ["white", "spotted", "patches", "small"]
    },
    "Murrah_Buffalo": {
        "hindi": "मुर्रा भैंस", "origin": "Haryana", "type": "Dairy",
        "milk_yield": "12-18 L/day", "weight": "450-650 kg", "color": "Jet black",
        "horns": "Tightly coiled spiral", "special": "World's best dairy buffalo",
        "characteristics": ["Jet black", "Spiral horns", "High milk yield"],
        "keywords": ["black", "buffalo", "spiral", "coiled"]
    },
    "Mehsana_Buffalo": {
        "hindi": "मेहसाणा भैंस", "origin": "Mehsana, Gujarat", "type": "Dairy",
        "milk_yield": "8-12 L/day", "weight": "400-600 kg", "color": "Black with white",
        "horns": "Curved backward", "special": "Murrah-Surti cross",
        "characteristics": ["Black with markings", "Curved horns", "Good milk"],
        "keywords": ["black", "white", "buffalo", "curved", "markings"]
    }
}

def analyze_image(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img_small = img.resize((50, 50))
    pixels = list(img_small.getdata())
    
    r_avg = sum(p[0] for p in pixels) / len(pixels)
    g_avg = sum(p[1] for p in pixels) / len(pixels)
    b_avg = sum(p[2] for p in pixels) / len(pixels)
    
    color_profile = {
        'red': r_avg > 120 and r_avg > g_avg and r_avg > b_avg,
        'white': r_avg > 180 and g_avg > 180 and b_avg > 180,
        'black': r_avg < 80 and g_avg < 80 and b_avg < 80,
        'grey': abs(r_avg - g_avg) < 30 and abs(g_avg - b_avg) < 30,
        'brown': r_avg > 100 and g_avg > 60 and b_avg < 80
    }
    
    return {
        'colors': color_profile,
        'brightness': (r_avg + g_avg + b_avg) / 3
    }

def predict_breed(image_analysis):
    scores = {}
    colors = image_analysis['colors']
    
    for breed, info in BREEDS.items():
        score = 0
        
        if colors['black'] and 'black' in info['color'].lower():
            score += 40
        if colors['white'] and 'white' in info['color'].lower():
            score += 40
        if colors['red'] and 'red' in info['color'].lower():
            score += 40
        if colors['grey'] and 'grey' in info['color'].lower():
            score += 40
        if colors['brown'] and 'brown' in info['color'].lower():
            score += 40
        
        if colors['black'] and 'Buffalo' in breed:
            score += 30
        
        import random
        score += random.uniform(10, 30)
        
        scores[breed] = score
    
    sorted_breeds = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total = sum(s for _, s in sorted_breeds[:3])
    
    results = []
    for breed, score in sorted_breeds[:3]:
        confidence = (score / total * 100) if total > 0 else 33.33
        results.append({
            'breed': breed,
            'confidence': round(confidence, 2),
            'info': BREEDS[breed]
        })
    
    return results

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
            session['user'] = {
                'email': email,
                'name': users[email]['name']
            }
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
        
        session['user'] = {
            'email': email,
            'name': name
        }
        
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
        image_analysis = analyze_image(file)
        file.seek(0)
        predictions = predict_breed(image_analysis)
        
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
            'analysis': {
                'dominant_colors': [k for k, v in image_analysis['colors'].items() if v],
                'brightness': round(image_analysis['brightness'], 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
