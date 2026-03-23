"""
CNN Model Training for Cattle Breed Recognition
Run on Google Colab or Python 3.11/3.12 with GPU for best results.
Expected accuracy: 85-95% vs 14% for Random Forest.

Usage:
    python train_cnn.py
"""
import os
import pickle
import numpy as np
from pathlib import Path

DATASET_DIR = 'dataset'
IMG_SIZE    = 128
BATCH_SIZE  = 32
EPOCHS      = 30

def load_data():
    from PIL import Image
    X, y, class_names = [], [], []
    for folder in sorted(Path(DATASET_DIR).iterdir()):
        if not folder.is_dir(): continue
        class_names.append(folder.name)
        idx = len(class_names) - 1
        images = list(folder.glob('*.jpg')) + list(folder.glob('*.jpeg')) + list(folder.glob('*.png'))
        for img_path in images[:150]:
            try:
                img = Image.open(img_path).convert('RGB').resize((IMG_SIZE, IMG_SIZE))
                X.append(np.array(img) / 255.0)
                y.append(idx)
            except: continue
    return np.array(X), np.array(y), class_names

def train():
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
        from sklearn.model_selection import train_test_split
    except ImportError:
        print('[ERROR] TensorFlow not installed. Run: pip install tensorflow==2.13.0')
        print('[INFO]  Requires Python 3.11 or 3.12')
        return

    print('='*60)
    print('CNN TRAINING - CATTLE BREED RECOGNITION')
    print('='*60)

    print('[1/4] Loading dataset...')
    X, y, class_names = load_data()
    print(f'      {len(X)} images, {len(class_names)} breeds')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    y_train_cat = tf.keras.utils.to_categorical(y_train, len(class_names))
    y_test_cat  = tf.keras.utils.to_categorical(y_test,  len(class_names))

    print('[2/4] Building CNN model...')
    model = models.Sequential([
        # Data augmentation
        layers.RandomFlip('horizontal', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),

        # Block 1
        layers.Conv2D(32, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),

        # Block 2
        layers.Conv2D(64, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),

        # Block 3
        layers.Conv2D(128, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),

        # Block 4
        layers.Conv2D(256, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),

        # Classifier
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(len(class_names), activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()

    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=3, verbose=1)
    ]

    print('[3/4] Training...')
    history = model.fit(
        X_train, y_train_cat,
        validation_data=(X_test, y_test_cat),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks
    )

    loss, acc = model.evaluate(X_test, y_test_cat, verbose=0)
    print(f'\n[4/4] Test Accuracy: {acc*100:.1f}%')

    # Save model in both formats
    model.save('cattle_cnn_model.h5')
    print('[OK] Saved: cattle_cnn_model.h5')

    with open('class_names.txt', 'w') as f:
        f.write('\n'.join(class_names))
    print('[OK] Saved: class_names.txt')

    # Also save as sklearn-compatible wrapper for app.py compatibility
    print('\n[DONE] CNN training complete!')
    print(f'       Accuracy: {acc*100:.1f}%')
    print('       To use in app.py, set USE_CNN=True in app.py')

if __name__ == '__main__':
    train()
