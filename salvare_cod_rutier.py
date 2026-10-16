import requests
from bs4 import BeautifulSoup
import json
import re
from collections import defaultdict

def extrage_cod_rutier():
    url = "https://www.drpciv-romania.ro/Code/Applications/web/index.cgi?action=codulrutier"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'  # corectam diacriticele

    soup = BeautifulSoup(r.text, "html.parser")
    rezultate = {}

    # cautam TOATE butoanele de tip collapsible
    butoane = soup.select("button[data-toggle='collapse']")

    for button in butoane:
        # curatam titlu de iconite si extragem textul
        for icon in button.select("i"):
            icon.decompose()
        titlu = button.get_text(strip=True)

        # extragem id-ul div-ului asociat
        data_target = button.get("data-target")
        if not data_target:
            continue

        id_div = data_target.replace("#", "")
        div_content = soup.find("div", id=id_div)

        if div_content:
            continut = div_content.get_text(separator="\n", strip=True)
            rezultate[titlu] = continut

    for cheie in list(rezultate.keys()):
        if not cheie.strip():
            del rezultate[cheie]
    return rezultate
# Extragem și salvăm
cod_rutier = extrage_cod_rutier()

with open("cod_rutier.json", "w", encoding="utf-8") as f:
    json.dump(cod_rutier, f, ensure_ascii=False, indent=2)

print("Codul rutier a fost salvat în 'cod_rutier.json'.")


with open("cod_rutier.json", "r", encoding="utf-8") as f:
    cod_rutier = json.load(f)

articole = {}

# pattern pentru Art. numar sau Art. numar.numar
articol_pattern = re.compile(r"^Art\. ?(\d+[A-Za-z0-9\.]*)\s*$", re.MULTILINE)

# pattern pentru delimitarea paragrafelor stricte: \n(număr)\n
paragraf_delimitator = re.compile(r"\n\((\d+(?:\.\d+)?)\)\n")

for capitol, continut in cod_rutier.items():
    lines = continut.split("\n")
    current_articol = None
    buffer = []

    for i, linie in enumerate(lines):
        linie_strip = linie.strip()
        match_art = articol_pattern.match(linie_strip)
        
        if match_art:
            # finalizeaza articolul anterior
            if current_articol and buffer:
                raw_text = "\n".join(buffer).strip()
                splits = list(paragraf_delimitator.finditer(raw_text))

                if splits:
                    for idx, match in enumerate(splits):
                        cod = match.group(1)
                        start = match.end()
                        end = splits[idx + 1].start() if idx + 1 < len(splits) else len(raw_text)
                        par_text = raw_text[start:end].strip()
                        articole[f"Art.{current_articol}({cod})"] = {
                            "capitol": capitol,
                            "continut": par_text
                        }
                else:
                    articole[f"Art.{current_articol}"] = {
                        "capitol": capitol,
                        "continut": raw_text
                    }

            current_articol = match_art.group(1).replace(" ", "")
            buffer = []
        if current_articol is not None:
            buffer.append(linie)

    # finalizeaza ultimul articol
    if current_articol and buffer:
        raw_text = "\n".join(buffer).strip()
        splits = list(paragraf_delimitator.finditer(raw_text))

        if splits:
            for idx, match in enumerate(splits):
                cod = match.group(1)
                start = match.end()
                end = splits[idx + 1].start() if idx + 1 < len(splits) else len(raw_text)
                par_text = raw_text[start:end].strip()
                articole[f"Art.{current_articol}({cod})"] = {
                    "capitol": capitol,
                    "continut": par_text
                }
        else:
            articole[f"Art.{current_articol}"] = {
                "capitol": capitol,
                "continut": raw_text
            }


# salvare finala
with open("articole_cod_rutier.json", "w", encoding="utf-8") as f:
    json.dump(articole, f, ensure_ascii=False, indent=2)

print(f"Articole și paragrafe salvate: {len(articole)}")