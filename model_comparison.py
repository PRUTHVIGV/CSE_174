import tensorflow as tf
from tensorflow.keras.applications import ResNet50, EfficientNetB0, VGG16, InceptionV3, MobileNetV2
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import pickle

class ModelComparison:
    def __init__(self, num_classes=10, img_size=(224, 224)):
        self.num_classes = num_classes
        self.img_size = img_size
        self.models = {}
        self.histories = {}
        self.results = {}
        
        self.breed_names = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
    
    def create_model(self, model_type):
        """Create different model architectures"""
        input_shape = (*self.img_size, 3)
        
        if model_type == 'resnet50':
            base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
        elif model_type == 'efficientnet':
            base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)
        elif model_type == 'vgg16':
            base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
        elif model_type == 'inception':
            base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
        elif model_type == 'mobilenet':
            base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
        elif model_type == 'custom_cnn':
            return self.create_custom_cnn()
        
        base_model.trainable = False
        
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def create_custom_cnn(self):
        """Create custom CNN architecture"""
        model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1./255, input_shape=(*self.img_size, 3)),
            
            # Block 1
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.BatchNormalization(),
            
            # Block 2
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.BatchNormalization(),
            
            # Block 3
            tf.keras.layers.Conv2D(256, 3, activation='relu'),
            tf.keras.layers.Conv2D(256, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.BatchNormalization(),
            
            # Block 4
            tf.keras.layers.Conv2D(512, 3, activation='relu'),
            tf.keras.layers.Conv2D(512, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.BatchNormalization(),
            
            # Classifier
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(1024, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_all_models(self, X_train, y_train, X_val, y_val, epochs=30):
        """Train multiple models for comparison"""
        model_types = ['resnet50', 'efficientnet', 'vgg16', 'mobilenet', 'custom_cnn']
        
        for model_type in model_types:
            print(f"\nTraining {model_type}...")
            
            model = self.create_model(model_type)
            
            callbacks = [
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                tf.keras.callbacks.ReduceLROnPlateau(factor=0.2, patience=5),
                tf.keras.callbacks.ModelCheckpoint(f'{model_type}_best.h5', save_best_only=True)
            ]
            
            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=32,
                callbacks=callbacks,
                verbose=1
            )
            
            self.models[model_type] = model
            self.histories[model_type] = history
            
            print(f"{model_type} training completed!")
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all trained models"""
        for model_type, model in self.models.items():
            print(f"\nEvaluating {model_type}...")
            
            # Predictions
            y_pred_proba = model.predict(X_test)
            y_pred = np.argmax(y_pred_proba, axis=1)
            
            # Metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            self.results[model_type] = {
                'accuracy': accuracy,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'classification_report': classification_report(y_test, y_pred, target_names=self.breed_names)
            }
            
            print(f"{model_type} Accuracy: {accuracy:.4f}")
    
    def plot_comparison(self):
        """Plot model comparison results"""
        # Training history comparison
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Training accuracy
        for model_type, history in self.histories.items():
            ax1.plot(history.history['accuracy'], label=f'{model_type} train')
            ax2.plot(history.history['val_accuracy'], label=f'{model_type} val')
        
        ax1.set_title('Training Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        ax2.set_title('Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        
        # Training loss
        for model_type, history in self.histories.items():
            ax3.plot(history.history['loss'], label=f'{model_type} train')
            ax4.plot(history.history['val_loss'], label=f'{model_type} val')
        
        ax3.set_title('Training Loss')
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('Loss')
        ax3.legend()
        
        ax4.set_title('Validation Loss')
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Loss')
        ax4.legend()
        
        plt.tight_layout()
        plt.show()
        
        # Accuracy comparison bar plot
        accuracies = [self.results[model]['accuracy'] for model in self.results.keys()]
        model_names = list(self.results.keys())
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(model_names, accuracies)
        plt.title('Model Accuracy Comparison')
        plt.ylabel('Accuracy')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{acc:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()

class EnsembleModel:
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights or [1.0] * len(models)
        self.breed_names = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
    
    def predict(self, X):
        """Ensemble prediction using weighted voting"""
        predictions = []
        
        for model, weight in zip(self.models, self.weights):
            pred = model.predict(X)
            predictions.append(pred * weight)
        
        # Average predictions
        ensemble_pred = np.mean(predictions, axis=0)
        return ensemble_pred
    
    def predict_with_confidence(self, X):
        """Predict with confidence intervals"""
        all_predictions = []
        
        for model in self.models:
            pred = model.predict(X)
            all_predictions.append(pred)
        
        all_predictions = np.array(all_predictions)
        
        # Mean and std across models
        mean_pred = np.mean(all_predictions, axis=0)
        std_pred = np.std(all_predictions, axis=0)
        
        # Predicted classes
        pred_classes = np.argmax(mean_pred, axis=1)
        
        # Confidence as inverse of std
        confidence = 1 - np.mean(std_pred, axis=1)
        
        return pred_classes, confidence, mean_pred
    
    def evaluate_ensemble(self, X_test, y_test):
        """Evaluate ensemble performance"""
        pred_classes, confidence, probabilities = self.predict_with_confidence(X_test)
        
        accuracy = accuracy_score(y_test, pred_classes)
        
        print(f"Ensemble Accuracy: {accuracy:.4f}")
        print(f"Average Confidence: {np.mean(confidence):.4f}")
        
        # Classification report
        print("\nEnsemble Classification Report:")
        print(classification_report(y_test, pred_classes, target_names=self.breed_names))
        
        return accuracy, confidence, probabilities

class AutoML:
    def __init__(self, num_classes=10):
        self.num_classes = num_classes
        self.best_model = None
        self.best_score = 0
        
    def hyperparameter_search(self, X_train, y_train, X_val, y_val):
        """Simple hyperparameter search"""
        param_grid = {
            'learning_rate': [0.001, 0.0001, 0.00001],
            'dropout_rate': [0.3, 0.5, 0.7],
            'dense_units': [256, 512, 1024],
            'batch_size': [16, 32, 64]
        }
        
        best_params = {}
        
        for lr in param_grid['learning_rate']:
            for dropout in param_grid['dropout_rate']:
                for units in param_grid['dense_units']:
                    for batch_size in param_grid['batch_size']:
                        
                        print(f"Testing: lr={lr}, dropout={dropout}, units={units}, batch_size={batch_size}")
                        
                        # Create model with current parameters
                        model = self.create_tuned_model(lr, dropout, units)
                        
                        # Train for few epochs
                        history = model.fit(
                            X_train, y_train,
                            validation_data=(X_val, y_val),
                            epochs=10,
                            batch_size=batch_size,
                            verbose=0
                        )
                        
                        # Get best validation accuracy
                        val_acc = max(history.history['val_accuracy'])
                        
                        if val_acc > self.best_score:
                            self.best_score = val_acc
                            self.best_model = model
                            best_params = {
                                'learning_rate': lr,
                                'dropout_rate': dropout,
                                'dense_units': units,
                                'batch_size': batch_size
                            }
                            
                            print(f"New best score: {val_acc:.4f}")
        
        print(f"\nBest parameters: {best_params}")
        print(f"Best validation accuracy: {self.best_score:.4f}")
        
        return best_params
    
    def create_tuned_model(self, learning_rate, dropout_rate, dense_units):
        """Create model with specific hyperparameters"""
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False
        
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(dropout_rate),
            tf.keras.layers.Dense(dense_units, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(dropout_rate),
            tf.keras.layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

def save_comparison_results(comparison, filename='model_comparison.pkl'):
    """Save comparison results"""
    results = {
        'results': comparison.results,
        'histories': comparison.histories
    }
    
    with open(filename, 'wb') as f:
        pickle.dump(results, f)
    
    print(f"Results saved to {filename}")

def load_comparison_results(filename='model_comparison.pkl'):
    """Load comparison results"""
    with open(filename, 'rb') as f:
        results = pickle.load(f)
    
    return results

def main():
    # Example usage
    print("Model Comparison and Ensemble System")
    print("This module provides:")
    print("1. Multiple model architectures comparison")
    print("2. Ensemble methods")
    print("3. Hyperparameter tuning")
    print("4. AutoML capabilities")

if __name__ == "__main__":
    main()