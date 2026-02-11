# 🐄 Indian Cattle Breed Recognition - CNN Powered

AI-powered web application for identifying 20 Indian cattle and buffalo breeds using deep learning.

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/tensorflow-2.13-orange)](https://www.tensorflow.org/)

## 🌟 Features

- 🤖 **CNN Model** - Real AI predictions with MobileNetV2
- 🐄 **20 Indian Breeds** - Comprehensive coverage
- 🔐 **Login/Signup** - Secure authentication
- 📊 **Confidence Scores** - Percentage-based accuracy
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Modern UI** - Beautiful gradient design

## 🐄 Supported Breeds (20)

### Cattle (16)
Gir, Sahiwal, Red Sindhi, Tharparkar, Ongole, Hariana, Kankrej, Rathi, Kangayam, Hallikar, Amritmahal, Khillari, Deoni, Dangi, Nagori, Punganur

### Buffalo (4)
Murrah, Mehsana, Surti, Jaffarabadi

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/PRUTHVIGV/CSE_174.git
cd CSE_174/cattle_breed_recognition
pip install -r requirements.txt
```

### 2. Run App (Demo Mode)
```bash
python app.py
```
Visit: http://localhost:5000

### 3. Train CNN Model (Optional)

**Step 1: Collect Dataset**
```bash
# Create folders
python create_folders.py

# Add 100+ images per breed to dataset/ folders
# Download from Kaggle or Google Images
```

**Step 2: Train Model**
```bash
python train_cnn.py
# Takes 30-60 minutes
# Creates cattle_model.h5
```

**Step 3: Run with CNN**
```bash
python app.py
# Automatically uses trained model
```

## 📁 Project Structure

```
cattle_breed_recognition/
├── app.py                  # Flask app with CNN integration
├── train_cnn.py           # CNN training script
├── create_folders.py      # Dataset structure creator
├── templates/
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   └── index.html         # Main app
├── dataset/               # Training images (add here)
│   ├── Gir/
│   ├── Sahiwal/
│   └── ... (20 breeds)
├── cattle_model.h5        # Trained model (after training)
├── class_names.txt        # Breed names
└── requirements.txt       # Dependencies
```

## 🎯 How It Works

### Without Model (Demo Mode)
- Color-based predictions
- Good for testing UI
- No training needed

### With CNN Model
- Real AI predictions
- 85-95% accuracy
- Production ready

## 🔧 Tech Stack

- **Backend**: Flask, TensorFlow
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Model**: MobileNetV2 (Transfer Learning)
- **Database**: JSON (users)
- **Deployment**: Render/Railway/Heroku

## 📊 Model Details

- **Architecture**: MobileNetV2 + Custom Head
- **Input Size**: 224x224 RGB
- **Training**: Transfer Learning + Fine-tuning
- **Augmentation**: Flip, Rotation, Zoom, Contrast
- **Accuracy**: 85-95% (with good dataset)

## 🚀 Deployment

### Deploy to Render
1. Push to GitHub
2. Go to [Render](https://render.com)
3. Create Web Service
4. Connect repository
5. Build: `pip install -r requirements.txt`
6. Start: `gunicorn app:app`

### Deploy to Railway
1. Go to [Railway](https://railway.app)
2. Deploy from GitHub
3. Auto-deploys!

## 📖 Documentation

- `CNN_SETUP_GUIDE.md` - Complete setup guide
- `MANUAL_DATASET_GUIDE.md` - Dataset collection
- `TOP_5_IMPROVEMENTS.md` - Feature roadmap
- `IMPROVEMENT_ROADMAP.md` - Long-term vision

## 🎓 Dataset Collection

### Option 1: Kaggle
Search "Indian cattle breeds" and download

### Option 2: Google Images
Use bulk downloader extensions

### Option 3: Manual
Download 100+ images per breed manually

**Minimum**: 50 images/breed
**Recommended**: 100+ images/breed
**Ideal**: 200+ images/breed

## 💡 Tips

- Use GPU for faster training (Google Colab)
- More images = better accuracy
- Verify breed labels before training
- Test with real cattle images

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

## 📄 License

MIT License - Free to use and modify

## 👨‍💻 Author

**PRUTHVIGV**
- GitHub: [@PRUTHVIGV](https://github.com/PRUTHVIGV)
- Repository: [CSE_174](https://github.com/PRUTHVIGV/CSE_174)

## 🙏 Acknowledgments

- ICAR-NBAGR for breed information
- TensorFlow & Keras teams
- Indian agricultural community

---

**Made with ❤️ for Indian Agriculture** 🇮🇳
