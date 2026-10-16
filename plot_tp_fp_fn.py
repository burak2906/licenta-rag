import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
# Folosește un backend fără interfață grafică (compatibil cu WSL/CLI)
matplotlib.use("Agg")

# Datele pentru fiecare model și tip de întrebare
models = ["Gemma3:27b (No image)", "Llava:34b (No image)",
          "Gemma3:27b (With image)", "Llava:34b (With image)"]

TP = np.array([532, 423, 196, 180])
FP = np.array([295, 404, 189, 205])
FN = np.array([28, 36, 12, 15])

x = np.arange(len(models))
bar_width = 0.6

fig, ax = plt.subplots(figsize=(10, 6))

# Plot stacked bars
p1 = ax.bar(x, TP, bar_width, label='TP (correct with context)', color='green')
p2 = ax.bar(x, FP, bar_width, bottom=TP, label='FP (incorrect with context)', color='red')
p3 = ax.bar(x, FN, bar_width, bottom=TP + FP, label='FN (broken by context)', color='purple')

# Titluri și etichete
ax.set_ylabel('Number of Questions')
ax.set_title('Distribution of TP, FP, FN')
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=30, ha='right')
ax.legend()
plt.ylim(0, max(TP + FP + FN) + 250)  # Setăm limita superioară pentru a avea spațiu de respirație
plt.tight_layout()
img_path = "llm_tp_fp_fn_distribution_en.png"
plt.savefig(img_path)
plt.close(fig)