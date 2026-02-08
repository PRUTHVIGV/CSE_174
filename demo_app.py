from flask import Flask, render_template, request, jsonify
from pathlib import Path
import random

app = Flask(__name__)

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
    return render_template('demo.html', breeds=BREEDS)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    # Demo mode - return random predictions
    breed_names = list(BREEDS.keys())
    random.shuffle(breed_names)
    
    results = []
    confidences = [random.uniform(75, 95), random.uniform(60, 75), random.uniform(40, 60)]
    
    for i in range(3):
        breed = breed_names[i]
        results.append({
            'breed': breed,
            'confidence': round(confidences[i], 2),
            'info': BREEDS[breed]
        })
    
    return jsonify({
        'success': True,
        'predictions': results,
        'demo_mode': True
    })

if __name__ == '__main__':
    print("="*60)
    print("CATTLE BREED RECOGNITION - DEMO WEBSITE")
    print("="*60)
    print("\nDEMO MODE: Showing random predictions")
    print("(Install Python 3.11 + TensorFlow for real predictions)")
    print("\nStarting server...")
    print("Open browser: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
