# Indian Cattle Breed Recognition System

Clean, modern implementation for recognizing Indian cattle and buffalo breeds using deep learning.

## Features

- **10 Indian Breeds**: Gir, Sahiwal, Red Sindhi, Tharparkar, Ongole, Hariana, Kankrej, Rathi, Murrah Buffalo, Mehsana Buffalo
- **Transfer Learning**: MobileNetV2 for efficient training
- **Web Interface**: Flask-based web application
- **CLI Tools**: Command-line prediction and training

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_clean.txt
```

### 2. Prepare Dataset
```bash
python src/train.py --data-dir dataset
```
This creates the folder structure. Add images to each breed folder.

### 3. Train Model
```bash
python src/train.py --data-dir dataset --epochs 20
```

### 4. Run Predictions
```bash
python src/predict.py --image path/to/image.jpg --show
```

### 5. Start Web App
```bash
python src/app.py
```

## Project Structure

```
src/
├── model.py          # MobileNetV2 model
├── data_loader.py    # Data loading & augmentation
├── breeds_info.py    # Breed information database
├── train.py          # Training script
├── predict.py        # Prediction script
└── app.py            # Flask web app
```

## Dataset Structure

```
dataset/
├── Gir/
├── Sahiwal/
├── Red_Sindhi/
├── Tharparkar/
├── Ongole/
├── Hariana/
├── Kankrej/
├── Rathi/
├── Murrah_Buffalo/
└── Mehsana_Buffalo/
```

## Model Architecture

- Base: MobileNetV2 (ImageNet pretrained)
- Custom layers: GlobalAveragePooling + Dense(256) + Dense(10)
- Training: Two-phase (freeze + fine-tune)
- Input: 224x224 RGB images

## References

- MobileNetV2: https://arxiv.org/abs/1801.04381
- Indian Cattle Breeds: ICAR-NBAGR
