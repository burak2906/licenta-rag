

# vreau sa deschid articole.json si sa le sortez alfabetic dupa articol in articole_sortate.json
import json
from operator import itemgetter
with open("articole.json", "r", encoding="utf-8") as f:
    articole = json.load(f)
# sortează alfabetic după articol dar elimina duplicatele
articole = {articol["articol"]: articol for articol in articole}.values()  # elimină duplicatele
articole_sortate = sorted(articole, key=itemgetter("articol"))
with open("articole_sortate.json", "w", encoding="utf-8") as f:
    json.dump(articole_sortate, f, ensure_ascii=False, indent=2)
print(f"Salvate {len(articole_sortate)} articole sortate în articole_sortate.json.")