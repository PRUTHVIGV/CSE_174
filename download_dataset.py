import kagglehub
import shutil
import os
from pathlib import Path

print("[INFO] Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("sujayroy723/indian-cattle-breeds")
print(f"[OK] Dataset downloaded to: {path}")

# Create dataset directory
dataset_dir = Path("dataset")
dataset_dir.mkdir(exist_ok=True)

# Copy downloaded data to dataset folder
source = Path(path)
print(f"\n[INFO] Organizing dataset...")

# List what's in the downloaded folder
print(f"\n[INFO] Contents of {source}:")
for item in source.rglob("*"):
    if item.is_file():
        print(f"  - {item.relative_to(source)}")

# Copy all breed folders to dataset directory
copied_breeds = []
for breed_folder in source.iterdir():
    if breed_folder.is_dir():
        dest = dataset_dir / breed_folder.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(breed_folder, dest)
        
        # Count images
        image_count = len(list(dest.glob("*.jpg"))) + len(list(dest.glob("*.jpeg"))) + len(list(dest.glob("*.png")))
        copied_breeds.append((breed_folder.name, image_count))
        print(f"[OK] Copied {breed_folder.name}: {image_count} images")

print(f"\n[OK] Dataset ready! Total breeds: {len(copied_breeds)}")
print("\n[INFO] Breed summary:")
for breed, count in sorted(copied_breeds):
    print(f"  - {breed}: {count} images")

print(f"\n[OK] You can now train the model with:")
print(f"     python train_cnn.py --data-dir dataset --epochs 30")
