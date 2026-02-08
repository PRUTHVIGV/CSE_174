@echo off
echo ========================================
echo Upload to GitHub - CSE_174
echo ========================================
echo.

cd /d c:\CSE_174\cattle_breed_recognition

echo Step 1: Initializing git...
git init

echo.
echo Step 2: Adding files...
git add app.py templates/index.html requirements.txt Procfile runtime.txt .gitignore README.md

echo.
echo Step 3: Committing...
git commit -m "Add cattle breed recognition web app"

echo.
echo Step 4: Connecting to GitHub...
git remote add origin https://github.com/PRUTHVIGV/CSE_174.git

echo.
echo Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Upload Complete!
echo ========================================
echo.
echo Next: Deploy on Render
echo 1. Go to https://render.com
echo 2. Sign up with GitHub
echo 3. Create Web Service from CSE_174 repo
echo 4. Use settings from GITHUB_DEPLOY.md
echo.
pause
