import argparse
import numpy as np
from pathlib import Path
from model import CattleBreedModel
from data_loader import DataLoader
from breeds_info import get_breed_info
import matplotlib.pyplot as plt
from PIL import Image

def predict_image(model_path, image_path, top_k=3):
    model = CattleBreedModel()
    model.load(model_path)
    loader = DataLoader()
    img_array = loader.load_and_preprocess_image(image_path)
    predictions = model.predict(img_array)
    
    class_names = ['Gir', 'Hariana', 'Kankrej', 'Mehsana_Buffalo', 'Murrah_Buffalo',
                   'Ongole', 'Rathi', 'Red_Sindhi', 'Sahiwal', 'Tharparkar']
    
    top_indices = np.argsort(predictions)[-top_k:][::-1]
    results = []
    for idx in top_indices:
        breed_name = class_names[idx]
        confidence = predictions[idx] * 100
        breed_info = get_breed_info(breed_name)
        results.append({'breed': breed_name, 'confidence': confidence, 'info': breed_info})
    return results, img_array

def display_results(image_path, results):
    img = Image.open(image_path)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.imshow(img)
    ax1.axis('off')
    ax1.set_title('Input Image', fontsize=14, fontweight='bold')
    
    breeds = [r['breed'] for r in results]
    confidences = [r['confidence'] for r in results]
    colors = ['#2ecc71' if i == 0 else '#3498db' for i in range(len(breeds))]
    
    bars = ax2.barh(breeds, confidences, color=colors)
    ax2.set_xlabel('Confidence (%)')
    ax2.set_title('Predictions')
    ax2.set_xlim(0, 100)
    
    for bar, conf in zip(bars, confidences):
        ax2.text(conf + 2, bar.get_y() + bar.get_height()/2, f'{conf:.1f}%', va='center')
    
    plt.tight_layout()
    plt.savefig('prediction_result.png', dpi=150)
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--model', type=str, default='cattle_model.h5')
    parser.add_argument('--top-k', type=int, default=3)
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()
    
    if not Path(args.model).exists():
        print(f"Model not found: {args.model}")
        return
    if not Path(args.image).exists():
        print(f"Image not found: {args.image}")
        return
    
    print("="*60)
    print("CATTLE BREED RECOGNITION - PREDICTION")
    print("="*60)
    
    results, _ = predict_image(args.model, args.image, args.top_k)
    
    print("\nRESULTS:")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['breed']} - {r['confidence']:.2f}%")
        if r['info']:
            print(f"   Origin: {r['info'].get('origin')}")
            print(f"   Type: {r['info'].get('type')}")
    
    if args.show:
        display_results(args.image, results)

if __name__ == "__main__":
    main()
