import json
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.config import Settings
from collections import defaultdict

from uuid import uuid4
import re

with open("articole_cod_rutier.json", "r", encoding="utf-8") as f:
    articole = json.load(f)

# initializare ChromaDB
settings = Settings(
    persist_directory="chroma_rag",
    anonymized_telemetry=False
)
chroma_client = PersistentClient(settings=settings)
if "cod_rutier" in [c.name for c in chroma_client.list_collections()]:
    chroma_client.delete_collection("cod_rutier")

# creare colectie
collection = chroma_client.get_or_create_collection(name="cod_rutier")

# Setup model embedding
model = SentenceTransformer("all-MiniLM-L6-v2")
#model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Construim liste pentru indexare
docs = []
ids = []
metadate = []

for i, (nume, info) in enumerate(articole.items()):
    text = info["continut"]
    docs.append(text)
    ids.append(nume)
    metadate.append({
        "articol": nume,
        "capitol": info["capitol"]
    })

# embedings
embeddings = model.encode(docs).tolist()

# adaugam in colectie
collection.add(documents=docs, metadatas=metadate, ids=ids, embeddings=embeddings)


print("Indexare finalizată. Total articole:", collection.count())
