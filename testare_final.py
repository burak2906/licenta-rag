import json
import ollama
import base64
import random
import os
import unicodedata
import re
import chromadb
import traceback
from chromadb import PersistentClient as PersistentClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer, CrossEncoder

from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from chromadb import PersistentClient
from chromadb.config import Settings

from pymongo.mongo_client import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")

if not uri:
    raise ValueError("Lipsește variabila de mediu MONGO_URI în fișierul .env!")

# Create a new client and connect to the server
client_mongo = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client_mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"An error occurred: {e}")
db = client_mongo["drpciv"]
intrebari = list(db["questions"].find({}))
# ia intrebarile toate intrebările din baza de date
selectate = intrebari[:12]
print(f"Întrebări încărcate: {len(intrebari)}")

chroma_client = PersistentClient(settings=Settings(persist_directory="chroma_rag"))
text_collection = chroma_client.get_or_create_collection("cod_rutier")
definitii_collection = chroma_client.get_or_create_collection("definitii_indicatoare")

from ultralytics import YOLO
model_yolo = YOLO("runs/detect/train7/weights/best.pt")

def extrage_context_din_imagine(image_path):
    if not os.path.exists(image_path):
        return None, None

    results = model_yolo(image_path, conf=0.3)
    boxe = results[0].boxes

    contexte = []
    detectate = set()

    for box in boxe:
        cls_id = int(box.cls[0])
        nume_semn = model_yolo.names[cls_id]

        # evita duplicate
        if nume_semn in detectate:
            continue
        detectate.add(nume_semn)

        # adauga "indicator " inceput daca nu exista
        if not nume_semn.startswith("Indicator "):
            nume_semn = "Indicator " + nume_semn
        # cauta în definitii
        definitii = definitii_collection.get(where={"articol": nume_semn})
        if not definitii or not definitii["documents"]:
            continue
        if definitii["documents"]:
            context = definitii["documents"][0]
            contexte.append(f"{context}")

    if contexte:
        return "\n---\n".join(contexte), "context_yolo"
    else:
        return None, None

print("Total articole text:", text_collection.count())

embedder = SentenceTransformer("all-MiniLM-L6-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Tokenul JWT de autentificare
auth_token = os.getenv("AUTH_TOKEN")
if not auth_token:
    raise ValueError("Lipsește AUTH_TOKEN din fișierul .env!")
# Creeaza clientul Ollama autenticat
client = ollama.Client(
    host='https://chat.readerbench.com/ollama',
    headers={"Authorization": f"Bearer {auth_token}"}
)

# incarca intrebarile
# with open('intrebari.json', 'r', encoding='utf-8') as f:
#     intrebari = json.load(f)

# selectate = intrebari[:12] # selectam intrebari pentru testare

# incarcare imagine în base64
def image_to_base64(cale):
    if cale and os.path.exists(cale):
        with open(cale, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# RAG - similaritate semantica - chromadb

def cauta_context_crossencode(text_intrebare, prag=0.2, max_articole=200):
    emb = embedder.encode([text_intrebare])[0].tolist()
    rezultate = text_collection.query(
        query_embeddings=[emb],
        n_results=max_articole,
        include=["documents"]
    )
    docs = rezultate["documents"][0]
    if not docs:
        return "", "fara_rezultate"

    pairs = [[text_intrebare, doc] for doc in docs]
    scores = cross_encoder.predict(pairs)

    doc_score_pairs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    # pastreaza doar scoruri peste 2.5
    doc_score_pairs = [(doc, score) for doc, score in doc_score_pairs if score > 2.5]
    articole_selectate = [doc for doc, score in doc_score_pairs if score > prag]
    # primele 10 articole
    articole_selectate = articole_selectate[:10]
    print("Articole selectate (cross-encode):")
    for doc, score in doc_score_pairs[:20]:
        print(f"Scor: {score:.4f} - Articol: {doc[:100]}...")
    if articole_selectate:
        return "\n---\n".join(articole_selectate), "crossencode_prag"
    else:
        # daca best score e mai mic decat pragul de 2 nu returneaza nimic
        best_score = doc_score_pairs[0][1] if doc_score_pairs else 0
        if best_score < 2.0:
            print(f"Best score ({best_score:.4f}) is below threshold (2.0), returning empty context.")
            return "", "empty_context"
        return "\n---\n".join(doc for doc, _ in doc_score_pairs[:3]), "crossencode_fallback"

def trimite_prompt(prompt, imagine_b64=None, model="llava:34b"):
    try:
        params = {
            "model": model,
            "prompt": prompt,
            "options": {
                "temperature": 0.0,
                "top_p": 0.9,
                "num_predict": 128
            },
            "stream": False
        }

        if imagine_b64:
            params["images"] = [imagine_b64]

        response = client.generate(**params)
        litere = [l for l in response.response.strip() if l in ["A", "B", "C"]]
        litere = sorted(set(litere))
        return litere

    except Exception as e:
        print("Eroare Ollama:", e)
        traceback.print_exc()
        return "Eroare la trimiterea promptului"

rezultate = []
model = "llava:34b"
#model = "gemma3:27b"

import random

for intrebare in selectate:
    optiuni = intrebare['options']

    # Facem listă de perechi (literă, text)
    optiuni_list = list(optiuni.items())

    # Amestecăm ordinea
    random.shuffle(optiuni_list)

    # Refacem mapping-ul cu litere noi (A, B, C)
    litere = ["A", "B", "C"]
    optiuni_random = {litere[i]: text for i, (_, text) in enumerate(optiuni_list)}

    # Corect answer mereu listă
    raspuns_corect_initial = intrebare['correct_answer']
    if not isinstance(raspuns_corect_initial, list):
        raspuns_corect_initial = [raspuns_corect_initial]

    # Găsim textele răspunsurilor corecte inițiale
    texte_corecte = [optiuni[r] for r in raspuns_corect_initial]

    # Căutăm în noile opțiuni unde au ajuns textele corecte
    raspuns_corect_nou = [k for k, v in optiuni_random.items() if v in texte_corecte]

    # Debug
    print("Opțiuni randomizate:", optiuni_random)
    print("Răspuns corect acum:", raspuns_corect_nou)

    # Actualizăm întrebarea cu noile opțiuni și noile răspunsuri corecte
    intrebare['options'] = optiuni_random
    intrebare['correct_answer'] = raspuns_corect_nou

    optiuni_formatate = ''.join([f"{k}. {v}\n" for k, v in intrebare['options'].items()])
    imagine_b64 = image_to_base64(intrebare.get("image_local_path"))

    intrebare_optiuni = f"{intrebare['text']}\n{optiuni_formatate}"
    print(f"Întrebare: {intrebare_optiuni}")
    context, tip_context = cauta_context_crossencode(intrebare['text'], prag=5.0, max_articole=200)

    if intrebare.get("image_local_path"):
        context_img, tip_ctx_img = extrage_context_din_imagine(intrebare["image_local_path"])
        if context_img:
            context += f"\n---\nContext vizual extras (YOLOv8):\n{context_img}"
            tip_context += f"+{tip_ctx_img}"

    prompt_fara = f"""
        Întrebare: {intrebare['text']}
        Opțiuni: {optiuni_formatate}

        Instrucțiuni:
        Răspunde DOAR cu literele mari corespunzătoare opțiunilor corecte, fără explicații.
        Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele.
        Formatul răspunsului trebuie să fie exact: ["A"], ["B"], ["C"], ["A", "B"], ["A", "C"], ["B", "C"], ["A", "B", "C"].
    """.strip()
    prompt_cu = f"""
        Întrebare: {intrebare['text']}
        Opțiuni: {optiuni_formatate}
        Context util extras automat din Codul Rutier: {context}

        Instrucțiuni:
        Bazându-te pe contextul de mai sus, răspunde DOAR cu literele opțiunilor corecte, în ordine alfabetică. 
        Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele.
        Formatul răspunsului trebuie să fie exact: ["A"], ["B"], ["C"], ["A", "B"], ["A", "C"], ["B", "C"], ["A", "B", "C"].
        """.strip()
    rasp_fara = trimite_prompt(prompt_fara, imagine_b64, model=model)
    rasp_cu = trimite_prompt(prompt_cu, imagine_b64, model=model)

    rezultate.append({
        # "id": intrebare["_id"],
        "id": str(intrebare["_id"]),
        "text": intrebare["text"],
        "optiuni": intrebare["options"],
        "cale_imagine": intrebare.get("image_local_path"),
        "raspuns_fara_context": rasp_fara,
        "raspuns_cu_context": rasp_cu,
        "raspuns_corect": intrebare["correct_answer"],
        "paragrafe_context": context,
        "tip_context": tip_context
    })

# salvam rezultatul in baza de date MongoDB si actualizam intrebarile cu rezultatele generate

# for rezultat in rezultate:
#     db["questions"].update_one(
#         {"_id": rezultat["id"]},
#         {"$set": {
#             f"rezultate_model.{model}": {
#                 "raspuns_fara_context": rezultat["raspuns_fara_context"],
#                 "raspuns_cu_context": rezultat["raspuns_cu_context"],
#                 "tip_context": rezultat["tip_context"],
#                 "paragrafe_context": rezultat["paragrafe_context"]
#             }
#         }}
#     )
# with open("demo_raspunsuri.json", "w", encoding="utf-8") as f:
#     json.dump(rezultate, f, ensure_ascii=False, indent=2)

with open(f"demo_raspunsuri_llava.json", "w", encoding="utf-8") as f:
    json.dump(rezultate, f, ensure_ascii=False, indent=2)
