# GhazalBench

This repository hosts **GhazalBench**, a benchmark for evaluating large language models' (LLMs') access to the canonical surface forms of Persian ghazals by Hafez and Saadi under controlled cueing conditions. The benchmark is introduced in the following paper:

**Title:** "GhazalBench: Canonical Verse Access in LLMs across Persian Ghazals and Shakespearean Sonnets"

**Authors:** Ghazal Kalhor and Yadollah Yaghoobzadeh

**URL:** https://doi.org/10.48550/arXiv.2603.09979

**Abstract:** "Persian poetry plays an active role in Iranian cultural practice, where verses by canonical poets such as Hafez and Saadi are frequently quoted, paraphrased, or completed from incomplete cues. Such practices can involve recalling canonical verses from partial semantic or lexical information, motivating the study of whether language models can access these texts. We introduce GhazalBench, a benchmark for evaluating how large language models (LLMs) access the canonical surface forms of Persian ghazals under controlled cueing conditions motivated by these practices. Unlike prior work that primarily treats memorization as a liability, GhazalBench studies settings in which access to exact wording is functionally important. The benchmark evaluates open-ended completion and multiple-choice recognition under varied semantic and lexical cues. These controlled tasks isolate canonical-text access rather than simulate naturalistic conversations. Across proprietary and open-weight multilingual LLMs, exact completion remains challenging, while recognition is substantially stronger. Performance also varies across poets and model families. Parallel experiments on Shakespearean sonnets yield markedly higher completion rates for several models, potentially reflecting differences in exposure to canonical texts. Additional experiments suggest that post-training may reduce direct continuation-based access to canonical text. Our findings motivate evaluation frameworks that distinguish production from recognition and assess behavioral access to culturally significant canonical text."

## Directories

The repository is organized into the following directories:

* **Analysis Code**: Contains Python scripts for calculating LLM completion rates on Persian ghazals by Hafez and Saadi and English sonnets by Shakespeare. It also includes scripts for assessing the quality of LLM-generated paraphrased prose against reference prose for Persian couplets.
 
* **Data**: Contains prompts for the Completion and Recognition tasks across different cueing conditions for Hafez, Saadi, and Shakespeare.

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
