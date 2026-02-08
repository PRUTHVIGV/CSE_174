import cv2
import numpy as np
import tensorflow as tf
from collections import deque
import time

class RealTimePredictor:
    def __init__(self, model_path, confidence_threshold=0.7):
        self.model = tf.keras.models.load_model(model_path)
        self.breeds = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
        self.confidence_threshold = confidence_threshold
        self.prediction_buffer = deque(maxlen=10)  # Smooth predictions
        self.frame_count = 0
        self.prediction_interval = 5  # Predict every 5 frames
    
    def preprocess_frame(self, frame):
        """Preprocess frame for prediction"""
        resized = cv2.resize(frame, (224, 224))
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)
    
    def smooth_prediction(self, current_pred):
        """Smooth predictions using buffer"""
        self.prediction_buffer.append(current_pred)
        
        if len(self.prediction_buffer) < 3:
            return current_pred
        
        # Average recent predictions
        avg_pred = np.mean(list(self.prediction_buffer), axis=0)
        return avg_pred
    
    def draw_prediction_overlay(self, frame, breed, confidence):
        """Draw prediction overlay on frame"""
        height, width = frame.shape[:2]
        
        # Create overlay
        overlay = frame.copy()
        
        # Draw semi-transparent rectangle
        cv2.rectangle(overlay, (10, 10), (400, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Add text
        cv2.putText(frame, f"Breed: {breed.replace('_', ' ')}", 
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Confidence: {confidence:.1%}", 
                   (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Confidence bar
        bar_width = int(300 * confidence)
        cv2.rectangle(frame, (20, 85), (320, 100), (50, 50, 50), -1)
        cv2.rectangle(frame, (20, 85), (20 + bar_width, 100), (0, 255, 0), -1)
        
        return frame
    
    def run_webcam(self, camera_id=0):
        """Run real-time prediction on webcam"""
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Starting webcam... Press 'q' to quit, 's' to save frame")
        
        current_breed = "Detecting..."
        current_confidence = 0.0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            
            # Predict every few frames to improve performance
            if self.frame_count % self.prediction_interval == 0:
                try:
                    processed_frame = self.preprocess_frame(frame)
                    predictions = self.model.predict(processed_frame, verbose=0)
                    
                    # Smooth predictions
                    smoothed_pred = self.smooth_prediction(predictions[0])
                    
                    pred_class = np.argmax(smoothed_pred)
                    confidence = np.max(smoothed_pred)
                    
                    if confidence > self.confidence_threshold:
                        current_breed = self.breeds[pred_class]
                        current_confidence = confidence
                    else:
                        current_breed = "Low Confidence"
                        current_confidence = confidence
                
                except Exception as e:
                    print(f"Prediction error: {e}")
            
            # Draw overlay
            frame = self.draw_prediction_overlay(frame, current_breed, current_confidence)
            
            # Add instructions
            cv2.putText(frame, "Press 'q' to quit, 's' to save", 
                       (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 255, 255), 1)
            
            cv2.imshow('Cattle Breed Recognition', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save current frame
                timestamp = int(time.time())
                filename = f"capture_{current_breed}_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()
    
    def process_video_file(self, video_path, output_path=None):
        """Process video file and add predictions"""
        cap = cv2.VideoCapture(video_path)
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        current_breed = "Processing..."
        current_confidence = 0.0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Predict every few frames
            if frame_count % self.prediction_interval == 0:
                try:
                    processed_frame = self.preprocess_frame(frame)
                    predictions = self.model.predict(processed_frame, verbose=0)
                    
                    pred_class = np.argmax(predictions[0])
                    confidence = np.max(predictions[0])
                    
                    if confidence > self.confidence_threshold:
                        current_breed = self.breeds[pred_class]
                        current_confidence = confidence
                
                except Exception as e:
                    print(f"Frame {frame_count} error: {e}")
            
            # Add overlay
            frame = self.draw_prediction_overlay(frame, current_breed, current_confidence)
            
            if output_path:
                out.write(frame)
            else:
                cv2.imshow('Video Processing', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        cap.release()
        if output_path:
            out.release()
            print(f"Processed video saved: {output_path}")
        else:
            cv2.destroyAllWindows()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='cattle_breed_model.h5')
    parser.add_argument('--webcam', action='store_true', help='Use webcam')
    parser.add_argument('--video', help='Process video file')
    parser.add_argument('--output', help='Output video path')
    parser.add_argument('--camera', type=int, default=0, help='Camera ID')
    
    args = parser.parse_args()
    
    predictor = RealTimePredictor(args.model)
    
    if args.webcam:
        predictor.run_webcam(args.camera)
    elif args.video:
        predictor.process_video_file(args.video, args.output)
    else:
        print("Use --webcam for live camera or --video for file processing")

if __name__ == "__main__":
    main()