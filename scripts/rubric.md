# Scoring Rubric

For each surviving paper, read the abstract and assign a **1–5 composite score**
plus a one-line rationale. The composite blends three sub-axes:

## Methodology (M)
RCT / meta-analysis > prospective cohort > retrospective cohort > case series > case report.
Penalize: n<30, no control, no blinding when feasible, weak stats.

## Source (S)
Top-tier (NEJM, JAMA, Lancet, BMJ) >
specialty flagship (Laryngoscope, JAMA Otolaryngol, Otolaryngol HNS, Plast Reconstr Surg) >
standard peer-reviewed >
predatory / preprint.

## Impact (I)
Effect size, NNT, generalizability, "would this change Monday morning practice?"

## Composite anchors

- **5** — practice-changing, strong methodology, top journal.
- **4** — solid evidence, likely to influence subspecialty practice.
- **3** — interesting/incremental, worth knowing about.
- **2** — limited evidence or niche; skim only.
- **1** — case report, weak design, or near-zero clinical applicability. (Dropped silently.)

## Novel-Technique Bump

A case report or case series describing a *new surgical technique* whose senior
author has prominence signals is bumped ~1 point (cap at 4).

**Both conditions required:**
- **Novelty cues:** "novel technique," "modified approach," "first description,"
  explicit single-surgeon technique paper.
- **Prominence proxies (any one):**
  - Top-tier academic affiliation (Hopkins, Stanford, Mayo, MEEI, MD Anderson,
    UCSF, Pitt, MSK, McGovern UTHealth, Hospital for Sick Children, etc.)
  - Named department chair / division chief
  - Prior PubMed publication track record in the same subspecialty (verifiable
    via a quick author lookup)

If a paper meets both, mark `novel_technique: true` in the per-paper data block
and apply the bump.

## Output format per paper

For each scored paper, produce a structured JSON record:

```json
{
  "pmid": "12345678",
  "score": 4,
  "novel_technique": true,
  "study_type": "Case Series",
  "n": 23,
  "rationale": "Case series would normally score 2-3, but novel technique from a department chair with rhinology track record meets the bump criteria.",
  "summary_sections": [
    {"label": "BACKGROUND", "text": "..."},
    {"label": "METHODS", "text": "..."},
    {"label": "RESULTS", "text": "..."},
    {"label": "LIMITATIONS", "text": "..."},
    {"label": "CLINICAL TAKEAWAY", "text": "..."}
  ],
  "noted_summary": "(only populated if score 2-3) 4-5 sentence summary."
}
```

Must Read papers (score ≥ 4 post-bump) require all 5 `summary_sections`.
Noted papers (score 2-3) require only `noted_summary`.
