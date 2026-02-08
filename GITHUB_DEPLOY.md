# 🚀 Upload to GitHub & Deploy

## Your Repository
https://github.com/PRUTHVIGV/CSE_174

## Step 1: Upload to GitHub

```bash
cd c:\CSE_174\cattle_breed_recognition

# Initialize git
git init

# Add only deployment files
git add app.py
git add templates/index.html
git add requirements.txt
git add Procfile
git add runtime.txt
git add .gitignore
git add README.md
git add DEPLOYMENT.md

# Commit
git commit -m "Add cattle breed recognition web app"

# Connect to your repo
git remote add origin https://github.com/PRUTHVIGV/CSE_174.git

# Push to main branch
git branch -M main
git push -u origin main
```

If you get "repository already exists" error:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Step 2: Deploy to Render

### A. Sign Up on Render
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub
4. Authorize Render to access your repos

### B. Create Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect account" if needed
4. Find "CSE_174" repository
5. Click "Connect"

### C. Configure Service
Fill in these settings:

**Name**: `cattle-breed-recognition`

**Region**: `Oregon (US West)` or closest to you

**Branch**: `main`

**Root Directory**: Leave empty (or `cattle_breed_recognition` if needed)

**Runtime**: `Python 3`

**Build Command**: 
```
pip install -r requirements.txt
```

**Start Command**:
```
gunicorn app:app
```

**Instance Type**: `Free`

### D. Deploy
1. Click "Create Web Service"
2. Wait 2-3 minutes for build
3. Your app will be live at: `https://cattle-breed-recognition.onrender.com`

## Step 3: Update README

After deployment, update your README.md with the live URL:

```markdown
## 🚀 Live Demo
[View Live App](https://cattle-breed-recognition.onrender.com)
```

Then push:
```bash
git add README.md
git commit -m "Add live demo link"
git push
```

## Alternative: Deploy to Railway

1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose "PRUTHVIGV/CSE_174"
6. Railway auto-deploys!
7. Click "Settings" → "Generate Domain"
8. Your app is live!

## Alternative: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd c:\CSE_174\cattle_breed_recognition
vercel

# Follow prompts
```

## Troubleshooting

### "Permission denied" error?
```bash
git remote set-url origin https://PRUTHVIGV@github.com/PRUTHVIGV/CSE_174.git
git push -u origin main
```

### Files in wrong location?
If your files are in `cattle_breed_recognition` subfolder:
- In Render, set **Root Directory** to: `cattle_breed_recognition`

### Build fails on Render?
Check these files exist:
- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `app.py`
- `templates/index.html`

### App crashes after deploy?
Check Render logs:
1. Go to your service dashboard
2. Click "Logs" tab
3. Look for errors

## Quick Commands Reference

```bash
# Check git status
git status

# See what will be pushed
git log --oneline

# Force push (if needed)
git push -f origin main

# Clone your repo elsewhere
git clone https://github.com/PRUTHVIGV/CSE_174.git
```

## Your Live URLs

After deployment, you'll have:

**Render**: `https://cattle-breed-recognition.onrender.com`
**Railway**: `https://cattle-breed-recognition.up.railway.app`
**Vercel**: `https://cattle-breed-recognition.vercel.app`

## Share Your Project

Add these to your GitHub repo:

1. **Description**: "AI-powered Indian cattle breed recognition web app"

2. **Topics**: 
   - `python`
   - `flask`
   - `machine-learning`
   - `agriculture`
   - `cattle`
   - `web-app`

3. **Website**: Your live URL

4. **README badges**: Already included in README.md

---

**Ready to deploy! Follow Step 1, then Step 2. Your app will be live in 5 minutes! 🚀**
