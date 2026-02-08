import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
import numpy as np

class CattleBreedModel:
    def __init__(self, num_classes=10, img_size=224):
        self.num_classes = num_classes
        self.img_size = img_size
        self.model = None
        
    def build_model(self):
        base_model = MobileNetV2(input_shape=(self.img_size, self.img_size, 3), include_top=False, weights='imagenet')
        base_model.trainable = False
        
        inputs = keras.Input(shape=(self.img_size, self.img_size, 3))
        x = keras.applications.mobilenet_v2.preprocess_input(inputs)
        x = base_model(x, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        self.model.compile(optimizer=keras.optimizers.Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        return self.model
    
    def fine_tune(self, base_layers_to_unfreeze=30):
        base_model = self.model.layers[2]
        base_model.trainable = True
        for layer in base_model.layers[:-base_layers_to_unfreeze]:
            layer.trainable = False
        self.model.compile(optimizer=keras.optimizers.Adam(0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    
    def train(self, train_ds, val_ds, epochs=20, fine_tune_epochs=10):
        print("Phase 1: Training top layers...")
        history1 = self.model.fit(train_ds, validation_data=val_ds, epochs=epochs, 
                                   callbacks=[keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                                            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3)])
        print("\nPhase 2: Fine-tuning...")
        self.fine_tune()
        history2 = self.model.fit(train_ds, validation_data=val_ds, epochs=fine_tune_epochs,
                                   callbacks=[keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)])
        return history1, history2
    
    def predict(self, image):
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        return self.model.predict(image, verbose=0)[0]
    
    def save(self, path):
        self.model.save(path)
        print(f"Model saved to {path}")
    
    def load(self, path):
        self.model = keras.models.load_model(path)
        print(f"Model loaded from {path}")
