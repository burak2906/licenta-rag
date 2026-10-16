import albumentations as A
import cv2
import shutil
from pathlib import Path

# Setări directoare
input_img_dir = Path("dataset/images/train")
input_lbl_dir = Path("dataset/labels/train")
output_img_dir = Path("augmented/images/train")
output_lbl_dir = Path("augmented/labels/train")

# Creează directoarele de output
shutil.rmtree(output_img_dir, ignore_errors=True)
shutil.rmtree(output_lbl_dir, ignore_errors=True)
output_img_dir.mkdir(parents=True, exist_ok=True)
output_lbl_dir.mkdir(parents=True, exist_ok=True)

# Transformări de augmentare (10 variații)
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.Rotate(limit=15, p=0.7),
    A.MotionBlur(p=0.2),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=10, p=0.7)
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# Parcurgem imaginile
augmented_count = 0
for img_path in input_img_dir.glob("*.*"):
    stem = img_path.stem
    label_path = input_lbl_dir / f"{stem}.txt"
    if not label_path.exists():
        continue

    # Încarcă imaginea și eticheta
    img = cv2.imread(str(img_path))
    if img is None:
        continue
    h, w = img.shape[:2]

    with open(label_path, "r") as f:
        bboxes = []
        class_labels = []
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls, xc, yc, bw, bh = parts
            class_labels.append(int(cls))
            bboxes.append([float(xc), float(yc), float(bw), float(bh)])

    # 10 augmentări per imagine
    for i in range(10):
        transformed = transform(image=img, bboxes=bboxes, class_labels=class_labels)
        aug_img = transformed["image"]
        aug_boxes = transformed["bboxes"]
        aug_labels = transformed["class_labels"]

        out_img_path = output_img_dir / f"{stem}_aug{i}.jpg"
        cv2.imwrite(str(out_img_path), aug_img)

        out_txt_path = output_lbl_dir / f"{stem}_aug{i}.txt"
        with open(out_txt_path, "w") as f_out:
            for label, box in zip(aug_labels, aug_boxes):
                f_out.write(f"{int(label)} {' '.join([f'{x:.6f}' for x in box])}\n")


        augmented_count += 1

print(f"Augmentări generate: {augmented_count}")
