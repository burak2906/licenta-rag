from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict

# Setup conexiune MongoDB
import os
from dotenv import load_dotenv

load_dotenv()

# Setup conexiune MongoDB
uri = os.getenv("MONGO_URI")
if not uri:
    raise ValueError("Lipsește MONGO_URI din fișierul .env!")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["drpciv"]
collection = db["questions"]

# Dict pentru fiecare model: tp, fp, fn, fara, total
statistici_text = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0, "fara": 0, "total": 0, "corect_gresit": 0, "corect_corect": 0, "gresit_gresit": 0, "gresit_corect": 0})
statistici_vizual = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0, "fara": 0, "total": 0, "corect_gresit": 0, "corect_corect": 0, "gresit_gresit": 0, "gresit_corect": 0})
cursor = collection.find({"rezultate_model": {"$exists": True}})
for doc in cursor:
    corect = doc.get("correct_answer", [])
    rezultate = doc.get("rezultate_model", {})
    has_image = bool(doc.get("image_local_path"))

    for model, r in rezultate.items():
        rasp_cu = r.get("raspuns_cu_context", [])
        rasp_fara = r.get("raspuns_fara_context", [])

        # alegem tipul de statistici in functie de existenta imaginii
        stats = statistici_vizual if has_image else statistici_text
        stats[model]["total"] += 1

        if rasp_cu == corect:
            stats[model]["tp"] += 1
        else:
            stats[model]["fp"] += 1

        if rasp_fara == corect:
            stats[model]["fara"] += 1

        if rasp_fara == corect and rasp_cu != corect:
            stats[model]["fn"] += 1
        
        if rasp_fara == corect and rasp_cu == corect:
            stats[model]["corect_corect"] += 1
        elif rasp_fara != corect and rasp_cu == corect:
            stats[model]["gresit_corect"] += 1
        elif rasp_fara != corect and rasp_cu != corect:
            stats[model]["gresit_gresit"] += 1
        elif rasp_fara == corect and rasp_cu != corect:
            stats[model]["corect_gresit"] += 1

# afisare metrici pentru fiecare model
def afiseaza_metrici(nume, statistici):
    for model, stats in statistici.items():
        tp, fp, fn, fara, total = stats["tp"], stats["fp"], stats["fn"], stats["fara"], stats["total"]
        accuracy_context = tp / (tp + fp) if tp + fp > 0 else 0
        accuracy_fara_context = fara / total if total > 0 else 0
        rata_stricate_de_context = stats["corect_gresit"] / total if total > 0 else 0
        rata_corectate_cu_context = stats["gresit_corect"] / total if total > 0 else 0
        rata_succes_context = tp / (tp + fn) if tp + fn > 0 else 0
        print(f"\n[{nume}] Rezultate pentru modelul: {model}")
        print(f"Total întrebări: {total}")
        print(f"Corecte fără context (FA): {fara}")
        print(f"Corecte cu context (TP): {tp}")
        print(f"Greșite cu context (FP): {fp}")
        print(f"Contextul a stricat (FN): {fn}")
        print(f"Accuracy (cu context): {accuracy_context:.2f}")
        print(f"Accuracy (fără context): {accuracy_fara_context:.2f}")
        print(f"Contextul a stricat: {rata_stricate_de_context:.2f}")
        print(f"Corectate cu context: {rata_corectate_cu_context:.2f}")
        print(f"Rata succesului cu context: {rata_succes_context:.2f}")

        print(f"Corect fără context și corect cu context: {stats['corect_corect']}")
        print(f"Greșit fără context și corect cu context: {stats['gresit_corect']}")
        print(f"Greșit fără context și greșit fără context: {stats['gresit_gresit']}")
        print(f"Corect fără context și greșit cu context: {stats['corect_gresit']}")

afiseaza_metrici("Fără imagine (doar text)", statistici_text)
afiseaza_metrici("Cu imagine (vizual + text)", statistici_vizual)