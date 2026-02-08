import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model

class GradCAM:
    def __init__(self, model, layer_name=None):
        self.model = model
        self.layer_name = layer_name or self.find_target_layer()
        
    def find_target_layer(self):
        """Find the last convolutional layer"""
        for layer in reversed(self.model.layers):
            if len(layer.output_shape) == 4:
                return layer.name
        raise ValueError("Could not find 4D layer")
    
    def make_gradcam_heatmap(self, img_array, pred_index=None):
        grad_model = Model(
            inputs=[self.model.inputs],
            outputs=[self.model.get_layer(self.layer_name).output, self.model.output]
        )
        
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]
        
        grads = tape.gradient(class_channel, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        return heatmap.numpy()
    
    def visualize_gradcam(self, img_path, breed_names, alpha=0.4):
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        img_array = np.expand_dims(img, axis=0) / 255.0
        
        # Get prediction
        preds = self.model.predict(img_array)
        pred_class = np.argmax(preds[0])
        confidence = np.max(preds[0])
        
        # Generate heatmap
        heatmap = self.make_gradcam_heatmap(img_array, pred_class)
        heatmap = cv2.resize(heatmap, (224, 224))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Overlay heatmap
        superimposed_img = heatmap * alpha + img * (1 - alpha)
        superimposed_img = np.uint8(superimposed_img)
        
        # Plot results
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original Image')
        axes[0].axis('off')
        
        axes[1].imshow(heatmap)
        axes[1].set_title('GradCAM Heatmap')
        axes[1].axis('off')
        
        axes[2].imshow(cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB))
        axes[2].set_title(f'Prediction: {breed_names[pred_class]}\nConfidence: {confidence:.3f}')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        return superimposed_img, breed_names[pred_class], confidence

class LIME_Explainer:
    def __init__(self, model, breed_names):
        self.model = model
        self.breed_names = breed_names
    
    def explain_instance(self, image_path, num_samples=1000):
        from lime import lime_image
        from skimage.segmentation import mark_boundaries
        
        explainer = lime_image.LimeImageExplainer()
        
        image = cv2.imread(image_path)
        image = cv2.resize(image, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        def predict_fn(images):
            processed = images / 255.0
            return self.model.predict(processed)
        
        explanation = explainer.explain_instance(
            image, predict_fn, top_labels=3, hide_color=0, num_samples=num_samples
        )
        
        temp, mask = explanation.get_image_and_mask(
            explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False
        )
        
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        plt.imshow(image)
        plt.title('Original')
        plt.axis('off')
        
        plt.subplot(1, 3, 2)
        plt.imshow(mark_boundaries(temp / 255.0, mask))
        plt.title('LIME Explanation')
        plt.axis('off')
        
        plt.subplot(1, 3, 3)
        plt.imshow(mask, cmap='gray')
        plt.title('Important Regions')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        return explanation

class FeatureVisualization:
    def __init__(self, model):
        self.model = model
    
    def visualize_filters(self, layer_name, num_filters=16):
        """Visualize convolutional filters"""
        layer = self.model.get_layer(layer_name)
        filters = layer.get_weights()[0]
        
        fig, axes = plt.subplots(4, 4, figsize=(12, 12))
        axes = axes.ravel()
        
        for i in range(min(num_filters, 16)):
            f = filters[:, :, :, i]
            f = (f - f.min()) / (f.max() - f.min())
            
            if f.shape[2] == 3:
                axes[i].imshow(f)
            else:
                axes[i].imshow(f[:, :, 0], cmap='viridis')
            
            axes[i].set_title(f'Filter {i}')
            axes[i].axis('off')
        
        plt.suptitle(f'Filters from {layer_name}')
        plt.tight_layout()
        plt.show()
    
    def visualize_feature_maps(self, image_path, layer_name):
        """Visualize feature maps for a specific image"""
        img = cv2.imread(image_path)
        img = cv2.resize(img, (224, 224))
        img_array = np.expand_dims(img, axis=0) / 255.0
        
        # Create model to output feature maps
        feature_model = Model(inputs=self.model.input, 
                            outputs=self.model.get_layer(layer_name).output)
        
        feature_maps = feature_model.predict(img_array)
        
        # Plot feature maps
        num_features = min(16, feature_maps.shape[-1])
        fig, axes = plt.subplots(4, 4, figsize=(12, 12))
        axes = axes.ravel()
        
        for i in range(num_features):
            axes[i].imshow(feature_maps[0, :, :, i], cmap='viridis')
            axes[i].set_title(f'Feature {i}')
            axes[i].axis('off')
        
        plt.suptitle(f'Feature Maps from {layer_name}')
        plt.tight_layout()
        plt.show()

class ModelAnalyzer:
    def __init__(self, model, breed_names):
        self.model = model
        self.breed_names = breed_names
        self.gradcam = GradCAM(model)
        self.lime = LIME_Explainer(model, breed_names)
        self.feature_viz = FeatureVisualization(model)
    
    def comprehensive_analysis(self, image_path):
        """Perform comprehensive model analysis"""
        print("🔍 Comprehensive Model Analysis")
        print("=" * 50)
        
        # 1. Basic prediction
        img = cv2.imread(image_path)
        img = cv2.resize(img, (224, 224))
        img_array = np.expand_dims(img, axis=0) / 255.0
        
        preds = self.model.predict(img_array)
        pred_class = np.argmax(preds[0])
        confidence = np.max(preds[0])
        
        print(f"Prediction: {self.breed_names[pred_class]}")
        print(f"Confidence: {confidence:.4f}")
        
        # 2. Top-3 predictions
        top_3_idx = np.argsort(preds[0])[-3:][::-1]
        print("\nTop 3 Predictions:")
        for i, idx in enumerate(top_3_idx):
            print(f"{i+1}. {self.breed_names[idx]}: {preds[0][idx]:.4f}")
        
        # 3. GradCAM visualization
        print("\n📊 Generating GradCAM visualization...")
        self.gradcam.visualize_gradcam(image_path, self.breed_names)
        
        # 4. LIME explanation
        print("\n🔬 Generating LIME explanation...")
        self.lime.explain_instance(image_path)
        
        # 5. Uncertainty analysis
        print("\n📈 Uncertainty Analysis:")
        entropy = -np.sum(preds[0] * np.log(preds[0] + 1e-8))
        print(f"Prediction Entropy: {entropy:.4f}")
        print(f"Uncertainty Level: {'High' if entropy > 1.5 else 'Medium' if entropy > 0.8 else 'Low'}")
        
        return {
            'prediction': self.breed_names[pred_class],
            'confidence': confidence,
            'entropy': entropy,
            'top_3': [(self.breed_names[idx], preds[0][idx]) for idx in top_3_idx]
        }

def create_interpretability_dashboard(model, breed_names):
    """Create interactive dashboard for model interpretability"""
    import streamlit as st
    
    st.title("🐄 Cattle Breed Recognition - Model Interpretability")
    
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Save uploaded file
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display image
        st.image("temp_image.jpg", caption="Uploaded Image", use_column_width=True)
        
        # Analysis options
        analysis_type = st.selectbox(
            "Choose Analysis Type:",
            ["Basic Prediction", "GradCAM", "LIME", "Comprehensive"]
        )
        
        if st.button("Analyze"):
            analyzer = ModelAnalyzer(model, breed_names)
            
            if analysis_type == "Basic Prediction":
                result = analyzer.comprehensive_analysis("temp_image.jpg")
                st.write(f"**Prediction:** {result['prediction']}")
                st.write(f"**Confidence:** {result['confidence']:.4f}")
            
            elif analysis_type == "GradCAM":
                analyzer.gradcam.visualize_gradcam("temp_image.jpg", breed_names)
                st.pyplot()
            
            elif analysis_type == "LIME":
                analyzer.lime.explain_instance("temp_image.jpg")
                st.pyplot()
            
            elif analysis_type == "Comprehensive":
                result = analyzer.comprehensive_analysis("temp_image.jpg")
                st.json(result)

if __name__ == "__main__":
    print("Model Interpretability Tools Ready!")
    print("Features:")
    print("- GradCAM visualization")
    print("- LIME explanations") 
    print("- Feature map visualization")
    print("- Comprehensive analysis")
    print("- Interactive dashboard")