# DPIA Assistant for the DPDP Act

A command-line tool that carries out the first draft of a **Data Protection Impact Assessment (DPIA)**
for India's Digital Personal Data Protection Act, 2023. It follows the same steps a privacy consultant
follows, and it produces a Word report with a risk register, legal evidence, residual risk and a sign-off block.

> **Design rule:** rules decide the risk. The retrieved law only supports it. No language model scores
> or writes anything, so every result can be traced to a fact and a rule.
> The output is decision support for a qualified reviewer. It is not legal advice.

## How it follows a real DPIA

| DPIA step | Stage in this tool | File |
|---|---|---|
| 1. Screening: is a DPIA needed? | Four questions give *Required / Recommended / Optional* | `agents/screening.py` |
| 2. Describe the processing | Interview becomes an `AssessmentProfile` of named facts | `agents/interviewer.py`, `agents/profile.py` |
| 3. Consultation | The report lists who should review it (the tool does not consult anyone) | `agents/report.py` |
| 4. Necessity and proportionality | Rules for notice, legal basis, consent, data minimisation, retention | `agents/scoring.py` |
| 5. Identify and score risks | Security, third-party, rights, children, transfer and governance rules; likelihood x impact; merge duplicates | `agents/scoring.py`, `agents/finding.py`, `agents/consolidator.py` |
| 5b. Legal evidence | MiniLM + FAISS find the DPDP provisions closest to each finding | `agents/retrieval.py` |
| 6. Measures and residual risk | Template drafting; inherent vs residual score; risk-appetite gate | `agents/drafting.py`, `agents/treatment.py` |
| 7. Sign-off and review | Report with approval block and review date | `agents/report.py` |

```
answers -> Profile -> Rules -> Findings -> Consolidate -> Evidence (RAG) -> Draft -> Treatment -> DOCX report
            facts      decide risk                        supports it                GRC gate
```

## The GRC part: residual risk and a risk-appetite gate

Each finding gets an **inherent score** (likelihood x impact, 1-25). The tool then projects a **residual
score** that assumes the recommended control is applied. A residual score at or above the **appetite
threshold (10)** cannot be accepted by the project owner. It is escalated to senior management.

Example from the demo: no breach process scores 20 (Critical). After a breach process is added it scores
10 (High). That is still at the threshold, so the tool says *escalate*. A fix reduces a risk. It does not
by itself make the remaining risk acceptable.

## Rubric (this project's own, not DPDP Act thresholds)

| Item | Value |
|---|---|
| Likelihood | Set by each rule. A missing control = 4. A "to confirm" item (transfer, SDF duties, non-consent basis) = 2. |
| Impact | Base value per rule (2 to 4), **+1** if sensitive data, children's data or large scale applies (unknown counts as yes). Maximum 5. |
| Score bands | 1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical |
| Effect of a control | Likelihood falls by 2 (minimum 1). Impact does not change. |
| Appetite threshold | Residual score of 10 or more needs a senior decision |
| Approver | Low: project owner. Medium: privacy lead / DPO. High or Critical: senior management. |

**Unknown is never safe.** If an answer is "not sure", no rule fires. The item appears under *open questions*
in the report. In screening, an unknown answer counts as a possible yes.

## Run it

```
pip install -r requirements.txt
python app.py --demo        # sample case: payroll for 8,000 employees. Report: outputs/DPIA_Report.docx
python app.py               # interactive interview
python -m pytest            # unit tests
python evaluate_retrieval.py   # tests the real MiniLM + FAISS retrieval against the rule labels
```

## Tests and evaluation

- `tests/` covers parsing, every rule (a clear "no" fires it, an unknown does not), the score rubric, the
  consolidator, the residual-risk gate, retrieval plumbing and the report file.
- Each rule carries `expected_chunk_ids`, the corpus chunks that should support its finding.
  `evaluate_retrieval.py` uses them to report **Recall@1, Recall@3 and MRR** for the real model.
- **Retrieval results:** *(run `python evaluate_retrieval.py` and paste the numbers and the failure list here)*

## Known limits

- The corpus has 20 curated provisions. It is a summary, not the full Act. Check every cited section against the official text.
- Check whether the DPDP Rules or sector rules add duties that this tool does not cover.
- Similarity means close wording. It does not prove that a provision applies. The similarity labels (Strong / Moderate / Weak) are not yet calibrated.
- The rubric values are judgement calls. The effect of a control (-2 likelihood) is a simple assumption.
- The tool does not consult people, check data accuracy, or audit processors.
- Not covered by a rule yet: data accuracy, retention periods that are too long, processor audits.

## Project layout

```
app.py                   run the whole assessment (--demo for the sample case)
demo_answers.py          scripted answers for the demo
evaluate_retrieval.py    Recall@k and MRR for the real retriever
agents/
  screening.py           stage 1
  profile.py, interviewer.py   stage 2
  scoring.py, finding.py       stages 3-4 (rules, score, Finding)
  consolidator.py        merge duplicates
  retrieval.py           MiniLM + FAISS
  drafting.py, treatment.py    stage 6 (text, residual risk)
  report.py              stage 7 (DOCX)
  pipeline.py            runs stages 3-6
knowledge/privacy_corpus.json   20 curated DPDP provisions
tests/
```
