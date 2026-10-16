import os
import requests
from bs4 import BeautifulSoup
import json
from bson import ObjectId


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

# Setup conexiune MongoDB
uri = os.getenv("MONGO_URI")
if not uri:
    raise ValueError("Lipsește MONGO_URI din fișierul .env!")

# creare client MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))

# confirmare conexiune
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"An error occurred: {e}")

# URL-ul paginilor cu intrebari

urls = [
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=4",
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=5",
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=6",
    "https://scoaladrpciv.ro/intrebari/categoria-b/indicatoare-si-marcaje?page=7",
    "https://scoaladrpciv.ro/intrebari/categoria-b/semnale-luminoase?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/semnale-luminoase?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/depasirea?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/depasirea?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/depasirea?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/reguli-referitoare-la-manevre?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/reguli-referitoare-la-manevre?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/trecerea-la-nivel-cu-calea-ferata?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/trecerea-la-nivel-cu-calea-ferata?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/circulatia-pe-autostrazi",
    "https://scoaladrpciv.ro/intrebari/categoria-b/sanctiuni-si-contraventii?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/sanctiuni-si-contraventii?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/sanctiuni-si-contraventii?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/sanctiuni-si-contraventii?page=4",
    "https://scoaladrpciv.ro/intrebari/categoria-b/conducerea-preventiva?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/conducerea-preventiva?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/conducerea-preventiva?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/conducerea-preventiva?page=4",
    "https://scoaladrpciv.ro/intrebari/categoria-b/conducerea-ecologica",
    "https://scoaladrpciv.ro/intrebari/categoria-b/semnalele-politistilor?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/semnalele-politistilor?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/pozitia-in-timpul-mersului-si-semnalele-conducatorilor-de-autovehicule?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/pozitia-in-timpul-mersului-si-semnalele-conducatorilor-de-autovehicule?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/pozitia-in-timpul-mersului-si-semnalele-conducatorilor-de-autovehicule?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/viteza-si-distanta-intre-vehicule?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/viteza-si-distanta-intre-vehicule?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/prioritate-de-trecere?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/prioritate-de-trecere?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/prioritate-de-trecere?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/prioritate-de-trecere?page=4",
    "https://scoaladrpciv.ro/intrebari/categoria-b/prioritate-de-trecere?page=5",
    "https://scoaladrpciv.ro/intrebari/categoria-b/oprirea-stationarea-si-parcarea?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/oprirea-stationarea-si-parcarea?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/oprirea-stationarea-si-parcarea?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/obligatiile-conducatorilor-de-autovehicule?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/obligatiile-conducatorilor-de-autovehicule?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/reguli-generale?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/reguli-generale?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/masuri-de-prim-ajutor?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/masuri-de-prim-ajutor?page=2",
    "https://scoaladrpciv.ro/intrebari/categoria-b/masuri-de-prim-ajutor?page=3",
    "https://scoaladrpciv.ro/intrebari/categoria-b/notiuni-de-mecanica?page=1",
    "https://scoaladrpciv.ro/intrebari/categoria-b/notiuni-de-mecanica?page=2",
]

# simulam un browser pt a evita restrictii anti-scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

questions_data = []
questions = []


for url in urls:
    # request catre pagina
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    questions += soup.find_all("div", class_="card-body")


for question in questions:
    text = question.find("h2").text.strip() if question.find("h2") else "No question text"
    # vreau sa scot din fiecare raspuns primele 4 caractere
    first_option = question.find_all("li")[0].text.strip()
    second_option = question.find_all("li")[1].text.strip()
    third_option = question.find_all("li")[2].text.strip()
    first_option = first_option[4:]
    second_option = second_option[4:]
    third_option = third_option[4:]
    options = {
        "A": first_option,
        "B": second_option,
        "C": third_option
    }


    # poate sa fie unul sau mai multe raspunsuri corecte sunt cele cu clasa __q_correct
    correct_answer = []
    # in __q_answers sunt toate raspunsurile cele din __q_correct sunt cele corecte si cele din __q_incorect sunt cele gresite, vreau sa salvez cheia raspunsului in loc de valoare
    for answer in question.find_all("li"):
        if answer["class"][0] == "__q_correct":
            correct = answer.text.strip()
            correct = correct[4:]
            # vreau sa vad ce cheie salvez ca si corecta din dictionar
            for key, value in options.items():
                if value == correct:
                    correct_answer.append(key)
        
    image_url = question.find("img")["src"] if question.find("img") else None

    # vreau sa salvez calea imaginii in loc de link-ul imaginii
    image_local_path = None
    if image_url:
        # afla calea actuala a fisierului
        current_path = os.path.dirname(os.path.realpath(__file__))
        # adauga /images la calea actuala
        image_local_path = os.path.join(current_path, "images")
        # adauga ultima parte din image_url la calea locala , adica ignora /storage/questions/ din exemplul /storage/questions/01JK5VE5VN14YACMQR50JJT7VR.jpg
        image_local_path = os.path.join(image_local_path, image_url.split("/")[-1])
    
    # adaugam intrebarea in lista de intrebari
    questions_data.append({
        "text": text,
        "options": options,
        "correct_answer": correct_answer,
        "image_local_path": image_local_path
    })

db = client["drpciv"]  # baza de date
collection = db["questions"]  # colectia

collection.delete_many({})  # stergem toate documentele existente

collection.insert_many(questions_data)

print(f"Am salvat {len(questions_data)} întrebări în MongoDB!")

# conversie ObjectId la string pentru a putea salva în JSON
def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # convertim ObjectId la string
    raise TypeError(f"Type {type(obj)} not serializable")

# salvare în JSON
with open("intrebari.json", "w", encoding="utf-8") as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=4, default=json_serial)

print(f"Am extras {len(questions_data)} întrebări.")

