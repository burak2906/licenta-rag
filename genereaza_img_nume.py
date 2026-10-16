import os
import json

folder = "indicatoare_img"
mapare = {}

for filename in os.listdir(folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        nume = os.path.splitext(filename)[0]  # fără extensie
        nume_curat = nume.replace("_", " ").capitalize()
        mapare[filename] = f"Indicator {nume_curat}"

with open("img_to_nume.json", "w", encoding="utf-8") as f:
    json.dump(mapare, f, ensure_ascii=False, indent=2)

print("Mapare generată pentru", len(mapare), "imagini.")