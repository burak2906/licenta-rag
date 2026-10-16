from ultralytics import YOLO
from chromadb import PersistentClient
from chromadb.config import Settings
import json
import os

# modelul YOLO antrenat
model_yolo = YOLO("runs/detect/train7/weights/best.pt")

# definitiile semnelor
with open("definitii_indicatoare.json", "r", encoding="utf-8") as f:
    definitii = json.load(f)

# conectare la chromadb
chroma_client = PersistentClient(settings=Settings(persist_directory="chroma_rag"))
definitii_collection = chroma_client.get_or_create_collection("definitii_indicatoare")

# imagini demo
imagini = [
    "/mnt/c/Users/Burak/Desktop/licenta/images/420.jpeg",
    "/mnt/c/Users/Burak/Desktop/licenta/images/621.jpeg",
    "/mnt/c/Users/Burak/Desktop/licenta/images/722.jpeg",
    "/mnt/c/Users/Burak/Desktop/licenta/images/870.jpeg",
    "/mnt/c/Users/Burak/Desktop/licenta/images/1092.jpeg"
]

for img in imagini:
    if not os.path.exists(img):
        print(f"Imaginea nu există: {img}")
        continue

    print(f"\nProcesăm imaginea: {img}")

    results = model_yolo(img, conf=0.3)
    boxe = results[0].boxes

    contexte = []
    detectate = set()

    for box in boxe:
        cls_id = int(box.cls[0])
        nume_semn = model_yolo.names[cls_id]

        # evită duplicate
        if nume_semn in detectate:
            continue
        detectate.add(nume_semn)

        # adauga "indicator " la început dacă nu există
        if not nume_semn.startswith("Indicator "):
            nume_semn = "Indicator " + nume_semn
        # caută în definitii
        definitii = definitii_collection.get(where={"articol": nume_semn})
        if not definitii or not definitii["documents"]:
            continue
        if definitii["documents"]:
            context = definitii["documents"][0]
            contexte.append(f"{context}")
        else:
            contexte.append(f"Definiție lipsă pentru {nume_semn}")

    if contexte:
        print(f"Semne detectate în {img}:")
        for context in contexte:
            print(f"- {context}")
    else:
        print(f"Niciun semn cunoscut detectat în {img}.")

print("\nScript terminat.")
