import json
import unicodedata
from collections import defaultdict
import re
import traceback
import ollama
import os
import base64
import random

# Tokenul JWT de autentificare
auth_token = os.getenv("AUTH_TOKEN")
if not auth_token:
    raise ValueError("Lipsește AUTH_TOKEN din fișierul .env!")# Creează clientul Ollama autenticat
client = ollama.Client(
    host='https://chat.readerbench.com/ollama',
    headers={"Authorization": f"Bearer {auth_token}"}
)

# Încarcă întrebările
with open('intrebari.json', 'r', encoding='utf-8') as f:
    intrebari = json.load(f)

# Încărcare imagine în base64
def image_to_base64(cale):
    if cale and os.path.exists(cale):
        with open(cale, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

with open("cod_rutier.json", "r", encoding="utf-8") as f:
    original = f.read()
with open("articole_cod_rutier.json", "r", encoding="utf-8") as f:
    articole = json.load(f)

reconstruit = "\n".join([a["continut"] for a in articole.values()])
print("Diferență de caractere:", abs(len(original) - len(reconstruit)))
def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()
print(normalize("Șoferul a încălcat marcajul."))


    # prompt_fara = f"""
    #     Întrebare: {intrebare['text']}
    #     Opțiuni: {optiuni_formatate}

    #     Instrucțiuni:
    #     Răspunde DOAR cu literele mari corespunzătoare opțiunilor corecte, fără explicații.
    #     Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele.
    #     Formatul răspunsului trebuie să fie exact: ["A"], ["B"], ["C"], ["A", "B"], ["A", "C"], ["B", "C"], ["A", "B", "C"].
    # """.strip()
    # prompt_cu = f"""
    #     Întrebare: {intrebare['text']}
    #     Opțiuni: {optiuni_formatate}
    #     Context util extras automat din Codul Rutier: {context}

    #     Instrucțiuni:
    #     Bazându-te pe contextul de mai sus, răspunde DOAR cu literele opțiunilor corecte. 
    #     Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele.
    #     Formatul răspunsului trebuie să fie exact: ["A"], ["B"], ["C"], ["A", "B"], ["A", "C"], ["B", "C"], ["A", "B", "C"].
    #     """.strip()
    # prompt_cu_greseala = f"""
    #         Întrebare: {intrebare['text']}
    #         Opțiuni: {optiuni_formatate}
    #         Context util extras automat din Codul Rutier:
    #         {context}

    #         Instrucțiuni:
    #         ATENȚIE: Răspunsul anterior ({rasp_fara}) este greșit.
    #         Bazându-te pe contextul de mai sus, răspunde DOAR cu literele opțiunilor corecte, în ordine alfabetică.
    #         Selectează doar opțiunile corecte, în ordine alfabetică, fără a repeta literele.
    #         Formatul răspunsului trebuie să fie exact: ["A"], ["B"], ["C"], ["A", "B"], ["A", "C"], ["B", "C"], ["A", "B", "C"].
    #     """.strip()

def trimite_prompt(prompt, imagine_b64=None, model="llava:34b"):
    try:
        params = {
            "model": model,
            "prompt": prompt,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "num_predict": 256
            },
            "stream": False
        }
        if imagine_b64:
            params["images"] = [imagine_b64]

        response = client.generate(**params)
        return response.response.strip()

    except Exception as e:
        print("Eroare Ollama:", e)
        traceback.print_exc()
        return "Eroare"

# Filtrăm doar întrebările cu imagini
intrebari_cu_imagini = [i for i in intrebari if i.get("image_local_path") and os.path.exists(i["image_local_path"])]

# Selectăm 5 random (sau primele 5)
selectate = intrebari_cu_imagini[:5]

rezultate = []

for intrebare in selectate:
    cale_img = intrebare["image_local_path"]
    imagine_b64 = image_to_base64(cale_img)
    prompt = "Ce vezi în imagine?"

    rasp_fara = trimite_prompt(prompt, model="mistral-small3.1:latest")
    rasp_cu = trimite_prompt(prompt, imagine_b64, model="mistral-small3.1:latest")

    print(f"\nImagine: {cale_img}")
    print("Fără imagine:", rasp_fara)
    print("Cu imagine:", rasp_cu)

    rezultate.append({
        "intrebare": intrebare["text"],
        "cale_imagine": cale_img,
        "fara_imagine": rasp_fara,
        "cu_imagine": rasp_cu
    })

# Salvăm rezultatele
with open("rezultate_test_imagini.json", "w", encoding="utf-8") as f:
    json.dump(rezultate, f, ensure_ascii=False, indent=2)

print("\n✅ Testul pe imagini a fost finalizat.")


from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Lista de etichete pentru clasificare
etichete = [
  "Presemnalizarea direcțiilor la o intersecție de drumuri din afara localității",
  "Presemnalizarea direcțiilor la o intersecție denivelată de drumuri",
  "Presemnalizarea direcțiilor indicate",
  "Presemnalizarea traseului de ocolire a localității",
  "Presemnalizare direcțiilor într-o intersecție cu sens giratoriu",
  "Drum închis sau deschis circulației publice",
  "Presemnalizarea traseului de urmat în cazul unei restricții de circulație",
  "Presemnalizare pe autostradă pentru parcare",
  "Presemnalizare pe autostradă pentru spațiu de servicii",
  "Confirmarea direcției de mers pe autostradă spre localități mai importante și distanțele până la acestea",
  "Presemnalizarea unui loc periculos, o intersecție sau o restricție pe un drum lateral",
  "Bandă rezervată circulației de transport public de persoane",
  "Drum fără ieșire",
  "Presemnalizarea traseului de urmat în vederea efectuării virajului la stânga",
  "Traseu de urmat pentru anumite categorii de autovehicule",
  "Traseu de urmat pentru un anumit tip de autovehicule",
  "Traseu de urmat pentru un anumit tip de autovehicul",
  "Selectarea circulației pe direcții de mers în apropierea intersecției",
  "Selectarea circulației pe direcții de mers în apropierea intersecției",
  "Selectarea direcției de mers în apropierea intersecției",
  "Bandă destinată circulației vehiculelor lente",
  "Terminarea benzii de circulație din dreapta a părții de carosabil",
  "Terminarea benzii de circulație din stânga părții carosabile",
  "Viteză minimă obligatorie pentru o bandă de circulație",
  "Viteză minimă obligatorie pentru diferite benzi de circulație",
  "Limitare de viteză pentru diferite benzi de circulație",
  "Bandă de circulație rezervată autovehiculelor de transport public de persoane",
  "Direcția spre localitatea indicată",
  "Direcție spre autostrada indicată",
  "Direcția spre localitatea indicată",
  "Direcția de urmat pentru autovehiculele destinate transportului de mărfuri",
  "Direcția spre obiectivul turistic",
  "Direcția spre obiective locale",
  "Direcția spre aeroport",
  "Direcția de urmat în cazul devierii temporare a circulației",
  "Direcția de urma în cazul devierii temporare a circulației",
  "Drum național",
  "Drum județean",
  "Drum comunal",
  "Drum deschis traficului internațional",
  "Direcția drumului deschis traficului internațional",
  "Traseu de tranzit european",
  "Simbolul și numărul autostrăzii",
  "Intrare în localitate",
  "Intrare în localitate",
  "Ieșire din localitate",
  "Ieșire din localitate",
  "Limitp de județ",
  "Curs de apă sau viaduct",
  "Confirmarea direcției de mers spre o localitate și distanța până la aceasta",
  "Confirmarea direcției de mers spre localități mai importante și distanțele până la acestea",
  "Organizarea traficului pe benzi de circulație",
  "Telefon de urgență (Poliție, Ambulanță, Pompieri, Depanare).",
  "Curbă la stânga",
  "Drum îngustat pe ambele părți",
  "Curbă la dreapta",
  "Curbă dublă",
  "Coborăre periculoasă",
  "Urcare cu înclinare mare",
  "Curbă dublă sau o succesiune de mai mult de două curbe, prima la dreapta",
  "Curbă deosebit de periculoasă",
  "Panouri succesive pentru curbe deosebit de periculoase",
  "Drum îngustat pe partea dreaptă",
  "Drum îngustat pe partea stângă",
  "Acostament periculos",
  "Drum aglomerat",
  "Tunel",
  "Pod mobil",
  "Ieșire spre un chei sau mal abrupt",
  "Drum cu denivelări",
  "Denivelare pentru limitarea vitezei",
  "Drum lunecos",
  "Împreșcare cu pietriș",
  "Căderi de pietre",
  "Presemnalizare trecere pietoni",
  "Copii",
  "Bicicliști",
  "Animale",
  "Animale",
  "Lucrări",
  "Semafoare",
  "Aeroport",
  "Vânt lateral",
  "Circulație în ambele sensuri",
  "Alte pericole",
  "Accident",
  "Intersecție de drumuri",
  "Intersecție cu drum fără prioritate",
  "Intersecție cu drum fără prioritate",
  "Intersecție cu drum fără prioritate",
  "Intersecție cu drum fără prioritate",
  "Presemnalizare intersecție cu sens giratoriu",
  "Trecere la nivel cu cale ferată cu bariere sau semibariere",
  "Trecere la nivel cu o cale ferată fără bariere",
  "Trecere la nivel cu linii de tramvai",
  "Mașini și utilaje agricole",
  "Presemnalizarea unei amenajări rutiere care permite întoarcerea vehiculului",
  "Baliză direcțională care indică ocolirea obstacolului prin partea stângă",
  "Baliză direcțională care indică ocolirea obstacolului prin partea dreaptă",
  "Baliză bidirecțională",
  "Panouri suplimentare pentru trecerea la nivel cu cale ferată",
  "Panouri suplimentare la nodurile rutiere de pe autostrăzi",
  "Trecere la nivel cu o cale ferată, fără bariere",
  "Trecere la nivel cu cale ferată dublă, fără bariere",
  "Accesul interzis",
  "Circulația interzisă în ambele sensuri",
  "Accesul interzis autovehiculelor cu excepția motocicletelor fără ataș",
  "Accesul interzis motocicletelor",
  "Accesul interzis bicicletelor",
  "Accesuk interzis mopedelor (ciclometrelor)",
  "Accesul interzis vehiculelor destinate transportului de mărfuri",
  "Accesul interzis autovehiculelor cu remorcă, cu excepția celor cu semiremorcă sau cu remorcă cu o osie",
  "Accesul interzis autobuzelor",
  "Accesul interzis pietonilor",
  "Accesul interzis vehiculelor cu tracțiune animală",
  "Accesul interzis vehiculelor împinse sau trase cu mâna",
  "Accesul interzis tractoarelor și mașinilor autopropulsate pentru lucrări",
  "Accesul interzis autovehiculelor",
  "Accesul interzis autovehiculelor și vehiculelor cu tracțiune animală",
  "Accesul interzis vehiculelor cu lățimea mai mare de ... m",
  "Accesul interzis vehiculelor cu înălțimea mai mare de .. m",
  "Accesul interzis vehiculelor cu masă mai mare de .. t",
  "Accesul interzis vehiculelor cu masă mai mare de ... t pe osia simplă",
  "Accesul interzis vehiculelor cu masă pe osia dublă mai mare de ... t",
  "Accesul interzis vehiculelor cu masa pe osia tripla mai mare de ... t",
  "Accesul interzis autovehiculelor sau ansamblurilor de vehicule cu lungimea mai mare de ... m",
  "Interzis autovehiculelor de a circula fără a menține între ele un interval de cel puțin ... m",
  "Interzis a vira la stânga",
  "Interzis a vira la dreapta",
  "Întoarcerea interzisă",
  "Depășirea autovehiculelor, cu excepția motocicletelor fără ataș, interzisă",
  "Depășirea interzisă autovehiculelor destinate transportului de mărfuri",
  "Limitare de viteză",
  "Limitare de viteză diferențiată pe categorii de autovehicule",
  "Claxonarea interzisă",
  "Vamă",
  "Taxă de trecere",
  "Control poliție",
  "Sfârșitul tuturor restricțiilor",
  "Sfârșitul limitării de viteză",
  "Sfârșitul interzicerii de a depăși",
  "Staționare interzisă",
  "Oprire interzisă",
  "Staționarea alternată",
  "Staționare alternată",
  "Zonă de staționare cu durată limitată",
  "Sfârșitul zonei cu staționare cu durată limitată",
  "Zonă cu limitare de viteză la 30 km/h",
  "Sfârșitul zonei de viteză limitată la 30 km/h",
  "Accesul interzis autovehiculelor care transportă substanțe explozive sau ușor inflamabile",
  "Accesul interzis vehiculelor care transportă mărfuri periculoase",
  "Accesul interzis autovehiculelor care transportă substanțe de natură să polueze apele",
  "Cedează trecerea",
  "Oprire",
  "Drum cu prioritate",
  "Sfârșitul drumului cu prioritate",
  "Prioritate pentru circulația din sens invers",
  "Prioritate față circulația din sens invers",
  "Înainte",
  "Înainte",
  "La dreapta",
  "La dreapta",
  "Înainte sau la dreapta",
  "Ocolire",
  "Ocolire",
  "Intersecție cu sens giratoriu",
  "Pistă pentru biciclete",
  "Drum obligatoriu pentru categoria de vehicule",
  "Drum pentru pietoni",
  "Delimitare piste pentru pietoni și biciclete",
  "Pistă comună pentru pietoni și bicicliști",
  "Viteză minimă obligatorie",
  "Sfârșitul vitezei minime obligatorii",
  "Lanțuri pentru zăpadă",
  "Direcție obligatorie pentru autovehiculele care transportă mărfuri periculoase",
  "Direcție obligatorie pentru vehicule care transportă mărfuri periculoase",
  "Direcție obligatorie pentru vehicule care transportă mărfuri periculoase",
  "Direcția și distanța până la telefonul pentru apel de urgență",
  "Rovignietă",
  "Trecere de pietoni",
  "Trecere pentru pietoni",
  "Limite generale de viteză",
  "Sens unic",
  "Sens unic",
  "Autostradă",
  "Sfârșit de autostradă",
  "Limite maxime de viteză pe autostradă, ân funcție de condițiile meteorologice",
  "Spital",
  "Poliția",
  "Post prim-ajutor",
  "Pasarelă pentru pietoni",
  "Pasaj subteran pentru pietoni",
  "Stație de autobuz",
  "Stație de tramvai",
  "Stație de taximetre",
  "Drum pentru autovehicule",
  "Sfârșitul drumului pentru autovehicule",
  "Vulcanizare",
  "Telefon",
  "Stație alimentare cu carburant",
  "Stație pentru alimentare cu carburant, inclusiv benzină fără plumb",
  "Stație de alimentare cu carburanți inclusiv benzină fără plumb și gaz petrolier lichefiat",
  "Hotel sau motel",
  "Restaurant",
  "Bufet sau cofetărie",
  "Teren pentru camping (tabără turistică)",
  "Teren pentru caravane (tabără turistică)",
  "Teren pentru caravane și camping",
  "Loc pentru popas",
  "Cabană pentru turiști",
  "WC public",
  "Service auto",
  "Parcare",
  "Parcare",
  "Parcare subterană sau în clădire",
  "Complex de servicii",
  "Zona rezidențială",
  "Sfârșitul zonei rezidențiale",
  "Zonă cu viteză recomandată de 30 km/h",
  "Sfârșitul zonei cu viteză recomandată de 30 km/h",
  "Zonă pietonală",
  "Sfârșitul zonei pietonale",
  "Tunel",
  "Sfârșit de tunel",
  "Îmbarcare pe vagoane platformă de cale ferată",
  "Îmbarcare pe ferry-boat",
  "Port",
  "Gară",
  "Autogară",
  "Închirieri auto",
  "Plajă",
  "Zonă de vânătoare",
  "Zonă de pescuit",
  "Centru viticol",
  "Zona industrială",
  "Poșta",
  "Apă potabilă",
  "Loc de joacă pentru copii",
  "Stadion",
  "Supermarket",
  "Acces internet",
  "Teatru",
  "Muzeu",
  "Cântar pentru autovehicule",
  "Control radar",
  "Informații rutiere",
  "Viteză recomandată",
  "Punct de informare turistică",
  "Denumirea străzii",
  "Intrare stradă indicată",
  "Numărul imobilului",
  "Monitorizare trafic",
  "Refugiu rezervat depanării",
  "Presemnalizarea sediului Poliției autostrăzii",
  "Distanța de siguranță între vehiculele pentru viteze de cel mult 60 km/h",
  "Distanța de siguranță între vehiculele pentru viteze mai maride  90 km/h"
]


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def clasifica_imagine(image_path, etichete):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=etichete, images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits_per_image
        probs = logits.softmax(dim=1).squeeze()

    rezultate = list(zip(etichete, probs.tolist()))
    rezultate.sort(key=lambda x: x[1], reverse=True)
    return rezultate[:3]

predictii = clasifica_imagine("/mnt/c/Users/Burak/Desktop/licenta/images/420.jpeg", etichete)
print("\nPredicții pentru imagine:")
for eticheta, probabilitate in predictii:
    print(f"{eticheta}: {probabilitate:.4f}")
