import numpy as np
import pandas as pd
import re
import sacrebleu
from bert_score import score
from rouge_score import rouge_scorer

df = pd.read_excel("proseGenerationQs.xlsx")
df.head()

def cleanProse(text: str) -> str:
    if text is None:
        return ""
    text = re.sub(r'</?answer>', '', text)
    return text.strip()

for index, row in df.iterrows():
  df.at[index, "Claude Sonnet 4.5"] = cleanProse(row["Claude Sonnet 4.5"])
  df.at[index, "DeepSeek V3.2"] = cleanProse(row["DeepSeek V3.2"])
  df.at[index, "Gemma 3 12B Instruct"] = cleanProse(row["Gemma 3 12B Instruct"])
  df.at[index, "Gemma 3 27B Instruct"] = cleanProse(row["Gemma 3 27B Instruct"])

refs = df["Couplet Text"].tolist()

"""## BERTScore F1"""

hyps = df["Claude Sonnet 4.5"].tolist()
P, R, F1 = score(
    hyps,
    refs,
    lang="fa",
    model_type="xlm-roberta-large",
    verbose=True
)
bert_f1 = F1.mean().item()
print("BERTScore F1:", bert_f1)

hyps = df["DeepSeek V3.2"].tolist()
P, R, F1 = score(
    hyps,
    refs,
    lang="fa",
    model_type="xlm-roberta-large",
    verbose=True
)
bert_f1 = F1.mean().item()
print("BERTScore F1:", bert_f1)

hyps = df["Gemma 3 12B Instruct"].tolist()
P, R, F1 = score(
    hyps,
    refs,
    lang="fa",
    model_type="xlm-roberta-large",
    verbose=True
)
bert_f1 = F1.mean().item()
print("BERTScore F1:", bert_f1)

hyps = df["Gemma 3 27B Instruct"].tolist()
P, R, F1 = score(
    hyps,
    refs,
    lang="fa",
    model_type="xlm-roberta-large",
    verbose=True
)
bert_f1 = F1.mean().item()
print("BERTScore F1:", bert_f1)

"""## chrF++"""

hyps = df["Claude Sonnet 4.5"].tolist()
chrfpp = sacrebleu.corpus_chrf(
    hyps,
    [refs],
    word_order=2
)
print("chrF++:", chrfpp.score)

hyps = df["DeepSeek V3.2"].tolist()
chrfpp = sacrebleu.corpus_chrf(
    hyps,
    [refs],
    word_order=2
)
print("chrF++:", chrfpp.score)

hyps = df["Gemma 3 12B Instruct"].tolist()
chrfpp = sacrebleu.corpus_chrf(
    hyps,
    [refs],
    word_order=2
)
print("chrF++:", chrfpp.score)

hyps = df["Gemma 3 27B Instruct"].tolist()
chrfpp = sacrebleu.corpus_chrf(
    hyps,
    [refs],
    word_order=2
)
print("chrF++:", chrfpp.score)

"""## BLEU-4"""

hyps = df["Claude Sonnet 4.5"].tolist()
bleu = sacrebleu.corpus_bleu(hyps, [refs])
print("BLEU-4:", bleu.score)

hyps = df["DeepSeek V3.2"].tolist()
bleu = sacrebleu.corpus_bleu(hyps, [refs])
print("BLEU-4:", bleu.score)

hyps = df["Gemma 3 12B Instruct"].tolist()
bleu = sacrebleu.corpus_bleu(hyps, [refs])
print("BLEU-4:", bleu.score)

hyps = df["Gemma 3 27B Instruct"].tolist()
bleu = sacrebleu.corpus_bleu(hyps, [refs])
print("BLEU-4:", bleu.score)