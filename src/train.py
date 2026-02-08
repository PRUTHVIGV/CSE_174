import argparse
from pathlib import Path
from model import CattleBreedModel
from data_loader import DataLoader
import matplotlib.pyplot as plt

def plot_history(history1, history2, save_path='training_history.png'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    acc = history1.history['accuracy'] + history2.history['accuracy']
    val_acc = history1.history['val_accuracy'] + history2.history['val_accuracy']
    loss = history1.history['loss'] + history2.history['loss']
    val_loss = history1.history['val_loss'] + history2.history['val_loss']
    epochs_range = range(len(acc))
    
    ax1.plot(epochs_range, acc, label='Training')
    ax1.plot(epochs_range, val_acc, label='Validation')
    ax1.set_title('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(epochs_range, loss, label='Training')
    ax2.plot(epochs_range, val_loss, label='Validation')
    ax2.set_title('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Training history saved to {save_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str, default='dataset')
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--fine-tune-epochs', type=int, default=10)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--img-size', type=int, default=224)
    parser.add_argument('--output', type=str, default='cattle_model.h5')
    args = parser.parse_args()
    
    print("="*60)
    print("CATTLE BREED RECOGNITION - TRAINING")
    print("="*60)
    
    data_path = Path(args.data_dir)
    if not data_path.exists():
        print(f"\nDataset not found. Creating structure...")
        DataLoader().create_sample_dataset_structure(args.data_dir)
        print("\nAdd images and run again!")
        return
    
    print("\n1. Loading dataset...")
    loader = DataLoader(img_size=args.img_size, batch_size=args.batch_size)
    train_ds, val_ds, class_names = loader.create_dataset(args.data_dir)
    print(f"   Found {len(class_names)} breeds")
    
    print("\n2. Building model...")
    model = CattleBreedModel(num_classes=len(class_names), img_size=args.img_size)
    model.build_model()
    
    print("\n3. Training...")
    history1, history2 = model.train(train_ds, val_ds, args.epochs, args.fine_tune_epochs)
    
    print("\n4. Evaluating...")
    loss, accuracy = model.model.evaluate(val_ds)
    print(f"   Accuracy: {accuracy*100:.2f}%")
    
    print("\n5. Saving...")
    model.save(args.output)
    plot_history(history1, history2)
    
    print("\n"+"="*60)
    print("TRAINING COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    main()
