"""
Simple ML Model for Cattle Breed Recognition
Uses scikit-learn (works with Python 3.14)
"""
import os
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from pathlib import Path

IMG_SIZE = 128
DATASET_DIR = "dataset"

def load_images():
    """Load and preprocess images"""
    print("[INFO] Loading images...")
    X, y, class_names = [], [], []
    
    for breed_folder in sorted(Path(DATASET_DIR).iterdir()):
        if not breed_folder.is_dir():
            continue
        
        breed_name = breed_folder.name
        class_names.append(breed_name)
        class_idx = len(class_names) - 1
        
        images = list(breed_folder.glob("*.jpg")) + list(breed_folder.glob("*.jpeg")) + list(breed_folder.glob("*.png"))
        print(f"  - {breed_name}: {len(images)} images")
        
        for img_path in images[:150]:  # Limit to 150 per breed for speed
            try:
                img = Image.open(img_path).convert('RGB')
                img = img.resize((IMG_SIZE, IMG_SIZE))
                img_array = np.array(img).flatten() / 255.0
                X.append(img_array)
                y.append(class_idx)
            except:
                continue
    
    return np.array(X), np.array(y), class_names

def train_model():
    print("="*60)
    print("TRAINING - CATTLE BREED RECOGNITION")
    print("="*60)
    
    if not os.path.exists(DATASET_DIR):
        print(f"\n[ERROR] Dataset not found at {DATASET_DIR}/")
        return
    
    # Load data
    X, y, class_names = load_images()
    print(f"\n[OK] Loaded {len(X)} images from {len(class_names)} breeds")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"[INFO] Training: {len(X_train)}, Testing: {len(X_test)}")
    
    # Train model
    print("\n[INFO] Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n[OK] Accuracy: {accuracy*100:.2f}%")
    
    # Save model
    with open('cattle_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('class_names.txt', 'w') as f:
        f.write('\n'.join(class_names))
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nModel saved: cattle_model.pkl")
    print(f"Accuracy: {accuracy*100:.2f}%")
    print(f"Classes: {len(class_names)} breeds")

if __name__ == "__main__":
    train_model()
