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

# Inițializează CLIP și Chroma doar o dată
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
chroma_client = PersistentClient(settings=Settings(persist_directory="chroma_rag"))
text_collection = chroma_client.get_or_create_collection("cod_rutier")
definitii_collection = chroma_client.get_or_create_collection("definitii_indicatoare")
vizual_collection = chroma_client.get_or_create_collection("indicatoare_vizuale")

from ultralytics import YOLO
model_yolo = YOLO("runs/detect/train7/weights/best.pt")  # sau calea ta

def extrage_context_din_imagine(image_path):
    if not os.path.exists(image_path):
        return None, None

    image = Image.open(image_path).convert("RGB")
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        image_emb = clip_model.get_image_features(**inputs).squeeze().tolist()

    rezultate = vizual_collection.query(
        query_embeddings=[image_emb],
        n_results=1,
        include=["metadatas"]
    )

    if not rezultate["metadatas"][0]:
        return None, None

    nume_indicator = rezultate["metadatas"][0][0]["Indicator"]

    # Căutăm doar în colecția cu definiții
    context_art = definitii_collection.get(where={"articol": nume_indicator})
    if context_art["documents"]:
        return context_art["documents"][0], "context_vizual"
    return None, None

# def extrage_context_din_imagine(image_path):
#     if not os.path.exists(image_path):
#         return None, None

#     results = model_yolo(image_path, conf=0.3)
#     boxe = results[0].boxes

#     contexte = []
#     detectate = set()

#     for box in boxe:
#         cls_id = int(box.cls[0])
#         nume_semn = model_yolo.names[cls_id]

#         # evită duplicate
#         if nume_semn in detectate:
#             continue
#         detectate.add(nume_semn)

#         # adauga "indicator " la început dacă nu există
#         if not nume_semn.startswith("Indicator "):
#             nume_semn = "Indicator " + nume_semn
#         # caută în definitii
#         definitii = definitii_collection.get(where={"articol": nume_semn})
#         if not definitii or not definitii["documents"]:
#             continue
#         if definitii["documents"]:
#             context = definitii["documents"][0]
#             contexte.append(f"{context}")

#     if contexte:
#         return "\n---\n".join(contexte), "context_yolo"
#     else:
#         return None, None

print("Total articole text:", text_collection.count())
# print("Total indicatoare vizuale:", vizual_collection.count())

# Încarcă modelul de embedding
#print("Model loading...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
#embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
#print("Model loaded.")

# Tokenul JWT de autentificare
auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjkyOTM5MmU5LTllZjMtNGMxZC1iNTg5LWQ3OTgwNjU0NjdlZiJ9.XwsBRTTMf8TCA3D6SebmGdphvBYtYIFmc65nW1exJF0'
# Creează clientul Ollama autenticat
client = ollama.Client(
    host='https://chat.readerbench.com/ollama',
    headers={"Authorization": f"Bearer {auth_token}"}
)

# Încarcă întrebările
with open('intrebari.json', 'r', encoding='utf-8') as f:
    intrebari = json.load(f)

# selecteaza intrebarea cu id 67f0dc3c2be5222d1c2e10af
# intrebari = [i for i in intrebari if i["_id"] == "67f0dc3c2be5222d1c2e0e95"]
# batch_num = 1  # ← modifică între 1, 2, 3...
# batch_size = 100
# start = (batch_num - 1) * batch_size
# end = start + batch_size
# # daca nu exista intrebari pana la end, le ia pe toate
# if end > len(intrebari):
#     end = len(intrebari)
# intrebari = intrebari[start:end]
selectate = intrebari[1200:] # selectăm primele 100 de întrebări pentru testare

# Încărcare imagine în base64
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

# 10 intrebari cu context cross-encode
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
    # printeaza articolele cu cele mai mari 20 de scoruri si scorurile lor
    print("Articole selectate (cross-encode):")
    for doc, score in doc_score_pairs[:20]:
        print(f"Scor: {score:.4f} - Articol: {doc[:100]}...")
    articol_test = "Catalizatorul auto este o componentă esențială a sistemului de evacuare, cu rolul de a reduce poluarea prin transformarea gazelor toxice din arderea combustibilului în substanțe mai puțin nocive. Funcționează pe baza unei reacții chimice activate la temperaturi înalte, folosind o structură de tip fagure impregnate cu metale prețioase (platină, rodiu, paladiu). Eficiența catalizatorului poate atinge aproape 100%, scăzând gradual cu uzura, dar menținând un rol crucial în respectarea standardelor de emisii."
    scor_test = cross_encoder.predict([(text_intrebare, articol_test)])[0]
    print(f"Scor forțat pentru articol testat manual: {scor_test:.4f}")

    if articole_selectate:
        return "\n---\n".join(articole_selectate), "crossencode_prag"
    else:
        # daca best score e mai mic decat pragul de 1 nu returneaza nimic
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
# model ="mistral-small3.1:latest"
#model = "gemma3:27b"

for intrebare in selectate:
    #print(f"Procesăm întrebare: {intrebare['text']}")
    optiuni_formatate = ''.join([f"{k}. {v}\n" for k, v in intrebare['options'].items()])
    imagine_b64 = image_to_base64(intrebare.get("image_local_path"))
    #context, tip_context = cauta_context_optimal(intrebare['text'], prag=0.75, max_articole=2)
    #concatenare intrebare + optiuni
    intrebare_optiuni = f"{intrebare['text']}\n{optiuni_formatate}"
    print(f"Întrebare: {intrebare_optiuni}")
    context, tip_context = cauta_context_crossencode(intrebare['text'], prag=5.0, max_articole=200)
    #context, tip_context = cauta_context_crossencode_avansat(intrebare['text'], prag_score=0.6, prag_distanta=0.8, max_articole=5)
    #context = cauta_articole_relevante_rag(intrebare['text'])
    #context = cauta_articole_relevante_rag_prag(intrebare['text'], prag=0.65)
    # print(f"Întrebare: {intrebare['text']}")
    # print(f"Opțiuni: {optiuni_formatate}")
    # print(f"Context: {context}")
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
    #print("Trimit prompt fără context...")
    rasp_fara = trimite_prompt(prompt_fara, imagine_b64, model=model)
    rasp_cu = trimite_prompt(prompt_cu, imagine_b64, model=model)

    rezultate.append({
        "id": intrebare["_id"],
        "text": intrebare["text"],
        "optiuni": intrebare["options"],
        "cale_imagine": intrebare.get("image_local_path"),
        "raspuns_fara_context": rasp_fara,
        "raspuns_cu_context": rasp_cu,
        "raspuns_corect": intrebare["correct_answer"],
        "paragrafe_context": context,
        "tip_context": tip_context
    })

# Salvăm rezultatul
# with open("raspunsuri_generate.json", "w", encoding="utf-8") as f:
#     json.dump(rezultate, f, ensure_ascii=False, indent=2)

with open(f"raspunsuri_batch_llava_13.json", "w", encoding="utf-8") as f:
    json.dump(rezultate, f, ensure_ascii=False, indent=2)

# verifica din jsonuri cate raspunsuri sunt corecte
with open(f"raspunsuri_batch_llava_13.json", "r", encoding="utf-8") as f:
    raspunsuri = json.load(f)
tp = fp = fn = total = 0
fa = 0
for r in raspunsuri:
    cu = r["raspuns_cu_context"]
    corect = r["raspuns_corect"]
    fara = r["raspuns_fara_context"]

    total += 1

    if cu == corect:
        tp += 1
    elif cu != corect:
        fp += 1
    if fara == corect:
        fa += 1
    if fara == corect and cu != corect:
        fn += 1  # a fost corect fără context, dar l-a stricat contextul
# Metrici
precision = tp / (tp + fp) if tp + fp > 0 else 0
recall = tp / (tp + fn) if tp + fn > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
# Afișare rezultate
print(f"\n📊 Număr total întrebări: {total}")
print(f"✔️ Corecte cu context (TP): {tp}")
print(f"❌ Greșite cu context (FP): {fp}")
print(f"📉 Contextul a stricat (FN): {fn}")
print(f"✅ Corecte fără context (FA): {fa}")

print(f"\nPrecision (cu context): {precision:.2f}")
print(f"Recall (cu context): {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"Total articole text: {text_collection.count()}")
print(f"Total definitii articole vizuale: {definitii_collection.count()}")
