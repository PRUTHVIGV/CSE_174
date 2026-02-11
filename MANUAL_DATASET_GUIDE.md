# 📸 Manual Dataset Collection Guide

## Quick Start (3 Options)

### Option 1: Download from Kaggle (Easiest)

1. Go to https://www.kaggle.com/datasets
2. Search "Indian cattle breeds"
3. Download dataset
4. Extract to `dataset/` folder

### Option 2: Use Google Images Bulk Downloader

1. Install Chrome Extension: "Download All Images"
2. For each breed:
   - Google: "Gir cattle India"
   - Click extension
   - Download 100+ images
   - Save to `dataset/Gir/`

### Option 3: Manual Collection

Create folders and add images manually:

```
dataset/
├── Gir/              (100+ images)
├── Sahiwal/          (100+ images)
├── Red_Sindhi/       (100+ images)
├── Tharparkar/       (100+ images)
├── Ongole/           (100+ images)
├── Hariana/          (100+ images)
├── Kankrej/          (100+ images)
├── Rathi/            (100+ images)
├── Murrah_Buffalo/   (100+ images)
├── Mehsana_Buffalo/  (100+ images)
├── Kangayam/         (100+ images)
├── Hallikar/         (100+ images)
├── Amritmahal/       (100+ images)
├── Khillari/         (100+ images)
├── Deoni/            (100+ images)
├── Dangi/            (100+ images)
├── Nagori/           (100+ images)
├── Punganur/         (100+ images)
├── Surti/            (100+ images)
└── Jaffarabadi/      (100+ images)
```

## 🔍 Where to Find Images

### Government Sources
- **ICAR-NBAGR**: https://nbagr.icar.gov.in/
- **NDDB**: https://www.nddb.coop/
- **State Animal Husbandry Departments**

### Image Sources
- **Google Images**: Search "[Breed] cattle India"
- **Flickr**: Creative Commons images
- **Wikimedia Commons**: Free images
- **YouTube**: Extract frames from videos

### Research Papers
- Search Google Scholar for cattle breed papers
- Download images from research publications

## 🎯 Image Quality Guidelines

### Good Images ✅
- Clear, focused cattle
- Full body visible
- Good lighting
- Different angles
- Various ages
- Different environments

### Avoid ❌
- Blurry images
- Multiple breeds in one image
- Heavily edited/filtered
- Watermarked images
- Too small (<200x200px)

## 🚀 Quick Collection Script

Create `manual_collect.py`:

```python
import os

breeds = [
    "Gir", "Sahiwal", "Red_Sindhi", "Tharparkar", "Ongole",
    "Hariana", "Kankrej", "Rathi", "Murrah_Buffalo", "Mehsana_Buffalo",
    "Kangayam", "Hallikar", "Amritmahal", "Khillari", "Deoni",
    "Dangi", "Nagori", "Punganur", "Surti", "Jaffarabadi"
]

os.makedirs("dataset", exist_ok=True)
for breed in breeds:
    os.makedirs(f"dataset/{breed}", exist_ok=True)
    print(f"Created: dataset/{breed}/")

print("\nDataset structure created!")
print("Now add 100+ images to each folder")
```

Run: `python manual_collect.py`

## 📊 Minimum Requirements

**For Training**:
- Minimum: 50 images per breed
- Recommended: 100+ images per breed
- Ideal: 200+ images per breed

**Total Images**:
- 20 breeds × 100 images = 2000 images
- Takes 2-3 hours to collect manually

## ⚡ After Collection

Once you have images:

```bash
# Check dataset
dir dataset

# Train model
python train_cnn.py

# Run app
python app.py
```

## 💡 Pro Tips

1. **Use Multiple Sources** - Don't rely on one website
2. **Verify Breeds** - Make sure images match breed
3. **Remove Duplicates** - Use tools to find similar images
4. **Organize Well** - Keep folder names consistent
5. **Backup Dataset** - Save to cloud storage

## 🎯 Recommended Approach

**Day 1**: Collect 10 breeds (1000 images)
**Day 2**: Collect 10 more breeds (1000 images)
**Day 3**: Train model and test

**Total Time**: 2-3 days for complete dataset

---

**Once dataset is ready, run: `python train_cnn.py`** 🚀
