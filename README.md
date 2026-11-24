# GhazalBench

This repository hosts **GhazalBench**, a benchmark designed to evaluate LLM interaction with Persian ghazals of Hafez and Saadi through usage-grounded diagnostic scenarios. The benchmark is introduced in the following paper:

**Title:** "GhazalBench: Canonical Verse Access in LLMs across Persian Ghazals and Shakespearean Sonnets"

**Authors:** Ghazal Kalhor and Yadollah Yaghoobzadeh

**URL:** https://doi.org/10.48550/arXiv.2603.09979

**Abstract:** "Persian poetry plays an active role in Iranian cultural practice, where verses by canonical poets such as Hafez and Saadi are frequently quoted, paraphrased, or completed from incomplete cues. Supporting such interactions requires language models to reliably access canonical verses from semantic and lexical information. We introduce GhazalBench, a benchmark for evaluating how large language models (LLMs) access the canonical surface forms of Persian ghazal under usage-grounded conditions. Unlike prior work that primarily treats memorization as a liability, GhazalBench studies settings in which access to exact wording is functionally important. The benchmark evaluates completion and recognition under varied semantic and lexical cues. Across proprietary and open-weight multilingual LLMs, exact completion remains challenging, while recognition is substantially stronger. Performance also varies across poets and model families. Parallel experiments on Shakespearean sonnets yield markedly higher completion for several models, consistent with differences in exposure to canonical texts. Our findings motivate evaluation frameworks that distinguish production from recognition and assess access to culturally significant canonical texts."

## Citation

If you use our data or analysis code in your work, please cite our paper as below.

```
@misc{kalhor-2027-ghazalbench,
    title = "{G}hazal{B}ench: Canonical Verse Access in {LLM}s across {P}ersian Ghazals and {S}hakespearean Sonnets",
    author = "Kalhor, Ghazal and Yaghoobzadeh, Yadollah",
    year = "2027",
    eprint = "2603.09979",
    archivePrefix = "arXiv",
    primaryClass = "cs.CL",
    url = "https://doi.org/10.48550/arXiv.2603.09979",
    note = "Accepted to the 18th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2027), Main Conference"
}
```
