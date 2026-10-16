from bs4 import BeautifulSoup
import requests
import json
import os


with open("indicatoare.json", "r", encoding="utf-8") as f:
    indicatoare2 = json.load(f)

# ia din directorul cu indicatoare_img si scrie intr-un fisier nume_indicatoare.txt toate numele indicatoarelor
with open("nume_indicatoare.txt", "w", encoding="utf-8") as f:
    # scoate din articol "Indicator " si scrie numele indicatoarelor
    for indicator in indicatoare2:
        nume = indicator["articol"]
        f.write(f"{nume.replace('Indicator ', '')}\n")

# make it unique
with open("nume_indicatoare.txt", "r", encoding="utf-8") as f:
    nume_indicatoare = f.readlines()
nume_indicatoare = list(set(nume_indicatoare))
# sort alphabetically
nume_indicatoare.sort()
with open("nume_indicatoare.txt", "w", encoding="utf-8") as f:
    for nume in nume_indicatoare:
        f.write(nume)


print(f"Salvate {len(indicatoare2)} indicatoare.")
