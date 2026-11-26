!pip install bert-score sacrebleu pandas torch sentencepiece

import numpy as np
import pandas as pd
from bert_score import score
import sacrebleu
import re

df = pd.read_excel("ghazalsHafez.xlsx")

def extract_answer(text):
    match = re.fullmatch(
        r"\s*<answer>(.*?)</answer>\s*",
        text,
        flags=re.DOTALL
    )
    if match:
        return match.group(1).strip()
    else:
        print("Format error: <answer>...</answer> not found")
        return None

df["Paraphrased Prose"] = df["Paraphrased Prose"].apply(extract_answer)

refs = df["Prose"].astype(str).tolist()
hyps = df["Paraphrased Prose"].astype(str).tolist()

P, R, F1 = score(
    hyps,
    refs,
    lang="fa",
    model_type="xlm-roberta-large",
    verbose=True
)

bert_f1 = F1.mean().item()
bert_p = P.mean().item()
bert_r = R.mean().item()

print(f"BERTScore Precision: {bert_p:.4f}")
print(f"BERTScore Recall:    {bert_r:.4f}")
print(f"BERTScore F1:        {bert_f1:.4f}")

bleu = sacrebleu.corpus_bleu(
    hyps,
    [refs],
    tokenize="none"
)

bleu_score = bleu.score
print(f"SacreBLEU: {bleu_score:.4f}")