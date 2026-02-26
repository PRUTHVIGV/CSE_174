import os

breeds = [
    "Gir", "Sahiwal", "Red_Sindhi", "Tharparkar", "Ongole",
    "Hariana", "Kankrej", "Rathi", "Murrah_Buffalo", "Mehsana_Buffalo",
    "Kangayam", "Hallikar", "Amritmahal", "Khillari", "Deoni",
    "Dangi", "Nagori", "Punganur", "Surti", "Jaffarabadi"
]

print("Creating dataset structure...")
os.makedirs("dataset", exist_ok=True)

for breed in breeds:
    path = f"dataset/{breed}"
    os.makedirs(path, exist_ok=True)
    print(f"[OK] Created: {path}/")

print(f"\n[DONE] Dataset structure ready!")
print(f"Total folders: {len(breeds)}")
print(f"\nNext: Add 100+ images to each folder")
print(f"Then run: python train_cnn.py")
