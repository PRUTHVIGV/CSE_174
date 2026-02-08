# Setup Guide - Indian Cattle Breed Recognition

## Step 1: Install Dependencies

```bash
pip install tensorflow numpy Pillow matplotlib flask
```

## Step 2: Collect Dataset

Create a `dataset` folder with subfolders for each breed:

```
dataset/
├── Gir/              (Add 100+ images)
├── Sahiwal/          (Add 100+ images)
├── Red_Sindhi/       (Add 100+ images)
├── Tharparkar/       (Add 100+ images)
├── Ongole/           (Add 100+ images)
├── Hariana/          (Add 100+ images)
├── Kankrej/          (Add 100+ images)
├── Rathi/            (Add 100+ images)
├── Murrah_Buffalo/   (Add 100+ images)
└── Mehsana_Buffalo/  (Add 100+ images)
```

**Image Sources:**
- Google Images (search "Gir cattle", "Sahiwal cattle", etc.)
- Kaggle datasets
- Government livestock websites
- Agricultural university databases

## Step 3: Train Model

```bash
cd cattle_breed_recognition
python src/train.py --data-dir dataset --epochs 20 --batch-size 32
```

Training takes 30-60 minutes depending on your hardware.

## Step 4: Test Predictions

```bash
python src/predict.py --image test_image.jpg --show
```

## Step 5: Run Web Application

```bash
python src/app.py
```

Open browser: http://localhost:5000

## Tips for Better Accuracy

1. **More Data**: Collect 200+ images per breed
2. **Quality Images**: Clear, well-lit photos
3. **Variety**: Different angles, ages, environments
4. **Balance**: Similar number of images per breed
5. **Augmentation**: Already included in training

## Troubleshooting

**Issue**: Model accuracy is low
- Solution: Add more training images, train for more epochs

**Issue**: Out of memory error
- Solution: Reduce batch size: `--batch-size 16`

**Issue**: Web app shows "Model not found"
- Solution: Train model first using train.py

## Next Steps

1. Deploy on cloud (AWS, Google Cloud, Azure)
2. Create mobile app using TensorFlow Lite
3. Add more breeds
4. Integrate with farm management systems
