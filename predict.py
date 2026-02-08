import cv2
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import argparse

class BreedPredictor:
    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)
        self.breed_names = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
        self.img_size = (224, 224)
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.img_size)
        img = np.expand_dims(img, axis=0)
        return img / 255.0
    
    def predict_breed(self, image_path, show_image=True):
        """Predict breed from image"""
        # Preprocess image
        processed_img = self.preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(processed_img)
        predicted_class = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        # Get breed name
        breed_name = self.breed_names[predicted_class]
        
        # Show results
        if show_image:
            self.display_prediction(image_path, breed_name, confidence, predictions[0])
        
        return breed_name, confidence, predictions[0]
    
    def display_prediction(self, image_path, breed_name, confidence, all_predictions):
        """Display image with prediction results"""
        # Load and display image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Show image
        ax1.imshow(img)
        ax1.set_title(f'Predicted: {breed_name}\nConfidence: {confidence:.2f}')
        ax1.axis('off')
        
        # Show prediction probabilities
        ax2.barh(self.breed_names, all_predictions)
        ax2.set_xlabel('Probability')
        ax2.set_title('Breed Probabilities')
        ax2.set_xlim(0, 1)
        
        plt.tight_layout()
        plt.show()
        
        # Print detailed results
        print(f"\nPrediction Results:")
        print(f"Predicted Breed: {breed_name}")
        print(f"Confidence: {confidence:.4f}")
        print(f"\nTop 3 predictions:")
        
        # Get top 3 predictions
        top_indices = np.argsort(all_predictions)[-3:][::-1]
        for i, idx in enumerate(top_indices):
            print(f"{i+1}. {self.breed_names[idx]}: {all_predictions[idx]:.4f}")
    
    def batch_predict(self, image_paths):
        """Predict breeds for multiple images"""
        results = []
        
        for img_path in image_paths:
            try:
                breed, confidence, _ = self.predict_breed(img_path, show_image=False)
                results.append({
                    'image': img_path,
                    'breed': breed,
                    'confidence': confidence
                })
                print(f"{img_path}: {breed} ({confidence:.3f})")
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Cattle Breed Recognition Inference')
    parser.add_argument('--model', default='cattle_breed_model.h5', 
                       help='Path to trained model')
    parser.add_argument('--image', required=True, 
                       help='Path to image for prediction')
    parser.add_argument('--batch', nargs='+', 
                       help='Multiple image paths for batch prediction')
    
    args = parser.parse_args()
    
    # Initialize predictor
    try:
        predictor = BreedPredictor(args.model)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Single image prediction
    if args.image and not args.batch:
        try:
            breed, confidence, _ = predictor.predict_breed(args.image)
            print(f"\nFinal Result: {breed} (Confidence: {confidence:.4f})")
        except Exception as e:
            print(f"Error predicting image: {e}")
    
    # Batch prediction
    elif args.batch:
        results = predictor.batch_predict(args.batch)
        print(f"\nProcessed {len(results)} images successfully")

if __name__ == "__main__":
    # Example usage without command line arguments
    # predictor = BreedPredictor('cattle_breed_model.h5')
    # breed, confidence, _ = predictor.predict_breed('path/to/your/image.jpg')
    main()