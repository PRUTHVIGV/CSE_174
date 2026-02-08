@echo off
echo ========================================
echo Indian Cattle Breed Recognition System
echo ========================================
echo.
echo Select an option:
echo 1. Train Model
echo 2. Run Predictions
echo 3. Start Web App
echo 4. Create Dataset Structure
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    python src\train.py --data-dir dataset --epochs 20
) else if "%choice%"=="2" (
    set /p imgpath="Enter image path: "
    python src\predict.py --image %imgpath% --show
) else if "%choice%"=="3" (
    python src\app.py
) else if "%choice%"=="4" (
    python src\train.py --data-dir dataset
    echo Dataset structure created! Add images to each breed folder.
) else (
    echo Invalid choice!
)

pause
