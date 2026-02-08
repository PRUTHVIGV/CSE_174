import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
import random
import os
from PIL import Image, ImageEnhance, ImageFilter

class AdvancedAugmentation:
    def __init__(self):
        self.transform = A.Compose([
            A.RandomRotate90(p=0.3),
            A.Flip(p=0.5),
            A.Transpose(p=0.3),
            A.OneOf([
                A.GaussNoise(var_limit=(10, 50)),
                A.GaussianBlur(blur_limit=3),
                A.MotionBlur(blur_limit=3),
            ], p=0.3),
            A.OneOf([
                A.OpticalDistortion(distort_limit=0.1),
                A.GridDistortion(distort_limit=0.1),
                A.ElasticTransform(alpha=1, sigma=50),
            ], p=0.2),
            A.OneOf([
                A.CLAHE(clip_limit=2),
                A.Sharpen(),
                A.Emboss(),
                A.RandomBrightnessContrast(),
            ], p=0.3),
            A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.3),
            A.RandomShadow(p=0.2),
            A.RandomFog(p=0.1),
            A.RandomRain(p=0.1),
            A.RandomSunFlare(p=0.1),
            A.CoarseDropout(max_holes=8, max_height=32, max_width=32, p=0.2),
        ])
    
    def augment_image(self, image):
        """Apply advanced augmentation"""
        if isinstance(image, str):
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        augmented = self.transform(image=image)
        return augmented['image']
    
    def generate_augmented_dataset(self, input_dir, output_dir, multiplier=5):
        """Generate augmented dataset"""
        os.makedirs(output_dir, exist_ok=True)
        
        for breed_folder in os.listdir(input_dir):
            breed_path = os.path.join(input_dir, breed_folder)
            if not os.path.isdir(breed_path):
                continue
            
            output_breed_path = os.path.join(output_dir, breed_folder)
            os.makedirs(output_breed_path, exist_ok=True)
            
            images = [f for f in os.listdir(breed_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            for img_file in images:
                img_path = os.path.join(breed_path, img_file)
                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Save original
                original_name = f"orig_{img_file}"
                cv2.imwrite(os.path.join(output_breed_path, original_name), 
                           cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                
                # Generate augmented versions
                for i in range(multiplier):
                    augmented = self.augment_image(image)
                    aug_name = f"aug_{i}_{img_file}"
                    cv2.imwrite(os.path.join(output_breed_path, aug_name), 
                               cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))
            
            print(f"Processed {breed_folder}: {len(images)} -> {len(images) * (multiplier + 1)} images")

class SyntheticDataGenerator:
    def __init__(self):
        self.background_colors = [
            (135, 206, 235),  # Sky blue
            (34, 139, 34),    # Forest green
            (210, 180, 140),  # Tan
            (128, 128, 128),  # Gray
        ]
    
    def create_synthetic_variations(self, image_path, num_variations=10):
        """Create synthetic variations of an image"""
        image = Image.open(image_path)
        variations = []
        
        for i in range(num_variations):
            # Random transformations
            variation = image.copy()
            
            # Color adjustments
            if random.random() > 0.5:
                enhancer = ImageEnhance.Color(variation)
                variation = enhancer.enhance(random.uniform(0.8, 1.2))
            
            # Brightness
            if random.random() > 0.5:
                enhancer = ImageEnhance.Brightness(variation)
                variation = enhancer.enhance(random.uniform(0.8, 1.2))
            
            # Contrast
            if random.random() > 0.5:
                enhancer = ImageEnhance.Contrast(variation)
                variation = enhancer.enhance(random.uniform(0.8, 1.2))
            
            # Sharpness
            if random.random() > 0.5:
                enhancer = ImageEnhance.Sharpness(variation)
                variation = enhancer.enhance(random.uniform(0.8, 1.2))
            
            # Add noise
            if random.random() > 0.7:
                variation = self.add_noise(variation)
            
            # Background replacement
            if random.random() > 0.8:
                variation = self.replace_background(variation)
            
            variations.append(variation)
        
        return variations
    
    def add_noise(self, image):
        """Add random noise to image"""
        img_array = np.array(image)
        noise = np.random.randint(0, 25, img_array.shape, dtype=np.uint8)
        noisy_img = cv2.add(img_array, noise)
        return Image.fromarray(noisy_img)
    
    def replace_background(self, image):
        """Replace background with random color"""
        # Simple background replacement (you can use more sophisticated methods)
        img_array = np.array(image)
        
        # Create a simple mask (this is very basic - use proper segmentation for better results)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Choose random background color
        bg_color = random.choice(self.background_colors)
        
        # Apply background
        result = img_array.copy()
        result[mask == 0] = bg_color
        
        return Image.fromarray(result)

class DataBalancer:
    def __init__(self, target_samples_per_class=1000):
        self.target_samples = target_samples_per_class
        self.augmenter = AdvancedAugmentation()
        self.synthetic_gen = SyntheticDataGenerator()
    
    def balance_dataset(self, dataset_dir):
        """Balance dataset by generating more samples for underrepresented classes"""
        class_counts = {}
        
        # Count samples per class
        for breed_folder in os.listdir(dataset_dir):
            breed_path = os.path.join(dataset_dir, breed_folder)
            if os.path.isdir(breed_path):
                count = len([f for f in os.listdir(breed_path) 
                           if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                class_counts[breed_folder] = count
        
        print("Current class distribution:")
        for breed, count in class_counts.items():
            print(f"{breed}: {count} samples")
        
        # Generate additional samples for underrepresented classes
        for breed_folder, current_count in class_counts.items():
            if current_count < self.target_samples:
                needed = self.target_samples - current_count
                breed_path = os.path.join(dataset_dir, breed_folder)
                
                print(f"Generating {needed} additional samples for {breed_folder}")
                
                # Get existing images
                existing_images = [f for f in os.listdir(breed_path) 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                generated = 0
                while generated < needed:
                    # Pick random existing image
                    source_img = random.choice(existing_images)
                    source_path = os.path.join(breed_path, source_img)
                    
                    # Generate augmented version
                    image = cv2.imread(source_path)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    augmented = self.augmenter.augment_image(image)
                    
                    # Save augmented image
                    output_name = f"balanced_{generated}_{source_img}"
                    output_path = os.path.join(breed_path, output_name)
                    cv2.imwrite(output_path, cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))
                    
                    generated += 1
                
                print(f"Completed {breed_folder}: {current_count} -> {self.target_samples}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True, help='Input dataset directory')
    parser.add_argument('--output-dir', help='Output directory for augmented data')
    parser.add_argument('--balance', action='store_true', help='Balance dataset')
    parser.add_argument('--augment', action='store_true', help='Generate augmented dataset')
    parser.add_argument('--multiplier', type=int, default=5, help='Augmentation multiplier')
    parser.add_argument('--target-samples', type=int, default=1000, help='Target samples per class')
    
    args = parser.parse_args()
    
    if args.balance:
        balancer = DataBalancer(args.target_samples)
        balancer.balance_dataset(args.input_dir)
    
    if args.augment:
        if not args.output_dir:
            args.output_dir = args.input_dir + "_augmented"
        
        augmenter = AdvancedAugmentation()
        augmenter.generate_augmented_dataset(args.input_dir, args.output_dir, args.multiplier)

if __name__ == "__main__":
    main()