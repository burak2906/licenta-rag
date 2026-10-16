# vreau sa numar cate intrebari sunt cu imagine si cate fara in intrebari.json


import json

with open("intrebari.json", "r", encoding="utf-8") as f:
    questions = json.load(f)
    with_image = sum(1 for q in questions if q.get("image_local_path"))
    without_image = len(questions) - with_image
    print(f"Număr întrebări cu imagine: {with_image}")
    print(f"Număr întrebări fără imagine: {without_image}")

# numara articole din articol.json
with open("articole.json", "r", encoding="utf-8") as f:
    articole = json.load(f)
    docs = [a["continut"] for a in articole]
    print(f"Număr articole: {len(docs)}")

# numara articole din definitii_indicatoare.json
with open("definitii_indicatoare.json", "r", encoding="utf-8") as f:
    definitii = json.load(f)
    docs = [a["continut"] for a in definitii]
    print(f"Număr definiții indicatoare: {len(docs)}")
