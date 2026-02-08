from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
import numpy as np
from werkzeug.utils import secure_filename
from model import CattleBreedModel
from data_loader import DataLoader
from breeds_info import get_breed_info, INDIAN_BREEDS
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

model = None
loader = None

def load_model():
    global model, loader
    model_path = 'cattle_model.h5'
    if not Path(model_path).exists():
        return False
    model = CattleBreedModel()
    model.load(model_path)
    loader = DataLoader()
    return True

@app.route('/')
def index():
    return render_template('index.html', breeds=INDIAN_BREEDS)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        img_array = loader.load_and_preprocess_image(filepath)
        predictions = model.predict(img_array)
        
        class_names = ['Gir', 'Hariana', 'Kankrej', 'Mehsana_Buffalo', 'Murrah_Buffalo',
                       'Ongole', 'Rathi', 'Red_Sindhi', 'Sahiwal', 'Tharparkar']
        
        top_indices = np.argsort(predictions)[-3:][::-1]
        results = []
        for idx in top_indices:
            breed_name = class_names[idx]
            confidence = float(predictions[idx] * 100)
            breed_info = get_breed_info(breed_name)
            results.append({'breed': breed_name, 'confidence': round(confidence, 2), 'info': breed_info})
        
        img = Image.open(filepath)
        img.thumbnail((400, 400))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'success': True, 'predictions': results, 'image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    print("="*60)
    print("CATTLE BREED RECOGNITION - WEB APP")
    print("="*60)
    if load_model():
        print("\n✓ Model loaded")
        print("\nAccess: http://localhost:5000")
        print("="*60)
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n✗ Model not found!")
        print("Train first: python src/train.py")
