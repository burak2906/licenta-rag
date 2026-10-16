import json
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.config import Settings

model = SentenceTransformer("all-MiniLM-L6-v2")
from numpy import dot
from numpy.linalg import norm

intrebare = "Care este rolul catalizatorului? A. de a asigura depoluarea atmosferică, prin arderea completă a gazelor de evacuare B. de a facilita arderea amestecului carburant in cilindrii motorului C. de a filtra carburantul înainte de pulverizarea acestuia în cilindri"
embedding_intrebare = model.encode(intrebare)
embedding_articol = model.encode("Catalizatorul auto este o componentă esențială a sistemului de evacuare, cu rolul de a reduce poluarea prin transformarea gazelor toxice din arderea combustibilului în substanțe mai puțin nocive. Funcționează pe baza unei reacții chimice activate la temperaturi înalte, folosind o structură de tip fagure impregnate cu metale prețioase (platină, rodiu, paladiu). Eficiența catalizatorului poate atinge aproape 100%, scăzând gradual cu uzura, dar menținând un rol crucial în respectarea standardelor de emisii.")

sim = dot(embedding_intrebare, embedding_articol) / (norm(embedding_intrebare) * norm(embedding_articol))
print(f"Cosine similarity: {sim:.4f}")
# Inițializare ChromaDB
settings = Settings(
    persist_directory="chroma_rag",
    anonymized_telemetry=False
)
chroma_client = PersistentClient(settings=settings)
# Șterge colecțiile existente
for name in ["cod_rutier", "definitii_indicatoare"]:
    if name in [c.name for c in chroma_client.list_collections()]:
        chroma_client.delete_collection(name)

# Funcție generală de indexare
def indexeaza(json_path, collection_name):
    with open(json_path, "r", encoding="utf-8") as f:
        articole = json.load(f)

    collection = chroma_client.get_or_create_collection(name=collection_name)
    docs = [a["continut"] for a in articole]
    ids = [f"{collection_name}_{i}" for i in range(len(articole))]  # IDs unice
    metadate = [{"articol": a["articol"]} for a in articole]
    embeddings = model.encode(docs).tolist()

    collection.add(documents=docs, metadatas=metadate, ids=ids, embeddings=embeddings)
    print(f"Indexat {len(docs)} în colecția {collection_name}.")


# Indexează ambele colecții
indexeaza("articole.json", "cod_rutier")
indexeaza("definitii_indicatoare.json", "definitii_indicatoare")
