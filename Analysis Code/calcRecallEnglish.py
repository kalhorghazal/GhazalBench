import pandas as pd
import numpy as np
import editdistance
from collections import Counter
import unicodedata
import re

df = pd.read_excel("completionQsEnglish.xlsx")
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


def normalizeEnglish(text):
    if text is None:
        return ""

    text = unicodedata.normalize("NFC", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def charEditDistance(pred, gold):
    p = normalizeEnglish(pred)
    g = normalizeEnglish(gold)
    return editdistance.eval(p, g)


def cer(pred, gold):
    g = normalizeEnglish(gold)
    if not g:
        return 1.0
    return charEditDistance(pred, gold) / len(g)


def allowedEditsByLength(text):
    length = len(text)
    if length < 40:
        return 1   # single typo
    elif length < 80:
        return 2
    else:
        return 3


def retrievalLabel(pred, gold, partial_cer_threshold=0.2):
    p = normalizeEnglish(pred)
    g = normalizeEnglish(gold)

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
  gold = row["Second Line"]
  df.at[index, "Score (Claude Sonnet 4.5)"] = retrievalLabel(pred, gold)

df["Score (DeepSeek V3.2)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["DeepSeek V3.2"])
  gold = row["Second Line"]
  df.at[index, "Score (DeepSeek V3.2)"] = retrievalLabel(pred, gold)

df["Score (Gemma 3 27B Instruct)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["Gemma 3 27B Instruct"])
  gold = row["Second Line"]
  df.at[index, "Score (Gemma 3 27B Instruct)"] = retrievalLabel(pred, gold)

df["Score (Gemma 3 12B Instruct)"] = np.nan

for index, row in df.iterrows():
  pred = extractAnswer(row["Gemma 3 12B Instruct"])
  gold = row["Second Line"]
  df.at[index, "Score (Gemma 3 12B Instruct)"] = retrievalLabel(pred, gold)

df.to_excel("completionQsEnglish.xlsx", index=False)