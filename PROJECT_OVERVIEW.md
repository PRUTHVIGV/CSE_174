# 🐄 Indian Cattle & Buffalo Breed Recognition System

A clean, modern deep learning system for identifying Indian cattle and buffalo breeds.

## 🎯 Overview

This system uses transfer learning with MobileNetV2 to recognize 10 major Indian cattle and buffalo breeds:

**Cattle Breeds:**
- Gir (गिर) - Gujarat
- Sahiwal (साहीवाल) - Punjab  
- Red Sindhi (लाल सिंधी) - Sindh
- Tharparkar (थारपारकर) - Rajasthan
- Ongole (ओंगोल) - Andhra Pradesh
- Hariana (हरियाणा) - Haryana
- Kankrej (कांकरेज) - Gujarat-Rajasthan
- Rathi (राठी) - Rajasthan

**Buffalo Breeds:**
- Murrah Buffalo (मुर्रा भैंस) - Haryana
- Mehsana Buffalo (मेहसाणा भैंस) - Gujarat

## 🚀 Quick Start

### Installation
```bash
pip install tensorflow numpy Pillow matplotlib flask
```

### Train Model
```bash
python src/train.py --data-dir dataset --epochs 20
```

### Run Predictions
```bash
python src/predict.py --image test.jpg --show
```

### Start Web App
```bash
python src/app.py
```
Visit: http://localhost:5000

## 📁 Project Structure

```
cattle_breed_recognition/
├── src/
│   ├── model.py           # MobileNetV2 architecture
│   ├── data_loader.py     # Data loading & augmentation
│   ├── breeds_info.py     # Breed information database
│   ├── train.py           # Training script
│   ├── predict.py         # CLI prediction tool
│   ├── app.py             # Flask web application
│   └── templates/
│       └── index.html     # Web interface
├── dataset/               # Training images (create this)
├── SETUP_GUIDE.md        # Detailed setup instructions
├── RUN.bat               # Windows launcher
└── requirements_clean.txt # Dependencies
```

## 🎓 How It Works

1. **Transfer Learning**: Uses MobileNetV2 pretrained on ImageNet
2. **Two-Phase Training**: 
   - Phase 1: Train top layers (frozen base)
   - Phase 2: Fine-tune last 30 layers
3. **Data Augmentation**: Random flips, rotations, zoom, contrast
4. **Optimization**: Early stopping, learning rate reduction

## 📊 Model Details

- **Architecture**: MobileNetV2 + Custom Head
- **Input Size**: 224x224 RGB
- **Parameters**: ~2.5M trainable
- **Training Time**: 30-60 minutes (CPU/GPU)
- **Expected Accuracy**: 85-95% (with good dataset)

## 💾 Dataset Requirements

- **Minimum**: 100 images per breed
- **Recommended**: 200+ images per breed
- **Quality**: Clear, well-lit photos
- **Variety**: Different angles, ages, environments
- **Format**: JPG, PNG

### Where to Get Images

1. Google Images (search breed names)
2. Kaggle datasets
3. Government livestock websites
4. ICAR-NBAGR database
5. Agricultural university resources

## 🔧 Usage Examples

### Training with Custom Parameters
```bash
python src/train.py --data-dir dataset --epochs 30 --batch-size 16 --img-size 224
```

### Prediction with Top 5 Results
```bash
python src/predict.py --image cattle.jpg --top-k 5 --show
```

### Web App on Custom Port
```python
# Edit src/app.py, change last line:
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 📈 Performance Tips

1. **More Data**: Collect 200+ images per breed
2. **Balanced Dataset**: Equal images for each breed
3. **Quality Images**: Clear, focused photos
4. **Longer Training**: Increase epochs to 30-40
5. **GPU Training**: Use CUDA-enabled TensorFlow

## 🌐 Deployment Options

### Local Server
```bash
python src/app.py
```

### Cloud Deployment
- **AWS**: EC2 + Elastic Beanstalk
- **Google Cloud**: App Engine
- **Azure**: App Service
- **Heroku**: Free tier available

### Mobile Deployment
Convert to TensorFlow Lite:
```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
```

## 🔍 API Usage

### Prediction Endpoint
```bash
curl -X POST -F "file=@cattle.jpg" http://localhost:5000/predict
```

### Response Format
```json
{
  "success": true,
  "predictions": [
    {
      "breed": "Gir",
      "confidence": 95.67,
      "info": {
        "hindi": "गिर",
        "origin": "Gir Forest, Gujarat",
        "type": "Dairy",
        "milk_yield": "10-12 L/day"
      }
    }
  ]
}
```

## 🛠️ Troubleshooting

**Low Accuracy?**
- Add more training images
- Train for more epochs
- Check image quality

**Out of Memory?**
- Reduce batch size: `--batch-size 8`
- Reduce image size: `--img-size 160`

**Model Not Found?**
- Train model first: `python src/train.py`

**Slow Training?**
- Use GPU-enabled TensorFlow
- Reduce image size
- Use smaller batch size

## 📚 References

- MobileNetV2: https://arxiv.org/abs/1801.04381
- Transfer Learning: https://www.tensorflow.org/tutorials/images/transfer_learning
- Indian Cattle Breeds: ICAR-NBAGR (https://nbagr.icar.gov.in/)

## 🤝 Contributing

Improvements welcome:
- Add more breeds
- Improve model architecture
- Better web interface
- Mobile app development
- API enhancements

## 📄 License

Open source - use for education, research, or commercial projects.

## 🎯 Use Cases

- **Farmers**: Identify cattle breeds
- **Veterinarians**: Quick breed identification
- **Livestock Markets**: Breed verification
- **Insurance**: Cattle documentation
- **Research**: Breed distribution studies
- **Education**: Learning about Indian breeds

---

**Built with ❤️ for Indian Agriculture**
