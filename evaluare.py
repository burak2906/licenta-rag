import json
from pathlib import Path

#files = [f"raspunsuri_batch_llava_{i}.json" for i in range(1, 14)]
files = [f"raspunsuri_batch_{i}.json" for i in range(1, 14)]

tp = fp = fn = total = 0
fa = 0

for file in files:
    path = Path(file)
    if not path.exists():
        print(f"Lipsă: {file}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        batch = json.load(f)

    for r in batch:
        cu = r["raspuns_cu_context"]
        corect = r["raspuns_corect"]
        fara = r["raspuns_fara_context"]

        total += 1

        if cu == corect:
            tp += 1
        elif cu != corect:
            fp += 1
        if fara == corect:
            fa += 1
        if fara == corect and cu != corect:
            fn += 1  # a fost corect fara context, dar l-a stricat contextul

# Metrici
precision = tp / (tp + fp) if tp + fp > 0 else 0
recall = tp / (tp + fn) if tp + fn > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0

# Afișare rezultate
print(f"\nNumăr total întrebări: {total}")
print(f"Corecte cu context (TP): {tp}")
print(f"Greșite cu context (FP): {fp}")
print(f"Contextul a stricat (FN): {fn}")
print(f"Corecte fără context (FA): {fa}")

print(f"\nPrecision (cu context): {precision:.2f}")
print(f"Recall (cu context): {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
