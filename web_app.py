from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

class WebPredictor:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.breeds = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
        self.breed_info = {
            'Gir': {'origin': 'Gujarat', 'type': 'Dairy', 'milk_yield': '10-12 L/day'},
            'Sahiwal': {'origin': 'Punjab', 'type': 'Dairy', 'milk_yield': '8-10 L/day'},
            'Red_Sindhi': {'origin': 'Sindh', 'type': 'Dairy', 'milk_yield': '6-8 L/day'},
            'Tharparkar': {'origin': 'Rajasthan', 'type': 'Dual Purpose', 'milk_yield': '4-6 L/day'},
            'Ongole': {'origin': 'Andhra Pradesh', 'type': 'Draught', 'milk_yield': '3-5 L/day'},
            'Hariana': {'origin': 'Haryana', 'type': 'Dual Purpose', 'milk_yield': '6-8 L/day'},
            'Kankrej': {'origin': 'Gujarat', 'type': 'Draught', 'milk_yield': '4-6 L/day'},
            'Rathi': {'origin': 'Rajasthan', 'type': 'Dairy', 'milk_yield': '5-7 L/day'},
            'Murrah_Buffalo': {'origin': 'Haryana', 'type': 'Dairy', 'milk_yield': '12-18 L/day'},
            'Mehsana_Buffalo': {'origin': 'Gujarat', 'type': 'Dairy', 'milk_yield': '8-12 L/day'}
        }
    
    def preprocess_image(self, image):
        img = cv2.resize(image, (224, 224))
        img = np.expand_dims(img, axis=0)
        return img / 255.0
    
    def predict(self, image):
        processed = self.preprocess_image(image)
        predictions = self.model.predict(processed)
        
        pred_class = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        breed = self.breeds[pred_class]
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3 = [(self.breeds[i], float(predictions[0][i])) for i in top_3_idx]
        
        return {
            'breed': breed,
            'confidence': confidence,
            'top_3': top_3,
            'breed_info': self.breed_info.get(breed, {})
        }

predictor = WebPredictor('cattle_breed_model.h5')

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cattle Breed Recognition</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            .result { margin-top: 20px; padding: 20px; background: #e8f5e8; border-radius: 5px; }
            .breed-info { margin-top: 15px; padding: 15px; background: #f0f8ff; border-radius: 5px; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #45a049; }
            .top-predictions { margin-top: 15px; }
            .prediction-item { margin: 5px 0; padding: 8px; background: #f9f9f9; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐄 Indian Cattle & Buffalo Breed Recognition</h1>
            <div class="upload-area">
                <input type="file" id="imageInput" accept="image/*" style="display: none;">
                <button onclick="document.getElementById('imageInput').click()">Choose Image</button>
                <p>Upload an image of cattle or buffalo</p>
            </div>
            <div id="preview"></div>
            <div id="result"></div>
        </div>
        
        <script>
            document.getElementById('imageInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        document.getElementById('preview').innerHTML = 
                            '<img src="' + e.target.result + '" style="max-width: 400px; border-radius: 5px;">';
                        
                        // Send to server
                        const formData = new FormData();
                        formData.append('image', file);
                        
                        fetch('/predict', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.error) {
                                document.getElementById('result').innerHTML = '<div class="result">Error: ' + data.error + '</div>';
                            } else {
                                let html = '<div class="result">';
                                html += '<h3>🎯 Prediction: ' + data.breed.replace('_', ' ') + '</h3>';
                                html += '<p><strong>Confidence:</strong> ' + (data.confidence * 100).toFixed(1) + '%</p>';
                                
                                if (data.breed_info) {
                                    html += '<div class="breed-info">';
                                    html += '<h4>📋 Breed Information:</h4>';
                                    html += '<p><strong>Origin:</strong> ' + data.breed_info.origin + '</p>';
                                    html += '<p><strong>Type:</strong> ' + data.breed_info.type + '</p>';
                                    html += '<p><strong>Milk Yield:</strong> ' + data.breed_info.milk_yield + '</p>';
                                    html += '</div>';
                                }
                                
                                html += '<div class="top-predictions"><h4>🏆 Top 3 Predictions:</h4>';
                                data.top_3.forEach((pred, i) => {
                                    html += '<div class="prediction-item">' + (i+1) + '. ' + 
                                           pred[0].replace('_', ' ') + ' (' + (pred[1] * 100).toFixed(1) + '%)</div>';
                                });
                                html += '</div></div>';
                                
                                document.getElementById('result').innerHTML = html;
                            }
                        });
                    };
                    reader.readAsDataURL(file);
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        image = Image.open(file.stream)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        result = predictor.predict(image)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)