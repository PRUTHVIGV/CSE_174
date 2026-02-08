import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path

class MobileModelConverter:
    def __init__(self, model_path):
        self.model_path = model_path
        self.breeds = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
    
    def convert_to_tflite(self, output_path='cattle_model.tflite', quantize=True):
        """Convert Keras model to TensorFlow Lite"""
        # Load the model
        model = tf.keras.models.load_model(self.model_path)
        
        # Create converter
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        if quantize:
            # Apply quantization for smaller model size
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            
            # Representative dataset for quantization
            def representative_dataset():
                for _ in range(100):
                    # Generate random data similar to your input
                    data = np.random.random((1, 224, 224, 3)).astype(np.float32)
                    yield [data]
            
            converter.representative_dataset = representative_dataset
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
            converter.inference_input_type = tf.uint8
            converter.inference_output_type = tf.uint8
        
        # Convert model
        tflite_model = converter.convert()
        
        # Save the model
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        print(f"TensorFlow Lite model saved: {output_path}")
        
        # Print model info
        original_size = Path(self.model_path).stat().st_size / (1024 * 1024)
        tflite_size = len(tflite_model) / (1024 * 1024)
        
        print(f"Original model size: {original_size:.2f} MB")
        print(f"TFLite model size: {tflite_size:.2f} MB")
        print(f"Compression ratio: {original_size/tflite_size:.2f}x")
        
        return output_path

class TFLitePredictor:
    def __init__(self, tflite_model_path):
        # Load TFLite model
        self.interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
        self.interpreter.allocate_tensors()
        
        # Get input and output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        self.breeds = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
        
        print(f"Input shape: {self.input_details[0]['shape']}")
        print(f"Input type: {self.input_details[0]['dtype']}")
    
    def preprocess_image(self, image_path):
        """Preprocess image for TFLite model"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        
        # Check if model expects uint8 or float32
        if self.input_details[0]['dtype'] == np.uint8:
            img = img.astype(np.uint8)
        else:
            img = img.astype(np.float32) / 255.0
        
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict(self, image_path):
        """Make prediction using TFLite model"""
        # Preprocess image
        input_data = self.preprocess_image(image_path)
        
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get output
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Process output
        if self.output_details[0]['dtype'] == np.uint8:
            # Dequantize if needed
            scale, zero_point = self.output_details[0]['quantization']
            output_data = scale * (output_data - zero_point)
        
        predictions = output_data[0]
        predicted_class = np.argmax(predictions)
        confidence = np.max(predictions)
        
        breed_name = self.breeds[predicted_class]
        
        return breed_name, confidence, predictions
    
    def benchmark_speed(self, image_path, num_runs=100):
        """Benchmark inference speed"""
        import time
        
        input_data = self.preprocess_image(image_path)
        
        # Warmup
        for _ in range(10):
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
        
        # Benchmark
        start_time = time.time()
        for _ in range(num_runs):
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
        
        end_time = time.time()
        avg_time = (end_time - start_time) / num_runs * 1000  # ms
        
        print(f"Average inference time: {avg_time:.2f} ms")
        print(f"FPS: {1000/avg_time:.1f}")
        
        return avg_time

def create_android_assets():
    """Create assets for Android app"""
    labels_content = """Gir
Sahiwal
Red_Sindhi
Tharparkar
Ongole
Hariana
Kankrej
Rathi
Murrah_Buffalo
Mehsana_Buffalo"""
    
    with open('labels.txt', 'w') as f:
        f.write(labels_content)
    
    print("Created labels.txt for Android app")

def create_flutter_plugin():
    """Create Flutter plugin code template"""
    flutter_code = '''
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:image/image.dart' as img;

class CattleBreedClassifier {
  static const String modelPath = 'assets/cattle_model.tflite';
  static const String labelsPath = 'assets/labels.txt';
  
  Interpreter? _interpreter;
  List<String>? _labels;
  
  Future<void> loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset(modelPath);
      _labels = await _loadLabels();
      print('Model loaded successfully');
    } catch (e) {
      print('Error loading model: $e');
    }
  }
  
  Future<List<String>> _loadLabels() async {
    final labelsData = await rootBundle.loadString(labelsPath);
    return labelsData.split('\\n');
  }
  
  Future<Map<String, dynamic>> classifyImage(File imageFile) async {
    if (_interpreter == null || _labels == null) {
      throw Exception('Model not loaded');
    }
    
    // Preprocess image
    final imageBytes = await imageFile.readAsBytes();
    final image = img.decodeImage(imageBytes)!;
    final resized = img.copyResize(image, width: 224, height: 224);
    
    // Convert to input tensor
    final input = Float32List(1 * 224 * 224 * 3);
    int pixelIndex = 0;
    
    for (int y = 0; y < 224; y++) {
      for (int x = 0; x < 224; x++) {
        final pixel = resized.getPixel(x, y);
        input[pixelIndex++] = img.getRed(pixel) / 255.0;
        input[pixelIndex++] = img.getGreen(pixel) / 255.0;
        input[pixelIndex++] = img.getBlue(pixel) / 255.0;
      }
    }
    
    // Run inference
    final output = Float32List(1 * 10);
    _interpreter!.run(input.reshape([1, 224, 224, 3]), output.reshape([1, 10]));
    
    // Process results
    final predictions = output.toList();
    final maxIndex = predictions.indexOf(predictions.reduce((a, b) => a > b ? a : b));
    
    return {
      'breed': _labels![maxIndex],
      'confidence': predictions[maxIndex],
      'all_predictions': Map.fromIterables(_labels!, predictions),
    };
  }
}
'''.strip()
    
    with open('cattle_classifier.dart', 'w') as f:
        f.write(flutter_code)
    
    print("Created Flutter plugin template: cattle_classifier.dart")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='cattle_breed_model.h5', help='Input Keras model')
    parser.add_argument('--output', default='cattle_model.tflite', help='Output TFLite model')
    parser.add_argument('--quantize', action='store_true', help='Apply quantization')
    parser.add_argument('--test', help='Test image for TFLite model')
    parser.add_argument('--benchmark', help='Benchmark image')
    parser.add_argument('--create-assets', action='store_true', help='Create mobile assets')
    
    args = parser.parse_args()
    
    if args.create_assets:
        create_android_assets()
        create_flutter_plugin()
        return
    
    # Convert model
    converter = MobileModelConverter(args.model)
    tflite_path = converter.convert_to_tflite(args.output, args.quantize)
    
    # Test TFLite model
    if args.test:
        predictor = TFLitePredictor(tflite_path)
        breed, confidence, _ = predictor.predict(args.test)
        print(f"TFLite Prediction: {breed} ({confidence:.3f})")
    
    # Benchmark
    if args.benchmark:
        predictor = TFLitePredictor(tflite_path)
        predictor.benchmark_speed(args.benchmark)

if __name__ == "__main__":
    main()