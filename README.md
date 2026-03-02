# 🐄 Cattle Breed Recognition System

AI-powered web application that identifies 41 cattle and buffalo breeds from images.

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download dataset (optional - model already trained)
python download_dataset.py

# 3. Run application
python app.py

# 4. Open browser
http://localhost:5000
```

## 🎯 Features

- ✅ **41 Breeds** - Indian & international cattle/buffalo breeds
- ✅ **Real-time Prediction** - 2-3 second analysis
- ✅ **History Tracking** - Auto-save all predictions
- ✅ **Breed Comparison** - Compare up to 3 breeds with charts
- ✅ **Analytics Dashboard** - Trends, stats, visualizations
- ✅ **Dark Mode** - Toggle theme with persistence
- ✅ **Responsive Design** - Works on all devices

## 📸 Demo Credentials

```
Email: demo@test.com
Password: demo123
```

Or create your own account via signup.

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.14, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **ML Model**: Random Forest (6,000+ images, 41 classes)
- **Storage**: JSON files (easy migration to database)

## 📁 Project Structure

```
├── app.py              # Main Flask app
├── history.py          # Prediction history
├── train_simple.py     # Model training
├── static/             # CSS & JS
├── templates/          # HTML pages
├── dataset/            # Training images
└── cattle_model.pkl    # Trained model
```

## 📊 Supported Breeds

**Indian Breeds**: Gir, Sahiwal, Tharparkar, Ongole, Hariana, Kankrej, Rathi, Red Sindhi, Deoni, Hallikar, Kangayam, Khillari, Pulikulam, Vechur, and more...

**Buffalo Breeds**: Murrah, Mehsana, Jaffrabadi, Nili Ravi, Surti, Toda, Bhadawari

**International**: Holstein Friesian, Jersey, Ayrshire, Brown Swiss, Guernsey, Red Dane

## 🎓 Documentation

- **PROJECT_DOCUMENTATION.md** - Complete technical details
- **REVIEWER_GUIDE.md** - Presentation script & Q&A
- **DATASET_SOURCES.md** - Dataset collection guide
- **UPCOMING_FEATURES.md** - Feature roadmap

## 🚀 Deployment

Ready for deployment on:
- Render
- Railway
- Heroku
- PythonAnywhere

Files included: `Procfile`, `runtime.txt`, `requirements.txt`

## 📈 Model Info

- **Current**: Random Forest (14% accuracy, Python 3.14 compatible)
- **Upgrade**: TensorFlow CNN (85-95% accuracy, needs Python 3.11/3.12)
- **Training Time**: 5 minutes
- **Inference Time**: 2-3 seconds

## 🔒 Security

- SHA-256 password hashing
- Session-based authentication
- File size limits (16MB)
- Input validation

## 🌟 Highlights

- Clean, modular code
- Base template architecture
- Unified CSS with variables
- Mobile-responsive
- Dark mode support
- Interactive charts
- Production-ready

## 📞 Links

- **GitHub**: https://github.com/PRUTHVIGV/CSE_174
- **Dataset**: Kaggle - sujayroy723/indian-cattle-breeds

## 🎯 Future Enhancements

1. TensorFlow CNN upgrade (95% accuracy)
2. Mobile apps (Android/iOS)
3. REST API
4. Disease detection
5. Batch upload
6. Multi-language support
7. Export reports (PDF)
8. Social sharing

---

**Built with ❤️ for cattle breed recognition**
