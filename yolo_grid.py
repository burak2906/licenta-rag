import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2

image_dir = '/mnt/c/Users/Burak/Desktop/licenta/dataset/images/train'
output_path = '/mnt/c/Users/Burak/Desktop/licenta/sample_images_grid.png'
if not os.path.exists(image_dir):
    print("Folderul NU există!")
    exit()
else:
    print("Folderul există:", image_dir)

image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print("Imagini găsite:", len(image_files))

if not image_files:
    print("Nu s-au găsit imagini în folder.")
    exit()

selected_images = random.sample(image_files, min(9, len(image_files)))
print("Imagini selectate:", selected_images)

fig, axes = plt.subplots(3, 3, figsize=(10, 10))

for ax, img_name in zip(axes.flatten(), selected_images):
    img_path = os.path.join(image_dir, img_name)
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    ax.imshow(img)
    ax.axis('off')

for i in range(len(selected_images), 9):
    axes.flatten()[i].axis('off')

plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.close()

print("Grid salvat la:", output_path)