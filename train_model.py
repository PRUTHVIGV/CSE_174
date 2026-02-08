from cattle_breed_model import CattleBreedRecognizer
from data_preprocessor import DataPreprocessor
from model_evaluator import ModelEvaluator
import os

def main():
    # Configuration
    DATA_DIR = "dataset"  # Update with your dataset path
    IMG_SIZE = (224, 224)
    NUM_CLASSES = 10
    EPOCHS = 50
    BATCH_SIZE = 32
    
    # Indian cattle and buffalo breeds
    BREED_NAMES = [
        'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
        'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
    ]
    
    print("=== Cattle Breed Recognition Model Training ===")
    
    # Initialize components
    recognizer = CattleBreedRecognizer(
        img_height=IMG_SIZE[0], 
        img_width=IMG_SIZE[1], 
        num_classes=NUM_CLASSES
    )
    
    preprocessor = DataPreprocessor(target_size=IMG_SIZE)
    evaluator = ModelEvaluator(BREED_NAMES)
    
    # Create dataset structure if needed
    if not os.path.exists(DATA_DIR):
        print("Creating dataset structure...")
        preprocessor.create_dataset_structure(DATA_DIR)
        print("Please add your images to the created directories and run again.")
        return
    
    # Build model
    print("Building model...")
    model = recognizer.build_model()
    model.summary()
    
    # Check if dataset exists and has images
    try:
        stats = preprocessor.get_dataset_stats(DATA_DIR)
        if sum(stats.values()) == 0:
            print("No images found in dataset. Please add images and try again.")
            return
    except:
        print("Dataset directory structure not found. Creating it...")
        preprocessor.create_dataset_structure(DATA_DIR)
        return
    
    # Train model
    print("Starting training...")
    history = recognizer.train(DATA_DIR, epochs=EPOCHS, batch_size=BATCH_SIZE)
    
    # Plot training history
    evaluator.plot_training_history(history)
    
    # Save model
    recognizer.save_model("cattle_breed_model.h5")
    print("Model saved as 'cattle_breed_model.h5'")
    
    # Load test data for evaluation
    X_train, X_test, y_train, y_test = recognizer.load_dataset(DATA_DIR)
    
    # Evaluate model
    print("Evaluating model...")
    metrics, accuracy = evaluator.evaluate_model(model, X_test, y_test)
    
    # Show prediction confidence
    evaluator.plot_prediction_confidence(model, X_test, y_test)
    
    # Analyze misclassifications
    evaluator.analyze_misclassifications(model, X_test, y_test)
    
    print(f"Training completed! Final accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()