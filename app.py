from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
import os
import base64
from io import BytesIO
from PIL import Image
import hashlib
import json
from datetime import datetime, date
import random
import pickle
import numpy as np
from database import (init_db, save_user, get_user, load_users, update_user_avatar, update_user_password, delete_user,
    add_prediction, get_user_history, clear_user_history, get_all_history,
    add_favorite, remove_favorite, get_user_favorites, is_favorite,
    add_feedback, get_user_feedback, get_all_feedback,
    log_search, get_search_counts, save_share, get_share, save_suggestion)
from translations import get_translation, get_breeds_by_state, TRANSLATIONS

app = Flask(__name__)
app.secret_key = 'cattle-breed-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

BREED_OF_DAY_FILE = 'breed_of_day.json'

init_db()

HEALTH_TIPS = {
    "Gir": ["Vaccinate against FMD every 6 months", "Provide 15-20L water daily", "Deworm every 3 months"],
    "Sahiwal": ["Monitor milk fever post-calving", "Provide mineral supplements", "Regular hoof trimming"],
    "Jersey": ["Susceptible to heat stress - provide shade", "High calcium diet needed", "Regular mastitis checks"],
    "Holstein_Friesian": ["Monitor for ketosis in early lactation", "Provide TMR diet", "Regular body condition scoring"],
    "Murrah": ["Wallow access reduces heat stress", "High protein diet for milk production", "Brucellosis vaccination"],
    "default": ["Annual vaccination schedule", "Regular deworming every 3 months", "Provide clean water daily", "Balanced mineral supplementation", "Regular veterinary checkups"]
}

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
        user = get_user(email)
        if user and user['password'] == hash_password(password):
            session['user'] = {'email': email, 'name': user['name']}
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
        if get_user(email):
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        save_user(email, name, hash_password(password))
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

    user_fb = get_user_feedback(session['user']['email'])
    accuracy = f"{round(sum(1 for f in user_fb if f['correct'])/len(user_fb)*100)}%" if user_fb else 'N/A'
    stats['accuracy'] = accuracy
    
    breed_counts = {}
    for h in history:
        breed_counts[h['breed'].replace('_', ' ')] = breed_counts.get(h['breed'].replace('_', ' '), 0) + 1
    
    timeline = {}
    for h in history:
        date = h['timestamp'][:10]
        timeline[date] = timeline.get(date, 0) + 1
    
    search_counts = get_search_counts(8)

    return render_template('dashboard.html', stats=stats, breed_counts=json.dumps(breed_counts), timeline=json.dumps(timeline), search_counts=json.dumps(search_counts))

@app.route('/features')
def features():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('features.html')

@app.route('/leaderboard')
def leaderboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    all_history = get_all_history()
    all_breed_counts = {}
    user_scores = {}
    for email, predictions in all_history.items():
        user_scores[email] = len(predictions)
        for p in predictions:
            breed = p['breed'].replace('_', ' ')
            all_breed_counts[breed] = all_breed_counts.get(breed, 0) + 1
    top_breeds = sorted(all_breed_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    return render_template('leaderboard.html',
        top_breeds=top_breeds, top_users=top_users,
        total_predictions=sum(user_scores.values()), total_users=len(user_scores)
    )

@app.route('/batch')
def batch():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('batch.html')

@app.route('/breed/<breed_name>')
def breed_detail(breed_name):
    if 'user' not in session:
        return redirect(url_for('login'))
    breed_info = BREEDS.get(breed_name)
    if not breed_info:
        return redirect(url_for('index'))
    log_search(breed_name)
    user_email = session['user']['email']
    is_fav = is_favorite(user_email, breed_name)
    return render_template('breed_detail.html', breed_name=breed_name, breed_info=breed_info, is_favorite=is_fav)

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

@app.route('/favorites')
def favorites():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_favs = get_user_favorites(session['user']['email'])
    fav_breeds = {k: v for k, v in BREEDS.items() if k in user_favs}
    return render_template('favorites.html', breeds=fav_breeds)

@app.route('/toggle-favorite', methods=['POST'])
def toggle_favorite():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    breed = data.get('breed')
    user_email = session['user']['email']
    
    if is_favorite(user_email, breed):
        remove_favorite(user_email, breed)
        return jsonify({'success': True, 'action': 'removed'})
    else:
        add_favorite(user_email, breed)
        return jsonify({'success': True, 'action': 'added'})

@app.route('/api/breeds', methods=['GET'])
def api_breeds():
    return jsonify({'breeds': BREEDS, 'total': len(BREEDS)})

@app.route('/api/breed/<breed_name>', methods=['GET'])
def api_breed_info(breed_name):
    breed_info = BREEDS.get(breed_name)
    if not breed_info:
        return jsonify({'error': 'Breed not found'}), 404
    return jsonify({'breed': breed_name, 'info': breed_info})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    history = get_user_history(session['user']['email'])
    breed_counts = {}
    for h in history:
        breed_counts[h['breed']] = breed_counts.get(h['breed'], 0) + 1
    
    return jsonify({
        'total_predictions': len(history),
        'avg_confidence': round(sum(h['confidence'] for h in history) / len(history), 1) if history else 0,
        'breed_distribution': breed_counts,
        'recent_predictions': history[-5:][::-1] if history else []
    })

@app.route('/export-history', methods=['GET'])
def export_history():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    history = get_user_history(session['user']['email'])
    return jsonify({'history': history, 'user': session['user']['email'], 'exported_at': datetime.now().isoformat()})

@app.route('/clear-history', methods=['POST'])
def clear_history():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    clear_user_history(session['user']['email'])
    return jsonify({'success': True, 'message': 'History cleared'})

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    results = []
    
    for file in files[:10]:  # Limit to 10 files
        if file.filename == '':
            continue
        
        try:
            filename = 'temp_' + str(datetime.now().timestamp()) + '_' + file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            if MODEL is not None:
                img = Image.open(filepath).convert('RGB')
                img_resized = img.resize((128, 128))
                img_array = np.array(img_resized).flatten() / 255.0
                proba = MODEL.predict_proba([img_array])[0]
                top_idx = np.argmax(proba)
                breed_name = CLASS_NAMES[top_idx]
                confidence = float(proba[top_idx] * 100)
            else:
                breed_name = random.choice(list(BREEDS.keys()))
                confidence = random.uniform(70, 95)
            
            results.append({
                'filename': file.filename,
                'breed': breed_name,
                'confidence': round(confidence, 2)
            })
            
            add_prediction(session['user']['email'], breed_name, confidence, file.filename)
            os.remove(filepath)
        
        except Exception as e:
            results.append({'filename': file.filename, 'error': str(e)})
    
    return jsonify({'success': True, 'results': results})

@app.route('/filter-breeds', methods=['GET'])
def filter_breeds():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    breed_type = request.args.get('type', 'all')
    origin = request.args.get('origin', 'all')
    
    filtered = BREEDS
    if breed_type != 'all':
        filtered = {k: v for k, v in filtered.items() if v['type'].lower() == breed_type.lower()}
    if origin != 'all':
        filtered = {k: v for k, v in filtered.items() if origin.lower() in v['origin'].lower()}
    
    return jsonify({'breeds': filtered, 'count': len(filtered)})

@app.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['avatar']
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        return jsonify({'error': 'Invalid file type'}), 400
    email = session['user']['email']
    filename = 'avatar_' + hashlib.md5(email.encode()).hexdigest() + '.' + ext
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    update_user_avatar(email, filename)
    return jsonify({'success': True, 'filename': filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_email = session['user']['email']
    user_data = get_user(user_email) or {}
    history = get_user_history(user_email)
    favs = get_user_favorites(user_email)
    stats = {
        'total': len(history),
        'avg_confidence': round(sum(h['confidence'] for h in history) / len(history), 1) if history else 0,
        'favorites_count': len(favs),
        'joined': user_data.get('created_at', 'N/A')[:10] if user_data.get('created_at') else 'N/A',
        'avatar': user_data.get('avatar', None)
    }
    return render_template('profile.html', user=session['user'], stats=stats)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.json
        email = session['user']['email']
        user = get_user(email)
        if user['password'] != hash_password(data.get('current')):
            return jsonify({'success': False, 'error': 'Current password incorrect'}), 400
        update_user_password(email, hash_password(data.get('new')))
        return jsonify({'success': True})
    return render_template('change_password.html')

@app.route('/delete-account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    delete_user(session['user']['email'])
    session.pop('user', None)
    return jsonify({'success': True})

@app.route('/health')
def health_tips():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('health.html', breeds=BREEDS, tips=HEALTH_TIPS)

@app.route('/encyclopedia')
def encyclopedia():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('encyclopedia.html', breeds=BREEDS)

@app.route('/breed-of-day')
def breed_of_day():
    today = str(date.today())
    if os.path.exists(BREED_OF_DAY_FILE):
        with open(BREED_OF_DAY_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    if data.get('date') != today:
        data = {'date': today, 'breed': random.choice(list(BREEDS.keys()))}
        with open(BREED_OF_DAY_FILE, 'w') as f:
            json.dump(data, f)
    breed = data['breed']
    return jsonify({'breed': breed, 'info': BREEDS[breed]})

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.json
    add_feedback(session['user']['email'], data.get('predicted'), data.get('correct'), data.get('actual', ''))
    return jsonify({'success': True})

@app.route('/streak')
def streak():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    history = get_user_history(session['user']['email'])
    if not history:
        return jsonify({'streak': 0, 'total_days': 0})
    dates = sorted(set(h['timestamp'][:10] for h in history), reverse=True)
    streak_count = 1
    for i in range(1, len(dates)):
        d1 = datetime.strptime(dates[i-1], '%Y-%m-%d')
        d2 = datetime.strptime(dates[i], '%Y-%m-%d')
        if (d1 - d2).days == 1:
            streak_count += 1
        else:
            break
    return jsonify({'streak': streak_count, 'total_days': len(dates)})

@app.route('/export-csv')
def export_csv():
    if 'user' not in session:
        return redirect(url_for('login'))
    history = get_user_history(session['user']['email'])
    lines = ['#,Breed,Confidence,Date']
    for i, h in enumerate(reversed(history), 1):
        lines.append(f"{i},{h['breed'].replace('_',' ')},{h['confidence']}%,{h['timestamp'][:10]}")
    response = make_response('\n'.join(lines))
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=cattle_history.csv'
    return response

@app.route('/export-pdf')
def export_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    history = get_user_history(session['user']['email'])
    user_email = session['user']['email']
    html = f"""<html><head><style>body{{font-family:Arial;padding:20px}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #ddd;padding:8px;text-align:left}}th{{background:#667eea;color:white}}h1{{color:#667eea}}</style></head>
    <body><h1>🐄 Cattle Breed Prediction Report</h1><p>User: {user_email}</p><p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <table><tr><th>#</th><th>Breed</th><th>Confidence</th><th>Date</th></tr>"""
    for i, h in enumerate(reversed(history), 1):
        html += f"<tr><td>{i}</td><td>{h['breed'].replace('_',' ')}</td><td>{h['confidence']}%</td><td>{h['timestamp'][:10]}</td></tr>"
    html += "</table></body></html>"
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=cattle_report.html'
    return response

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

ADMIN_EMAIL = 'admin@cattle.com'

@app.route('/admin')
def admin():
    if 'user' not in session or session['user']['email'] != ADMIN_EMAIL:
        return redirect(url_for('index'))
    users = load_users()
    all_history = get_all_history()
    feedback = get_all_feedback()
    total_preds = sum(len(v) for v in all_history.values())
    correct_fb = sum(1 for f in feedback if f['correct'])
    accuracy = round(correct_fb / len(feedback) * 100) if feedback else 0
    return render_template('admin.html',
        users=users, total_preds=total_preds,
        feedback=feedback[:20], accuracy=accuracy, model_loaded=MODEL is not None
    )

@app.route('/admin/retrain', methods=['POST'])
def admin_retrain():
    if 'user' not in session or session['user']['email'] != ADMIN_EMAIL:
        return jsonify({'error': 'Unauthorized'}), 403
    import subprocess, sys
    try:
        subprocess.Popen([sys.executable, 'train_simple.py'])
        return jsonify({'success': True, 'message': 'Training started in background'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/delete-user/<email>', methods=['POST'])
def admin_delete_user(email):
    if 'user' not in session or session['user']['email'] != ADMIN_EMAIL:
        return jsonify({'error': 'Unauthorized'}), 403
    delete_user(email)
    return jsonify({'success': True})

@app.route('/share/<share_id>')
def shared_prediction(share_id):
    data = get_share(share_id)
    if data:
        if isinstance(data.get('info'), str):
            data['info'] = json.loads(data['info'])
        return render_template('shared.html', data=data, breeds=BREEDS)
    return redirect(url_for('index'))

@app.route('/create-share', methods=['POST'])
def create_share():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.json
    share_id = hashlib.md5((str(datetime.now()) + data.get('breed','')).encode()).hexdigest()[:8]
    save_share(share_id, data.get('breed'), data.get('confidence'),
        json.dumps(BREEDS.get(data.get('breed'), {})), session['user']['name'])
    return jsonify({'success': True, 'share_id': share_id})

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html', breeds_json=json.dumps(BREEDS))

@app.route('/similar-breeds/<breed_name>')
def similar_breeds(breed_name):
    breed_info = BREEDS.get(breed_name)
    if not breed_info:
        return jsonify({'similar': []})
    similar = [
        {'name': k, 'info': v} for k, v in BREEDS.items()
        if k != breed_name and (v['type'] == breed_info['type'] or v['origin'] == breed_info['origin'])
    ][:4]
    return jsonify({'similar': similar})

@app.context_processor
def inject_globals():
    lang = session.get('lang', 'en')
    return {'t': get_translation(lang), 'current_lang': lang, 'all_langs': TRANSLATIONS}

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/set-language', methods=['POST'])
def set_language():
    lang = request.json.get('lang', 'en')
    if lang in TRANSLATIONS:
        session['lang'] = lang
    return jsonify({'success': True})

@app.route('/location-breeds')
def location_breeds():
    state = request.args.get('state', '')
    breeds = get_breeds_by_state(state)
    result = {b: BREEDS[b] for b in breeds if b in BREEDS}
    return jsonify({'state': state, 'breeds': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting server on port", port)
    app.run(host='0.0.0.0', port=port, debug=True)
