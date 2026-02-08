# 🐄 Indian Cattle Breed Recognition

AI-powered web application for identifying Indian cattle and buffalo breeds.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://your-app.onrender.com)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green)](https://flask.palletsprojects.com/)

## 🌟 Features

- 🐄 **10 Indian Breeds** - Comprehensive breed database
- 🎯 **Instant Recognition** - Upload and get results
- 📱 **Responsive Design** - Works on all devices
- 🌐 **Web-based** - No installation needed
- 📊 **Detailed Info** - Learn about each breed

## 🚀 Live Demo

**[Try it now →](https://your-app.onrender.com)**

## 📸 Preview

![App Screenshot](https://via.placeholder.com/800x400?text=Cattle+Breed+Recognition)

## 🐄 Supported Breeds

| Breed | Hindi | Origin | Type | Milk Yield |
|-------|-------|--------|------|------------|
| Gir | गिर | Gujarat | Dairy | 10-12 L/day |
| Sahiwal | साहीवाल | Punjab | Dairy | 8-10 L/day |
| Red Sindhi | लाल सिंधी | Sindh | Dairy | 6-8 L/day |
| Tharparkar | थारपारकर | Rajasthan | Dual Purpose | 4-6 L/day |
| Ongole | ओंगोल | Andhra Pradesh | Draught | 3-5 L/day |
| Hariana | हरियाणा | Haryana | Dual Purpose | 6-8 L/day |
| Kankrej | कांकरेज | Gujarat-Rajasthan | Draught | 4-6 L/day |
| Rathi | राठी | Rajasthan | Dairy | 5-7 L/day |
| Murrah Buffalo | मुर्रा भैंस | Haryana | Dairy | 12-18 L/day |
| Mehsana Buffalo | मेहसाणा भैंस | Gujarat | Dairy | 8-12 L/day |

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render / Heroku / Railway

## 📦 Quick Start

### Local Development

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

## 🚀 Deploy to Cloud

### Deploy to Render (Free)

1. Fork this repository
2. Go to [Render](https://render.com)
3. Create new Web Service
4. Connect your GitHub repo
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

### Deploy to Railway

1. Go to [Railway](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select this repository
4. Done! Railway auto-deploys

### Deploy to Heroku

```bash
heroku create your-app-name
git push heroku main
heroku open
```

## 📁 Project Structure

```
cattle-breed-recognition/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Web interface
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment config
├── runtime.txt        # Python version
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🎯 Use Cases

- 👨‍🌾 **Farmers** - Quick breed identification
- 🏥 **Veterinarians** - Breed verification
- 🏪 **Markets** - Authentication & pricing
- 📚 **Education** - Learning about breeds
- 🔬 **Research** - Data collection

## 🔮 Roadmap

- [ ] Add ML model for real predictions
- [ ] Mobile app (React Native)
- [ ] More Indian breeds (20+)
- [ ] Multi-language support
- [ ] Breed comparison tool
- [ ] Health assessment feature
- [ ] API for developers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [ICAR-NBAGR](https://nbagr.icar.gov.in/) - Breed information
- [Flask](https://flask.palletsprojects.com/) - Web framework
- All contributors and supporters

## 📞 Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for Indian Agriculture**
