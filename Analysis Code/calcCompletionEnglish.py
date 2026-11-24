import pandas as pd
import numpy as np
import editdistance
from collections import Counter
import unicodedata
import re

df = pd.read_excel("sonnets.xlsx")

# -----------------------------
# Extract answer from LLM output
# -----------------------------
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


# -----------------------------
# English text normalization
# -----------------------------
def normalize_english(text):
    if text is None:
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # Normalize whitespace only
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------
# Edit distance helpers
# -----------------------------
def char_edit_distance(pred, gold):
    p = normalize_english(pred)
    g = normalize_english(gold)
    return editdistance.eval(p, g)


def cer(pred, gold):
    g = normalize_english(gold)
    if not g:
        return 1.0
    return char_edit_distance(pred, gold) / len(g)


# -----------------------------
# Retrieval labeling
# -----------------------------
def allowed_edits_by_length(text):
    """Allow minimal tolerance for English +Shuffleic lines"""
    length = len(text)
    if length < 40:
        return 1   # single typo
    elif length < 80:
        return 2
    else:
        return 3


def retrieval_label(pred, gold, partial_cer_threshold=0.2):
    p = normalize_english(pred)
    g = normalize_english(gold)

    ed = editdistance.eval(p, g)
    cer_val = ed / max(1, len(g))

    # COMPLETE: near-exact match
    if ed <= allowed_edits_by_length(g):
        return "Complete"

    # PARTIAL: recognizable but flawed retrieval
    elif cer_val <= partial_cer_threshold:
        return "Partial"

    # NON-RETRIEVAL: wrong line
    else:
        return "Non-Retrieval"


for index, row in df.iterrows():
  pred = extract_answer(row["Model Output"])
  gold = row["Second Line"]
  df.at[index, "Retrieval Label"] = retrieval_label(pred, gold)


df.to_excel("sonnets.xlsx", index=False)