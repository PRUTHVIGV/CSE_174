# 🚀 QUICK START - Indian Cattle Breed Recognition

## ✅ What You Have Now

A **clean, modern** cattle breed recognition system in the `src/` folder:

```
src/
├── model.py          - MobileNetV2 model
├── data_loader.py    - Data handling
├── breeds_info.py    - Breed database
├── train.py          - Training script
├── predict.py        - Prediction tool
├── app.py            - Web application
└── templates/
    └── index.html    - Web interface
```

## 📋 Step-by-Step Guide

### 1. Install Dependencies (2 minutes)

```bash
pip install tensorflow numpy Pillow matplotlib flask
```

### 2. Prepare Dataset (Manual - varies)

**Option A: Create structure and add images manually**
```bash
python src/train.py --data-dir dataset
```
This creates folders. Then add 100+ images per breed.

**Option B: Download existing dataset**
- Search Kaggle for "Indian cattle breeds"
- Or collect from Google Images
- Organize in folders: dataset/Gir/, dataset/Sahiwal/, etc.

**Required structure:**
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
└── Mehsana_Buffalo/  (100+ images)
```

### 3. Train Model (30-60 minutes)

```bash
cd cattle_breed_recognition
python src/train.py --data-dir dataset --epochs 20
```

**Training output:**
- Creates `cattle_model.h5` (trained model)
- Creates `training_history.png` (accuracy/loss plots)
- Shows final accuracy

### 4. Test Predictions

```bash
python src/predict.py --image path/to/cattle_image.jpg --show
```

### 5. Run Web App

```bash
python src/app.py
```

Open browser: **http://localhost:5000**

Upload cattle images and get instant predictions!

## 🎯 What Each File Does

| File | Purpose |
|------|---------|
| `model.py` | MobileNetV2 architecture with transfer learning |
| `data_loader.py` | Loads images, applies augmentation |
| `breeds_info.py` | Database of 10 Indian breeds |
| `train.py` | Trains the model |
| `predict.py` | CLI prediction tool |
| `app.py` | Flask web application |

## 💡 Tips for Success

1. **More images = better accuracy**
   - Minimum: 100 per breed
   - Recommended: 200+ per breed

2. **Quality matters**
   - Clear, well-lit photos
   - Different angles
   - Various ages and environments

3. **Balanced dataset**
   - Similar number of images per breed

4. **Training parameters**
   - Default (20 epochs): Good for testing
   - Production (40 epochs): Better accuracy
   - GPU: Much faster training

## 🔧 Common Commands

**Train with custom settings:**
```bash
python src/train.py --data-dir dataset --epochs 30 --batch-size 16
```

**Predict with top 5 results:**
```bash
python src/predict.py --image test.jpg --top-k 5 --show
```

**Create dataset structure:**
```bash
python src/train.py --data-dir dataset
```

## 🐛 Troubleshooting

**"Dataset not found"**
- Run: `python src/train.py --data-dir dataset`
- Add images to created folders

**"Model not found"**
- Train model first: `python src/train.py`

**Low accuracy**
- Add more training images
- Train for more epochs
- Check image quality

**Out of memory**
- Reduce batch size: `--batch-size 8`
- Reduce image size: `--img-size 160`

## 📊 Expected Results

With good dataset (200+ images per breed):
- **Training time**: 30-60 minutes (CPU), 10-15 minutes (GPU)
- **Accuracy**: 85-95%
- **Model size**: ~10 MB
- **Inference time**: <1 second per image

## 🎓 Learning Resources

**Understanding the code:**
1. Start with `breeds_info.py` (simplest)
2. Then `data_loader.py` (data handling)
3. Then `model.py` (architecture)
4. Finally `train.py` and `predict.py`

**Improving the system:**
- Add more breeds (edit `breeds_info.py`)
- Try different models (edit `model.py`)
- Improve UI (edit `templates/index.html`)
- Add features (extend `app.py`)

## 🚀 Next Steps

1. **Test it**: Train on small dataset first
2. **Improve it**: Add more data, tune parameters
3. **Deploy it**: Put on cloud (AWS, Google Cloud)
4. **Extend it**: Add mobile app, API, etc.

## 📞 Quick Reference

**Train:** `python src/train.py --data-dir dataset`
**Predict:** `python src/predict.py --image test.jpg --show`
**Web App:** `python src/app.py`

---

**You're ready to build an amazing cattle breed recognition system! 🐄🚀**
