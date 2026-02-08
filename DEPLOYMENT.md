# 🚀 Deployment Guide

## Quick Deploy Options

### Option 1: Render (Recommended - Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/cattle-breed-recognition.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Settings:
     - **Name**: cattle-breed-recognition
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment

3. **Your app is live!**
   - URL: `https://cattle-breed-recognition.onrender.com`

### Option 2: Railway (Easy - Free)

1. **Push to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to https://railway.app
   - Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-deploys!

3. **Get URL**
   - Click "Settings" → "Generate Domain"
   - Your app is live!

### Option 3: Heroku (Classic)

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create cattle-breed-recognition

# Deploy
git push heroku main

# Open
heroku open
```

### Option 4: Vercel (Fast)

1. Install Vercel CLI
   ```bash
   npm install -g vercel
   ```

2. Deploy
   ```bash
   vercel
   ```

3. Follow prompts - Done!

## Files Needed for Deployment

✅ **app.py** - Main Flask app
✅ **templates/index.html** - Frontend
✅ **requirements.txt** - Dependencies
✅ **Procfile** - Server config
✅ **runtime.txt** - Python version
✅ **.gitignore** - Ignore files

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Visit
http://localhost:5000
```

## Environment Variables (Optional)

For production, set:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key`

## Troubleshooting

**Build fails?**
- Check `requirements.txt` syntax
- Ensure Python 3.11 in `runtime.txt`

**App crashes?**
- Check logs: `heroku logs --tail`
- Verify `Procfile` command

**Port issues?**
- App uses `PORT` environment variable
- Deployment platforms set this automatically

## Custom Domain

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records

### Heroku
```bash
heroku domains:add www.yourdomain.com
```

## SSL Certificate

All platforms provide free SSL automatically!

## Monitoring

- **Render**: Built-in metrics
- **Railway**: Dashboard analytics
- **Heroku**: `heroku logs --tail`

## Cost

- **Render**: Free tier available
- **Railway**: $5/month after free tier
- **Heroku**: $7/month (no free tier)
- **Vercel**: Free for hobby projects

## Recommended: Render

Best balance of:
- Free tier
- Easy setup
- Good performance
- Auto-deploy from GitHub

---

**Your app will be live in 5 minutes!** 🚀
