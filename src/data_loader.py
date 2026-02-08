import tensorflow as tf
from pathlib import Path
import numpy as np
from PIL import Image

class DataLoader:
    def __init__(self, img_size=224, batch_size=32):
        self.img_size = img_size
        self.batch_size = batch_size
        
    def create_dataset(self, data_dir, validation_split=0.2, augment=True):
        data_dir = Path(data_dir)
        
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir, validation_split=validation_split, subset="training", seed=123,
            image_size=(self.img_size, self.img_size), batch_size=self.batch_size)
        
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir, validation_split=validation_split, subset="validation", seed=123,
            image_size=(self.img_size, self.img_size), batch_size=self.batch_size)
        
        self.class_names = train_ds.class_names
        
        if augment:
            train_ds = train_ds.map(self._augment, num_parallel_calls=tf.data.AUTOTUNE)
        
        train_ds = train_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
        val_ds = val_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
        
        return train_ds, val_ds, self.class_names
    
    def _augment(self, image, label):
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
        ])
        return data_augmentation(image, training=True), label
    
    def load_and_preprocess_image(self, image_path):
        img = Image.open(image_path).convert('RGB')
        img = img.resize((self.img_size, self.img_size))
        return np.array(img)
    
    def create_sample_dataset_structure(self, base_dir):
        breeds = ['Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
                  'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo']
        base_path = Path(base_dir)
        for breed in breeds:
            (base_path / breed).mkdir(parents=True, exist_ok=True)
        print(f"Dataset structure created at {base_dir}")
        for breed in breeds:
            print(f"  - {base_dir}/{breed}/")
