"""
Automated Dataset Collection for Indian Cattle Breeds
Downloads images from Google Images using bing-image-downloader
"""
from bing_image_downloader import downloader
import os

# 20 Indian cattle and buffalo breeds
BREEDS = [
    "Gir cattle India",
    "Sahiwal cattle India", 
    "Red Sindhi cattle India",
    "Tharparkar cattle India",
    "Ongole cattle India",
    "Hariana cattle India",
    "Kankrej cattle India",
    "Rathi cattle India",
    "Murrah buffalo India",
    "Mehsana buffalo India",
    "Kangayam cattle India",
    "Hallikar cattle India",
    "Amritmahal cattle India",
    "Khillari cattle India",
    "Deoni cattle India",
    "Dangi cattle India",
    "Nagori cattle India",
    "Punganur cattle India",
    "Surti buffalo India",
    "Jaffarabadi buffalo India"
]

def download_dataset(images_per_breed=100):
    """Download images for all breeds"""
    print("="*60)
    print("CATTLE BREED DATASET COLLECTION")
    print("="*60)
    
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, breed in enumerate(BREEDS, 1):
        print(f"\n[{i}/{len(BREEDS)}] Downloading {breed}...")
        
        breed_name = breed.split()[0]  # Get first word as folder name
        
        try:
            downloader.download(
                breed,
                limit=images_per_breed,
                output_dir=output_dir,
                adult_filter_off=True,
                force_replace=False,
                timeout=15
            )
            print(f"✓ Downloaded {breed_name}")
        except Exception as e:
            print(f"✗ Error downloading {breed_name}: {e}")
    
    print("\n" + "="*60)
    print("DATASET COLLECTION COMPLETE!")
    print("="*60)
    print(f"\nDataset location: {output_dir}/")
    print(f"Total breeds: {len(BREEDS)}")
    print(f"Images per breed: ~{images_per_breed}")
    print(f"\nNext step: python train_cnn.py")

if __name__ == "__main__":
    # Download 100 images per breed (adjust as needed)
    download_dataset(images_per_breed=100)
