import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib

# Folosește un backend fără interfață grafică (compatibil cu WSL/CLI)
matplotlib.use("Agg")
# Valorile finale extrase din noul screenshot
models = [
    "Gemma3:27b (No image)", "Llava:34b (No image)",
    "Gemma3:27b (With image)", "Llava:34b (With image)"
]

# Corect fără și cu context
aa = [398, 344, 165, 166]
# Greșit fără, dar corect cu context
tp = [134, 79, 31, 14]
# Corect fără, dar greșit cu context
fn = [28, 36, 12, 15]
# Greșit în ambele
fp = [267, 368, 177, 190]

# Construim matricea 2x2 pentru fiecare model
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, model in enumerate(models):
    cm = np.array([
        [aa[i], fn[i]],  # corect fără context
        [tp[i], fp[i]]   # greșit fără context
    ])
    
    df_cm = pd.DataFrame(cm,
                         index=["Correct w/o context", "Wrong w/o context"],
                         columns=["Correct with context", "Wrong with context"])
    
    sns.heatmap(df_cm, annot=True, fmt='d', cmap="YlOrRd", ax=axes[i], vmin=0, vmax=450, annot_kws={"size": 22})
    axes[i].set_title(model, fontsize=18)
    axes[i].tick_params(axis='both', labelsize=14)

plt.tight_layout()
img_path = "final_confusion_matrix_updated.png"
plt.savefig(img_path)
plt.close()

img_path
