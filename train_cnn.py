"""
CNN Training for Cattle Breed Recognition
Trains on 20 Indian cattle and buffalo breeds
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
import os
import matplotlib.pyplot as plt

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 30
DATASET_DIR = "dataset"

def create_model(num_classes):
    """Create CNN model using MobileNetV2"""
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = keras.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.Rescaling(1./255),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def load_dataset():
    """Load and prepare dataset"""
    # Training dataset with augmentation
    train_ds = keras.preprocessing.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE
    )
    
    # Validation dataset
    val_ds = keras.preprocessing.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE
    )
    
    # Data augmentation
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),
    ])
    
    train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y))
    
    # Optimize performance
    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
    
    return train_ds, val_ds, train_ds.class_names

def plot_history(history):
    """Plot training history"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(history.history['accuracy'], label='Training')
    ax1.plot(history.history['val_accuracy'], label='Validation')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(history.history['loss'], label='Training')
    ax2.plot(history.history['val_loss'], label='Validation')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=150)
    print("Training history saved to training_history.png")

def main():
    print("="*60)
    print("CNN TRAINING - CATTLE BREED RECOGNITION")
    print("="*60)
    
    # Check dataset
    if not os.path.exists(DATASET_DIR):
        print(f"\n✗ Dataset not found at {DATASET_DIR}/")
        print("Run: python collect_dataset.py")
        return
    
    # Load dataset
    print("\n1. Loading dataset...")
    train_ds, val_ds, class_names = load_dataset()
    num_classes = len(class_names)
    print(f"   Found {num_classes} breeds: {', '.join(class_names[:5])}...")
    
    # Create model
    print("\n2. Building CNN model...")
    model = create_model(num_classes)
    print(f"   Model parameters: {model.count_params():,}")
    
    # Train
    print("\n3. Training model...")
    print(f"   Epochs: {EPOCHS}")
    print(f"   Batch size: {BATCH_SIZE}")
    
    callbacks = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
        keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True)
    ]
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )
    
    # Evaluate
    print("\n4. Evaluating model...")
    loss, accuracy = model.evaluate(val_ds)
    print(f"   Final Accuracy: {accuracy*100:.2f}%")
    print(f"   Final Loss: {loss:.4f}")
    
    # Save
    print("\n5. Saving model...")
    model.save('cattle_model.h5')
    
    # Save class names
    with open('class_names.txt', 'w') as f:
        f.write('\n'.join(class_names))
    
    # Plot history
    plot_history(history)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nModel saved: cattle_model.h5")
    print(f"Accuracy: {accuracy*100:.2f}%")
    print(f"Classes: class_names.txt")
    print("\nNext: Update app.py to use this model")

if __name__ == "__main__":
    main()
