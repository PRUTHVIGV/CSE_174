import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import matplotlib.pyplot as plt

class CattleBreedRecognizer:
    def __init__(self, img_height=224, img_width=224, num_classes=10):
        self.img_height = img_height
        self.img_width = img_width
        self.num_classes = num_classes
        self.model = None
        self.label_encoder = LabelEncoder()
        
        # Common Indian cattle and buffalo breeds
        self.breed_classes = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
    
    def build_model(self):
        """Build CNN model for breed classification"""
        model = keras.Sequential([
            layers.Rescaling(1./255, input_shape=(self.img_height, self.img_width, 3)),
            
            # First Conv Block
            layers.Conv2D(32, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.BatchNormalization(),
            
            # Second Conv Block
            layers.Conv2D(64, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.BatchNormalization(),
            
            # Third Conv Block
            layers.Conv2D(128, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.BatchNormalization(),
            
            # Fourth Conv Block
            layers.Conv2D(256, 3, activation='relu'),
            layers.MaxPooling2D(),
            layers.BatchNormalization(),
            
            # Flatten and Dense layers
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def preprocess_image(self, image_path):
        """Preprocess single image for prediction"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.img_width, self.img_height))
        img = np.expand_dims(img, axis=0)
        return img / 255.0
    
    def load_dataset(self, data_dir):
        """Load and preprocess dataset"""
        images = []
        labels = []
        
        for breed in os.listdir(data_dir):
            breed_path = os.path.join(data_dir, breed)
            if os.path.isdir(breed_path):
                for img_file in os.listdir(breed_path):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(breed_path, img_file)
                        try:
                            img = cv2.imread(img_path)
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, (self.img_width, self.img_height))
                            images.append(img)
                            labels.append(breed)
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
        
        images = np.array(images)
        labels = self.label_encoder.fit_transform(labels)
        
        return train_test_split(images, labels, test_size=0.2, random_state=42)
    
    def train(self, data_dir, epochs=50, batch_size=32):
        """Train the model"""
        X_train, X_test, y_train, y_test = self.load_dataset(data_dir)
        
        # Data augmentation
        datagen = keras.preprocessing.image.ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            fill_mode='nearest'
        )
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.2, patience=5),
            keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True)
        ]
        
        # Train model
        history = self.model.fit(
            datagen.flow(X_train, y_train, batch_size=batch_size),
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=callbacks
        )
        
        return history
    
    def predict(self, image_path):
        """Predict breed from image"""
        img = self.preprocess_image(image_path)
        prediction = self.model.predict(img)
        predicted_class = np.argmax(prediction[0])
        confidence = np.max(prediction[0])
        
        breed_name = self.label_encoder.inverse_transform([predicted_class])[0]
        return breed_name, confidence
    
    def save_model(self, filepath):
        """Save trained model"""
        self.model.save(filepath)
    
    def load_model(self, filepath):
        """Load pre-trained model"""
        self.model = keras.models.load_model(filepath)

# Example usage
if __name__ == "__main__":
    # Initialize recognizer
    recognizer = CattleBreedRecognizer(num_classes=10)
    
    # Build model
    model = recognizer.build_model()
    model.summary()
    
    # Train model (uncomment when you have dataset)
    # history = recognizer.train('path/to/your/dataset')
    
    # Make prediction (uncomment when model is trained)
    # breed, confidence = recognizer.predict('path/to/test/image.jpg')
    # print(f"Predicted breed: {breed} (Confidence: {confidence:.2f})")