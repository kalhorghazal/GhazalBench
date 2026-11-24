import pandas as pd
import numpy as np
import editdistance
from collections import Counter
import unicodedata
import re

df = pd.read_excel("ghazals.xlsx")

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
# Persian text normalization
# -----------------------------
PERSIAN_MAP = {
    "ي": "ی",
    "ك": "ک",
    "ة": "ه",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "ٱ": "ا",
}

DIACRITICS = re.compile(r"[\u064B-\u065F\u0670]")

def normalize_persian(text):
    if text is None:
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # Remove kashida (tatweel) — these are just formatting characters
    text = text.replace("\u0640", "")

    # Arabic → Persian character normalization
    for ar, fa in PERSIAN_MAP.items():
        text = text.replace(ar, fa)

    # Remove diacritics (tashkeel)
    text = DIACRITICS.sub("", text)

    # Remove half-space (ZWNJ)
    text = text.replace("\u200c", " ")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------
# Edit distance helpers
# -----------------------------
def char_edit_distance(pred, gold):
    p = normalize_persian(pred)
    g = normalize_persian(gold)
    return editdistance.eval(p, g)


def cer(pred, gold):
    g = normalize_persian(gold)
    if not g:
        return 1.0
    return char_edit_distance(pred, gold) / len(g)


# -----------------------------
# Retrieval labeling
# -----------------------------
def allowed_edits_by_length(text):
    """Allow more tolerance for longer verses"""
    length = len(text)
    if length < 40:
        return 1
    elif length < 80:
        print("long")
        return 2
    else:
        print("too long")
        return 3


def retrieval_label(pred, gold, partial_cer_threshold=0.2):
    p = normalize_persian(pred)
    g = normalize_persian(gold)

    ed = editdistance.eval(p, g)
    cer_val = ed / max(1, len(g))

    # COMPLETE: near-exact match
    if ed <= allowed_edits_by_length(g):
        return "Complete"

    # PARTIAL: significant overlap
    elif cer_val <= partial_cer_threshold:
        return "Partial"

    # NON-RETRIEVAL: wrong verse
    else:
        return "Non-Retrieval"


for index, row in df.iterrows():
  pred = extract_answer(row["Model Output"])
  gold = row['Couplet Text'].split("/")[1].strip()
  df.at[index, "Retrieval Label"] = retrieval_label(pred, gold)


df.to_excel("ghazals.xlsx", index=False)