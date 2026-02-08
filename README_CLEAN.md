# 🐄 Indian Cattle Breed Recognition System

AI-powered web application for identifying Indian cattle and buffalo breeds.

## 🌟 Features

- **10 Indian Breeds**: Gir, Sahiwal, Red Sindhi, Tharparkar, Ongole, Hariana, Kankrej, Rathi, Murrah Buffalo, Mehsana Buffalo
- **Web Interface**: Drag-and-drop image upload
- **Real-time Predictions**: Instant breed identification
- **Breed Information**: Detailed info about each breed

## 🚀 Live Demo

[View Live Demo](#) *(Add your deployment URL here)*

## 📸 Screenshots

![Home Page](screenshots/home.png)
![Prediction Results](screenshots/results.png)

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Heroku / Render / Railway

## 📦 Installation

### Local Setup

```bash
# Clone repository
git clone https://github.com/yourusername/cattle-breed-recognition.git
cd cattle-breed-recognition

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit: `http://localhost:5000`

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy to Render

1. Fork this repository
2. Go to [Render Dashboard](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

### Deploy to Railway

1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway auto-detects and deploys

## 📁 Project Structure

```
cattle-breed-recognition/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Web interface
├── requirements.txt    # Dependencies
├── Procfile           # Heroku config
├── runtime.txt        # Python version
├── .gitignore         # Git ignore rules
└── README.md          # Documentation
```

## 🐄 Supported Breeds

| Breed | Hindi | Origin | Type |
|-------|-------|--------|------|
| Gir | गिर | Gujarat | Dairy |
| Sahiwal | साहीवाल | Punjab | Dairy |
| Red Sindhi | लाल सिंधी | Sindh | Dairy |
| Tharparkar | थारपारकर | Rajasthan | Dual Purpose |
| Ongole | ओंगोल | Andhra Pradesh | Draught |
| Hariana | हरियाणा | Haryana | Dual Purpose |
| Kankrej | कांकरेज | Gujarat-Rajasthan | Draught |
| Rathi | राठी | Rajasthan | Dairy |
| Murrah Buffalo | मुर्रा भैंस | Haryana | Dairy |
| Mehsana Buffalo | मेहसाणा भैंस | Gujarat | Dairy |

## 🎯 Use Cases

- **Farmers**: Quick breed identification
- **Veterinarians**: Breed verification
- **Livestock Markets**: Authentication
- **Insurance**: Documentation
- **Education**: Learning about breeds

## 🔮 Future Enhancements

- [ ] Add ML model for real predictions
- [ ] Mobile app version
- [ ] More Indian breeds
- [ ] Multi-language support
- [ ] Breed comparison feature
- [ ] Health assessment

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/yourusername/cattle-breed-recognition](https://github.com/yourusername/cattle-breed-recognition)

## 🙏 Acknowledgments

- Indian Council of Agricultural Research (ICAR)
- National Bureau of Animal Genetic Resources (NBAGR)
- Flask framework
- All contributors

---

**Made with ❤️ for Indian Agriculture**
