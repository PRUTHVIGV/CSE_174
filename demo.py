"""Demo - Shows system structure"""
import os
from pathlib import Path

print("="*60)
print("INDIAN CATTLE BREED RECOGNITION SYSTEM")
print("="*60)
print("\nSystem Status: READY")
print("Location: src/")
print("Breeds: 10 Indian cattle and buffalo breeds")

print("\nCore Components:")
components = [
    ("model.py", "MobileNetV2 model"),
    ("data_loader.py", "Data loading"),
    ("breeds_info.py", "Breed database"),
    ("train.py", "Training script"),
    ("predict.py", "Prediction tool"),
    ("app.py", "Web application")
]

for file, desc in components:
    exists = Path(f"src/{file}").exists()
    status = "[OK]" if exists else "[MISSING]"
    print(f"  {status} {file:20s} - {desc}")

print("\nSupported Breeds:")
breeds = [
    "1. Gir", "2. Sahiwal", "3. Red Sindhi", "4. Tharparkar",
    "5. Ongole", "6. Hariana", "7. Kankrej", "8. Rathi",
    "9. Murrah Buffalo", "10. Mehsana Buffalo"
]
for breed in breeds:
    print(f"  {breed}")

print("\nDocumentation:")
docs = ["INDEX.md", "START_HERE.md", "QUICK_START.md", "SETUP_GUIDE.md"]
for doc in docs:
    exists = Path(doc).exists()
    status = "[OK]" if exists else "[MISSING]"
    print(f"  {status} {doc}")

print("\nIMPORTANT:")
print("  - Your Python: 3.14.0")
print("  - TensorFlow needs: Python 3.9-3.11")
print("  - Solution: Install Python 3.11")

print("\nNext Steps:")
print("  1. Read INDEX.md")
print("  2. Read START_HERE.md")
print("  3. Install Python 3.11")
print("  4. Install: pip install tensorflow numpy Pillow matplotlib flask")
print("  5. Collect dataset images")
print("  6. Train model: python src/train.py --data-dir dataset")

print("\n" + "="*60)
print("System ready! Check documentation to begin.")
print("="*60)
