import pandas as pd
import numpy as np
import editdistance
from collections import Counter
import unicodedata
import re

df = pd.read_excel("completionQs.xlsx")
df.head()

def extractAnswer(text):
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

def normalizePersian(text):
    if text is None:
        return ""

    text = unicodedata.normalize("NFC", text)

    for ar, fa in PERSIAN_MAP.items():
        text = text.replace(ar, fa)

    text = DIACRITICS.sub("", text)

    text = text.replace("\u200c", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def charEditDistance(pred, gold):
    p = normalizePersian(pred)
    g = normalizePersian(gold)
    return editdistance.eval(p, g)


def cer(pred, gold):
    g = normalizePersian(gold)
    if not g:
        return 1.0
    return charEditDistance(pred, gold) / len(g)


def allowedEditsByLength(text):
    length = len(text)
    if length < 40:
        return 1
    elif length < 80:
        print("long")
        return 2
    else:
        print("too long")
        return 3


def recallLabel(pred, gold, partial_cer_threshold=0.2):
    p = normalizePersian(pred)
    g = normalizePersian(gold)

    ed = editdistance.eval(p, g)
    cer_val = ed / max(1, len(g))

    if ed <= allowedEditsByLength(g):
        return "Complete"

    elif cer_val <= partial_cer_threshold:
        return "Partial"

    else:
        return "Non-Retrieval"

df["Score (Claude Sonnet 4.5)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["Claude Sonnet 4.5"])
  gold = row["Correct"]
  df.at[index, "Score (Claude Sonnet 4.5)"] = recallLabel(pred, gold)

df["Score (DeepSeek V3.2)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["DeepSeek V3.2"])
  gold = row["Correct"]
  df.at[index, "Score (DeepSeek V3.2)"] = recallLabel(pred, gold)

df["Score (Gemma 3 27B Instruct)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["Gemma 3 27B Instruct"])
  gold = row["Correct"]
  df.at[index, "Score (Gemma 3 27B Instruct)"] = recallLabel(pred, gold)

df["Score (Gemma 3 12B Instruct)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["Gemma 3 12B Instruct"])
  gold = row["Correct"]
  df.at[index, "Score (Gemma 3 12B Instruct)"] = recallLabel(pred, gold)

df.to_excel("completionQs.xlsx", index=False)
