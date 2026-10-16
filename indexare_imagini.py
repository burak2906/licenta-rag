import os
import json
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
from chromadb import PersistentClient
from chromadb.config import Settings

# Setup CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Setup ChromaDB
settings = Settings(persist_directory="chroma_rag")
chroma_client = PersistentClient(settings=settings)
if "indicatoare_vizuale" in [c.name for c in chroma_client.list_collections()]:
    chroma_client.delete_collection("indicatoare_vizuale")

collection = chroma_client.get_or_create_collection(name="indicatoare_vizuale")

# Load mapping imagine → nume indicator
with open("img_to_nume.json", "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Encode + adaugă fiecare imagine în colecție
for filename, nume_indicator in mapping.items():
    path = os.path.join("indicatoare_img", filename)
    if not os.path.exists(path):
        print(f"Fișier lipsă: {filename}")
        continue

    image = Image.open(path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        image_emb = model.get_image_features(**inputs).squeeze().tolist()

    collection.add(
        documents=[nume_indicator],
        metadatas=[{"Indicator": nume_indicator}],
        ids=[filename],
        embeddings=[image_emb]
    )
    print(f"Indexat: {filename} → {nume_indicator}")

print("Indexare vizuală completă.")
