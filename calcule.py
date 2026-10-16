# Valorile din tabelul ales de utilizator
# Folosim aceste valori pentru a calcula Accuracy, Recall (strict) și alte metrice

import pandas as pd

# Definim valorile brute pentru cele patru cazuri din tabel
data = {
    "Model": [
        "Gemma3:27b (No image)", 
        "LLaVA:34b (No image)", 
        "Gemma3:27b (With image)", 
        "LLaVA:34b (With image)"
    ],
    "Total": [827, 827, 385, 385],  # numărul total de întrebări de fiecare tip
    "Correct with context": [532, 423, 196, 180],
    "Correct without context": [426, 380, 177, 181],
    "Helped by context": [132, 85, 30, 17],
    "Harmed by context": [26, 35, 11, 15],
}

df = pd.DataFrame(data)

# Calculăm metricele
df["Accuracy with context"] = df["Correct with context"] / df["Total"]
df["Accuracy without context"] = df["Correct without context"] / df["Total"]
df["% Helped by context"] = df["Helped by context"] / df["Total"]
df["% Harmed by context"] = df["Harmed by context"] / df["Total"]
df["Recall strict"] = df["Helped by context"] / (df["Helped by context"] + df["Harmed by context"])

import ace_tools as tools; tools.display_dataframe_to_user(name="Evaluare modele LLM", dataframe=df)
