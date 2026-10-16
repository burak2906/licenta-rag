from pathlib import Path
import shutil
import random

# Căile pentru train și val
train_images_dir = Path("dataset/images/train")
train_labels_dir = Path("dataset/labels/train")
val_images_dir = Path("dataset/images/val")
val_labels_dir = Path("dataset/labels/val")

# Creează directoarele val/ dacă nu există
val_images_dir.mkdir(parents=True, exist_ok=True)
val_labels_dir.mkdir(parents=True, exist_ok=True)

# Selectează 10% din imaginile din train
image_paths = list(train_images_dir.glob("*.*"))
sample_size = max(1, int(0.10 * len(image_paths)))
val_samples = random.sample(image_paths, sample_size)

# Mută imaginile și etichetele corespunzătoare în val/
for img_path in val_samples:
    label_path = train_labels_dir / (img_path.stem + ".txt")
    
    if label_path.exists():
        shutil.move(str(img_path), val_images_dir / img_path.name)
        shutil.move(str(label_path), val_labels_dir / label_path.name)

print(f"Mutate {sample_size} imagini în val/")