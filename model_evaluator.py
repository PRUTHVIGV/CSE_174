import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import tensorflow as tf

class ModelEvaluator:
    def __init__(self, breed_names):
        self.breed_names = breed_names
    
    def plot_training_history(self, history):
        """Plot training and validation metrics"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy plot
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Loss plot
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
    
    def evaluate_model(self, model, X_test, y_test):
        """Comprehensive model evaluation"""
        # Predictions
        y_pred_proba = model.predict(X_test)
        y_pred = np.argmax(y_pred_proba, axis=1)
        
        # Accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {accuracy:.4f}")
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.breed_names))
        
        # Confusion matrix
        self.plot_confusion_matrix(y_test, y_pred)
        
        # Per-class metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred, average=None
        )
        
        metrics_df = {
            'Breed': self.breed_names,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Support': support
        }
        
        return metrics_df, accuracy
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.breed_names,
                   yticklabels=self.breed_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    
    def plot_prediction_confidence(self, model, X_test, y_test, num_samples=10):
        """Plot prediction confidence for sample images"""
        predictions = model.predict(X_test[:num_samples])
        
        fig, axes = plt.subplots(2, 5, figsize=(15, 8))
        axes = axes.ravel()
        
        for i in range(num_samples):
            # Display image
            axes[i].imshow(X_test[i])
            
            # Get prediction
            pred_class = np.argmax(predictions[i])
            confidence = np.max(predictions[i])
            true_class = y_test[i]
            
            # Set title with prediction info
            color = 'green' if pred_class == true_class else 'red'
            axes[i].set_title(
                f'True: {self.breed_names[true_class]}\n'
                f'Pred: {self.breed_names[pred_class]}\n'
                f'Conf: {confidence:.2f}',
                color=color, fontsize=8
            )
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    def analyze_misclassifications(self, model, X_test, y_test):
        """Analyze misclassified samples"""
        predictions = model.predict(X_test)
        y_pred = np.argmax(predictions, axis=1)
        
        # Find misclassified samples
        misclassified_idx = np.where(y_pred != y_test)[0]
        
        print(f"Total misclassified samples: {len(misclassified_idx)}")
        
        if len(misclassified_idx) > 0:
            # Show some misclassified examples
            num_show = min(6, len(misclassified_idx))
            fig, axes = plt.subplots(2, 3, figsize=(12, 8))
            axes = axes.ravel()
            
            for i in range(num_show):
                idx = misclassified_idx[i]
                axes[i].imshow(X_test[idx])
                
                true_breed = self.breed_names[y_test[idx]]
                pred_breed = self.breed_names[y_pred[idx]]
                confidence = np.max(predictions[idx])
                
                axes[i].set_title(
                    f'True: {true_breed}\n'
                    f'Predicted: {pred_breed}\n'
                    f'Confidence: {confidence:.2f}',
                    fontsize=8
                )
                axes[i].axis('off')
            
            plt.suptitle('Misclassified Samples')
            plt.tight_layout()
            plt.show()
        
        return misclassified_idx