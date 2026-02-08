import os
import cv2
import numpy as np
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

class DataPreprocessor:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
    
    def create_dataset_structure(self, base_dir):
        """Create directory structure for dataset"""
        breeds = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
        
        for split in ['train', 'validation', 'test']:
            for breed in breeds:
                os.makedirs(os.path.join(base_dir, split, breed), exist_ok=True)
        
        print(f"Dataset structure created at {base_dir}")
    
    def augment_image(self, image):
        """Apply data augmentation to image"""
        augmented_images = []
        
        # Original image
        augmented_images.append(image)
        
        # Horizontal flip
        augmented_images.append(cv2.flip(image, 1))
        
        # Rotation
        rows, cols = image.shape[:2]
        for angle in [15, -15]:
            M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
            rotated = cv2.warpAffine(image, M, (cols, rows))
            augmented_images.append(rotated)
        
        # Brightness adjustment
        bright = cv2.convertScaleAbs(image, alpha=1.2, beta=30)
        dark = cv2.convertScaleAbs(image, alpha=0.8, beta=-30)
        augmented_images.extend([bright, dark])
        
        return augmented_images
    
    def preprocess_batch(self, image_paths, labels):
        """Preprocess batch of images"""
        processed_images = []
        processed_labels = []
        
        for img_path, label in zip(image_paths, labels):
            try:
                # Load and resize image
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, self.target_size)
                
                # Apply augmentation
                augmented = self.augment_image(img)
                processed_images.extend(augmented)
                processed_labels.extend([label] * len(augmented))
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        return np.array(processed_images), np.array(processed_labels)
    
    def visualize_samples(self, images, labels, breed_names, num_samples=8):
        """Visualize sample images from dataset"""
        plt.figure(figsize=(15, 8))
        
        for i in range(min(num_samples, len(images))):
            plt.subplot(2, 4, i + 1)
            plt.imshow(images[i])
            plt.title(f'Breed: {breed_names[labels[i]]}')
            plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def get_dataset_stats(self, data_dir):
        """Get statistics about the dataset"""
        stats = {}
        total_images = 0
        
        for breed in os.listdir(data_dir):
            breed_path = os.path.join(data_dir, breed)
            if os.path.isdir(breed_path):
                count = len([f for f in os.listdir(breed_path) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                stats[breed] = count
                total_images += count
        
        print(f"Dataset Statistics:")
        print(f"Total images: {total_images}")
        for breed, count in stats.items():
            print(f"{breed}: {count} images")
        
        return stats