# Evidence-Centric Adaptive DPIA — Complete Project Context

## 1. Project Overview

### Working project
**Agentic AI-Powered Data Protection Impact Assessment (DPIA) Assistant**

### Current research direction
The project is being developed as a **technical research paper + patent-oriented technical concept**, rather than simply an AI application.

The central idea is to move DPIA automation from a **static, document-centric workflow** toward an:

> **Evidence-centric, adaptive, traceable, and continuously maintainable DPIA process.**

The proposed system combines:
- Agentic AI / LLMs for natural-language understanding and adaptive interaction.
- Retrieval-augmented legal analysis.
- Structured evidence representation.
- Evidence fusion and conflict detection.
- Deterministic privacy-risk reasoning.
- Mitigation and residual-risk assessment.
- Confidence-based human review.
- Event-triggered, targeted DPIA reassessment.

The system should behave more like a genuine DPIA process rather than simply asking questions and generating a report.

---

# 2. Existing Prototype / Baseline

A functional prototype already exists.

### Current workflow

```text
Project Owner
      ↓
Interview Agent
      ↓
User Responses
      ↓
Retrieval Agent
      ↓
Relevant DPDP Provisions
      ↓
Risk Scoring Agent
      ↓
Drafting Agent
      ↓
Report Agent
      ↓
DPIA Report
```

### Current implementation

- Interview Agent uses fixed questions around:
  - personal data
  - purpose
  - consent
  - withdrawal
  - third-party sharing
  - retention
  - encryption
  - children's data
  - grievance mechanisms.
- Legal knowledge base is structured JSON.
- Legal entries contain metadata such as:
  - ID
  - source
  - section
  - topic
  - title
  - keywords
  - risk category
  - text
  - mitigation hint.
- Retrieval currently uses:
  - Sentence Transformers (`all-MiniLM-L6-v2`)
  - FAISS.
- Risk scoring is currently basic rule-based logic.
- Drafting is currently deterministic/template-based.
- `python-docx` is used for report generation.
- FLAN-T5 was considered/planned but is not currently implemented as the core drafting model.
- The current end-to-end prototype is operational.

### Current weaknesses

1. Duplicate findings occur because answers are processed independently.
2. Retrieval sometimes returns broad or irrelevant provisions.
3. Risk scoring is basic and does not fully reflect DPIA-style risk methodology.
4. Legal knowledge coverage is limited.
5. Drafting is not yet a full generative LLM workflow.
6. Formal evaluation is missing.
7. Agent autonomy is limited.
8. The workflow is largely sequential and does not maintain a strong persistent state.

---

# 3. Real DPIA Process Baseline

The architecture should follow the general structure of established DPIA processes rather than inventing a purely AI-centric workflow.

The reviewed ICO DPIA process provides the following functional baseline:

1. Determine whether a DPIA is required / screening.
2. Describe the processing:
   - nature
   - scope
   - context
   - purpose.
3. Consult relevant stakeholders / data subjects / DPO where appropriate.
4. Assess necessity and proportionality.
5. Identify and assess privacy risks to individuals:
   - likelihood
   - severity.
6. Identify mitigation measures.
7. Determine residual risk.
8. Obtain appropriate human / DPO review and sign-off.
9. Monitor and reassess when processing changes.

Important caveat:
The ICO material was used primarily as a **DPIA process reference**. It should not automatically be treated as the complete current legal framework for every jurisdiction.

The system is currently focused on the **DPDP Act 2023** legal knowledge base, while the DPIA workflow is informed by established DPIA methodology.

---

# 4. Prior-Art / Literature Findings

Existing research already contains many individual building blocks.

### Existing areas

- Structured DPIA modeling.
- Compliance automation.
- Privacy-risk scoring.
- Agent/RAG governance systems.
- Continuous monitoring.
- NLP compliance checking.
- Ontology / knowledge-graph approaches.
- Runtime privacy monitoring.

However, existing systems are often:
- document-centric,
- checklist-oriented,
- domain-specific,
- focused on one stage of the process,
- weakly connected across the complete DPIA lifecycle.

### Important research gap

The potentially interesting gap is not:

> "Nobody has used AI for DPIA."

That would be too broad and likely incorrect.

Instead, the research direction is the **combination and control of multiple mechanisms into a traceable DPIA lifecycle**, particularly:

1. Adaptive information elicitation.
2. Evidence-centric state and traceability.
3. Evidence fusion and conflict detection.
4. Structured risk and residual-risk reasoning.
5. Confidence-based human escalation.
6. Event-triggered targeted reassessment.

### Important prior-art caution

The following individual concepts already have related work:

- Adaptive questioning / active information elicitation.
- RAG for compliance.
- Knowledge graphs.
- Privacy-risk scoring.
- Human-in-the-loop compliance.
- Continuous monitoring.

Therefore, the project should **not claim any one of these components alone as novel**.

The potentially stronger contribution is the **integrated technical control mechanism** and how the components interact inside a DPIA workflow.

---

# 5. Core Research Concept

## Evidence-Grounded Adaptive DPIA

The proposed architecture can be summarized as:

```text
Project Owner
      ↓
DPIA Screening
      ↓
Adaptive Interview / Information Elicitation
      ↓
Processing Profile
      ↓
Legal Evidence + Technical Evidence + Consultation
      ↓
Evidence Fusion
      ↓
Necessity & Proportionality
      ↓
Risk Assessment
      ↓
Mitigation
      ↓
Residual Risk
      ↓
Confidence / Human Review Gate
      ↓
DPIA Report + Action Plan
      ↓
Monitoring / Change Detection
      ↓
Targeted Reassessment
```

A persistent **Evidence Graph** sits underneath the workflow and stores state and relationships.

---

# 6. Architectural Principle

The system should be a **hybrid architecture**, not an LLM-only system.

### AI / LLM responsibilities

Use AI for:
- natural-language understanding,
- extracting facts from responses/documents,
- generating adaptive questions,
- semantic retrieval,
- interpreting evidence,
- generating explanations,
- drafting report content.

### Deterministic logic responsibilities

Use deterministic logic for:
- workflow states,
- evidence IDs and relationships,
- risk calculations,
- residual-risk calculations,
- completeness checks,
- escalation thresholds,
- audit trail,
- reassessment triggers,
- state transitions.

### Human responsibilities

Human/DPO review should remain important for:
- high-risk cases,
- conflicting evidence,
- low-confidence findings,
- unresolved gaps,
- final acceptance of residual risk.

Core principle:

> **AI interprets; rules control; humans decide.**

---

# 7. Evidence Graph

The Evidence Graph is a central design decision.

It is **not being positioned simply as a generic knowledge graph**.

It is the persistent **state + traceability layer** of the DPIA.

### Core relationship

```text
Evidence
   ↓ supports / contradicts
Fact
   ↓ contributes_to
Risk Factor
   ↓ contributes_to
Risk
   ↓ addressed_by
Mitigation
   ↓ reduces
Residual Risk
```

Additional relationships:

- supports
- contradicts
- derived_from
- applies_to
- contributes_to
- violates
- addresses
- reduces
- reviewed_by
- triggered_by

### Why it matters

The evidence graph allows the system to:

- avoid duplicate findings,
- preserve provenance,
- connect findings to their sources,
- detect contradictions,
- determine confidence,
- connect risks to evidence and legal requirements,
- connect mitigations to specific risks,
- identify which DPIA components are affected by a change.

---

# 8. Central DPIA Case Representation

The system should maintain a central DPIA Case rather than disconnected dictionaries.

Conceptual structure:

```json
{
  "case_id": "DPIA-001",
  "project": {},
  "screening": {},
  "processing_profile": {},
  "consultation": {},
  "necessity_assessment": {},
  "evidence": [],
  "legal_references": [],
  "risks": [],
  "mitigations": [],
  "residual_risks": [],
  "reviews": [],
  "actions": [],
  "monitoring": {},
  "status": "IN_PROGRESS"
}
```

---

# 9. Main Technical Mechanism 1 — Adaptive Information Acquisition

The current prototype uses a fixed questionnaire.

The proposed system should instead ask:

> What information is currently missing, uncertain, or contradictory, and which next question would reduce the uncertainty most relevant to the DPIA?

### Adaptive loop

```text
Current DPIA State
       ↓
Known Information
       ↓
Missing Information
       ↓
Uncertainty / Conflicts
       ↓
Question Selection
       ↓
User Answer
       ↓
New Evidence
       ↓
Updated DPIA State
```

### Example

```json
{
  "question_id": "Q-021",
  "question": "Does the AI system make or support decisions about employees?",
  "target": "decision_making",
  "reason": "Required to assess potential impact on individuals.",
  "expected_information_gain": 0.72
}
```

After the answer:

```json
{
  "answer_id": "A-021",
  "question_id": "Q-021",
  "answer": "The model recommends candidates but a manager makes the final decision.",
  "evidence_ids": ["E-021"]
}
```

### Important research distinction

The novelty should not be claimed as:

> "We invented adaptive questioning."

Instead:

> Adaptive information elicitation is integrated into the DPIA evidence/state model so that questions are selected according to unresolved assessment requirements, uncertainty, and their impact on downstream risk reasoning.

---

# 10. Processing Profile Builder

The Processing Profile converts collected evidence into a canonical description of the processing activity.

Important fields include:

- purpose
- data subjects
- data categories
- sensitive data
- collection method
- storage
- access
- sharing
- processors
- retention
- security controls
- technology
- scale
- geography
- vulnerable groups
- individual control.

This provides the structured foundation for the rest of the DPIA.

---

# 11. Main Technical Mechanism 2 — Evidence Fusion and Risk Reasoning

Evidence can originate from:

- user responses,
- uploaded documents,
- technical configurations,
- logs,
- legal sources,
- system events,
- human reviews.

### Evidence Fusion

The engine should perform:

1. Evidence collection.
2. Fact extraction.
3. Deduplication.
4. Contradiction detection.
5. Evidence linking.
6. Confidence estimation.

Example:

```text
User response:
"Encryption is enabled."

             VS

Technical configuration:
"Encryption at rest disabled."

             ↓

       Evidence Conflict

             ↓

      Human Review Gate
```

This directly addresses the current prototype's duplicate/independent-finding problem.

---

# 12. Legal Retrieval

Current baseline:

```text
Query
  ↓
MiniLM Embedding
  ↓
FAISS
  ↓
Top-K Results
```

Proposed conceptual pipeline:

```text
DPIA Context
     ↓
Query Understanding
     ↓
Semantic Retrieval
     ↓
Metadata Filtering
     ↓
Candidate Legal Provisions
     ↓
Reranking
     ↓
Legal Evidence
```

Potential output:

```json
{
  "retrieval_id": "RET-032",
  "query": "...",
  "results": [
    {
      "source_id": "DPDP-S6",
      "section": "6",
      "topic": "Consent",
      "relevance_score": 0.91,
      "evidence": "..."
    }
  ]
}
```

Do not permanently lock the paper to MiniLM + FAISS. They are the current baseline technology choices; the research contribution is the architecture/control mechanism.

---

# 13. Necessity and Proportionality

A real DPIA should not only ask:

> "Is the system secure?"

It should also ask:

> "Is this processing necessary and proportionate for the stated purpose?"

The proposed engine considers:

- processing purpose,
- data categories,
- legal basis,
- alternatives,
- minimisation,
- retention,
- individual rights,
- applicable legal requirements.

Example output:

```json
{
  "assessment_id": "NP-001",
  "purpose_justified": true,
  "data_minimisation": {
    "status": "PARTIAL",
    "evidence_ids": ["E-012"]
  },
  "alternatives_considered": [],
  "proportionality": "REQUIRES_REVIEW",
  "gaps": [
    "Retention justification not established"
  ]
}
```

---

# 14. Risk Engine

The Risk Engine should not simply ask an LLM to produce:

> HIGH

Instead, risk should be structured around:

- scenario,
- affected individuals,
- affected data,
- potential harm,
- likelihood,
- severity,
- evidence,
- legal requirements,
- confidence.

Conceptual risk:

```text
Risk = f(Harm, Likelihood, Severity, Context, Evidence)
```

Example:

```json
{
  "risk_id": "R-001",
  "scenario": "Unauthorised disclosure of employee financial data",
  "affected_data": ["bank_account_information"],
  "affected_subjects": ["employees"],
  "harm": ["financial_loss", "loss_of_confidentiality"],
  "likelihood": 4,
  "severity": 5,
  "initial_risk": "HIGH",
  "evidence_ids": ["E-017", "TE-004"],
  "legal_reference_ids": ["DPDP-S..."],
  "confidence": 0.84
}
```

---

# 15. Mitigation and Residual Risk

Mitigations must be linked to specific risks/evidence gaps.

Example:

```json
{
  "mitigation_id": "M-001",
  "risk_id": "R-001",
  "action": "Implement role-based access control",
  "addresses": ["unauthorised_internal_access"],
  "expected_effect": "REDUCE_LIKELIHOOD",
  "evidence_gap_addressed": "TE-004",
  "priority": "HIGH"
}
```

Then calculate residual risk:

```text
Initial Risk
      ↓
Mitigation
      ↓
Expected Control Effect
      ↓
Residual Likelihood + Severity
      ↓
Residual Risk
```

Example:

```json
{
  "risk_id": "R-001",
  "initial": {
    "likelihood": 4,
    "severity": 5,
    "level": "HIGH"
  },
  "mitigations": ["M-001"],
  "residual": {
    "likelihood": 2,
    "severity": 5,
    "level": "MEDIUM"
  },
  "treatment": "REDUCED",
  "acceptance_required": true
}
```

---

# 16. Confidence-Based Human Review

The system should have explicit review states:

```text
AUTO_CONTINUE
MORE_INFORMATION_REQUIRED
REVIEW_REQUIRED
CONFLICT_REQUIRES_HUMAN
```

Potential inputs to the gate:

- evidence confidence,
- retrieval confidence,
- risk confidence,
- completeness,
- contradictions,
- risk severity.

Example:

```text
High Risk
   +
Low Confidence
   +
Conflicting Evidence
        ↓
Human Review Required
```

This is more technically meaningful than simply saying "human-in-the-loop."

---

# 17. Main Technical Mechanism 3 — Continuous Targeted Reassessment

Traditional DPIA documentation can become stale after the system changes.

The proposed system maintains a lifecycle:

```text
DPIA
 ↓
Deployment
 ↓
System / Processing Change
 ↓
Change Detection
 ↓
Impact Analysis
 ↓
Affected Risks
 ↓
Affected DPIA Sections
 ↓
Targeted Reassessment
 ↓
Updated DPIA
```

Possible change events:

- new processor,
- new data source,
- new data category,
- new technology,
- changed retention,
- changed access control,
- changed processing purpose,
- policy change.

Example:

```json
{
  "event_id": "CHG-009",
  "change_type": "new_processor",
  "affected_entities": ["third_party_processor"],
  "affected_risks": ["R-004", "R-007"],
  "reassessment_required": true
}
```

The goal is **not** to regenerate the entire DPIA every time.

Instead:

> Identify the affected graph entities and reopen only the relevant assessment components.

---

# 18. Three Feedback Loops

The complete system can be understood through three loops.

### Information Loop

```text
Evidence insufficient
       ↓
Ask question
       ↓
New evidence
       ↓
Reassess sufficiency
```

### Risk Loop

```text
Risk
 ↓
Mitigation
 ↓
Residual Risk
 ↓
Human Decision
```

### Lifecycle Loop

```text
DPIA
 ↓
Deployment
 ↓
Change
 ↓
Affected Assessment
 ↓
Reassessment
 ↓
Updated DPIA
```

These three loops are a useful way to explain the architecture concisely.

---

# 19. Research Hypothesis

Tentative hypothesis:

> Whether an evidence-centric graph representation combined with adaptive evidence acquisition can improve the completeness, traceability, consistency, and maintainability of AI-assisted DPIA assessments compared with a conventional sequential RAG-based DPIA workflow.

This is a working hypothesis and should be refined after the final experimental design.

---

# 20. Research Paper

## Target length

The paper should be **less than 6 pages**, ideally around **5–5.5 pages including references**, using the target IEEE conference format.

The paper should NOT become a module-by-module system documentation report.

Do not give every agent a separate major section.

Instead, organize the paper around the three technical mechanisms:

1. **Adaptive Evidence Acquisition**
2. **Evidence-Centric Risk Reasoning**
3. **Continuous Targeted Reassessment**

Agents are implementation mechanisms supporting these ideas.

---

# 21. Recommended Paper Skeleton

## Title

Current preferred working title:

> **An Evidence-Centric Architecture for Adaptive and Continuous Data Protection Impact Assessment**

Other possible titles:

- An Evidence-Grounded Agentic Framework for Adaptive Data Protection Impact Assessment
- Adaptive Evidence Acquisition and Risk Reasoning for Data Protection Impact Assessment
- Evidence Fusion and Adaptive Risk Reasoning for Agentic Data Protection Impact Assessment
- A Hybrid Agentic Framework for Evidence-Grounded Data Protection Impact Assessment

The final title should be selected after the architecture and novelty claims are finalized.

---

## Abstract

The abstract should establish:

1. DPIA problem.
2. Limitations of existing static/document-centric approaches.
3. Proposed evidence-grounded adaptive architecture.
4. Evidence graph.
5. Adaptive questioning.
6. Evidence fusion and structured risk reasoning.
7. Human review.
8. Continuous targeted reassessment.
9. Evaluation against a conventional RAG baseline.

Working abstract:

> Data Protection Impact Assessments (DPIAs) are an important mechanism for identifying and mitigating privacy risks associated with personal-data processing, but conventional DPIA processes remain largely dependent on manual information gathering, expert assessment, and static documentation. Existing AI-assisted approaches have explored individual capabilities such as legal retrieval, privacy-risk scoring, compliance checking, and automated documentation, but there remains a need for an integrated approach that can dynamically acquire missing information, maintain traceable evidence, and continuously update privacy-risk assessments as processing environments evolve.
>
> This paper proposes an evidence-grounded adaptive DPIA framework that combines agentic information elicitation, machine-readable legal knowledge, retrieval-augmented legal analysis, structured privacy-risk reasoning, mitigation recommendation, human oversight, and event-triggered reassessment. The proposed architecture maintains an explicit evidence graph linking user-provided information, processing facts, risk factors, applicable legal requirements, identified risks, mitigation measures, residual risks, and human decisions. An adaptive interview agent identifies information gaps and selects targeted follow-up questions based on assessment uncertainty, while the evidence fusion layer detects supporting and conflicting evidence before risk assessment. A hybrid risk engine then evaluates potential harms using structured likelihood and severity factors rather than relying solely on generative model outputs. Mitigation measures are subsequently evaluated to determine residual risk, with confidence-based human review applied to uncertain or conflicting assessments. Finally, changes in processing conditions can trigger targeted reassessment of affected portions of the DPIA rather than requiring the entire assessment to be repeated.
>
> The proposed framework aims to move DPIA automation from a document-centric and static workflow toward an evidence-centric, traceable, and continuously maintainable assessment process. The system will be evaluated against a conventional RAG-based DPIA baseline using measures including information completeness, retrieval effectiveness, risk-assessment consistency, evidence traceability, mitigation relevance, and reassessment efficiency.

---

# 22. Index Terms

Recommended concise version:

> **Index Terms—** Data Protection Impact Assessment (DPIA), Agentic AI, Evidence Graph, Privacy Risk Assessment, Adaptive Information Elicitation, Risk Reasoning, Continuous Reassessment.

---

# 23. Paper Structure for <6 Pages

## I. Introduction — ~0.6 page

Include:
- background,
- problem,
- research gap,
- proposed approach,
- 3–4 contributions.

Do not spend excessive space on DPIA background.

---

## II. Related Work and Research Gap — ~0.8 page

Group literature into:

### A. Automated/AI-Assisted DPIA and Privacy Compliance

### B. Agentic/RAG-Based Compliance Systems

### C. Privacy Risk Assessment and Evidence-Based Reasoning

### D. Continuous/Adaptive Assessment

Use one compact comparison table.

End with the exact research gap.

---

## III. Proposed Framework — ~1.5 pages

### A. System Architecture

One major architecture figure.

### B. Evidence-Centric DPIA Representation

Explain the evidence graph and core entities.

### C. Adaptive Assessment and Risk Reasoning

Combine:
- adaptive information acquisition,
- evidence fusion,
- necessity/proportionality,
- risk reasoning,
- mitigation/residual risk.

Do not provide huge JSON schemas in the paper.

---

## IV. Human-Guided and Continuous DPIA — ~0.7 page

### A. Confidence-Based Human Review

### B. Change-Triggered Targeted Reassessment

Combine these to save space.

---

## V. Implementation and Experimental Methodology — ~0.8 page

### A. Prototype Implementation

Briefly state technologies.

### B. Evaluation Setup

Compare:

**Baseline:** conventional sequential RAG-based DPIA workflow.

**Proposed:** evidence-centric adaptive DPIA.

### C. Metrics

Potential metrics:

- information completeness,
- legal retrieval effectiveness,
- evidence traceability,
- duplicate finding rate,
- risk-assessment consistency,
- mitigation relevance,
- human escalation quality,
- reassessment efficiency.

---

## VI. Results and Discussion — ~0.7 page

Include:
- quantitative results,
- qualitative case,
- failure cases,
- ablation study if possible.

Potential ablation:

```text
Baseline
   ↓
+ Evidence Graph
   ↓
+ Adaptive Interview
   ↓
+ Evidence Fusion
   ↓
+ Continuous Reassessment
```

---

## VII. Limitations and Conclusion — ~0.4 page

Limitations:
- evaluation dataset size,
- knowledge-base quality,
- human validation,
- limited real-world deployment.

Then concise conclusion and future work.

---

# 24. Page Budget

| Section | Target |
|---|---:|
| Introduction | ~0.6 |
| Related Work & Gap | ~0.8 |
| Proposed Framework | ~1.5 |
| Human + Continuous DPIA | ~0.7 |
| Implementation & Evaluation | ~0.8 |
| Results & Discussion | ~0.7 |
| Limitations & Conclusion | ~0.4 |
| References | ~0.5–0.8 |
| **Total** | **~5.5–6 pages** |

---

# 25. Important Writing Strategy

The paper should tell this story:

```text
Problem
  ↓
Existing approaches are fragmented/static
  ↓
Research gap
  ↓
Evidence-centric adaptive architecture
  ↓
Adaptive evidence acquisition
  ↓
Evidence-grounded risk reasoning
  ↓
Human-controlled decisions
  ↓
Continuous targeted reassessment
  ↓
Experimental evaluation
```

Do NOT make the paper's central story:

```text
Agent 1
Agent 2
Agent 3
Agent 4
Agent 5
...
```

That would make it look like an implementation report.

---

# 26. Evaluation Strategy

The evaluation is essential because the paper should demonstrate more than architectural novelty.

### Baseline

A conventional sequential RAG-based DPIA assistant similar to the current prototype:

```text
Fixed Interview
   ↓
RAG
   ↓
Risk Scoring
   ↓
Report
```

### Proposed

```text
Adaptive Interview
   ↓
Evidence Graph
   ↓
Evidence Fusion
   ↓
Structured Risk Reasoning
   ↓
Human Gate
   ↓
Targeted Reassessment
```

### Core evaluation questions

1. Does adaptive questioning reduce missing information?
2. Does evidence fusion reduce duplicate/inconsistent findings?
3. Does evidence grounding improve risk traceability?
4. Does structured risk reasoning improve consistency?
5. Does targeted reassessment reduce unnecessary reassessment work?
6. Does the confidence gate identify cases requiring human review?

---

# 27. Potential Ablation Study

A strong experiment can progressively add mechanisms:

```text
Model 0: Conventional RAG DPIA
Model 1: + Evidence Graph
Model 2: + Adaptive Information Acquisition
Model 3: + Evidence Fusion
Model 4: + Continuous Targeted Reassessment
```

Measure the relevant metrics after each addition.

This helps demonstrate that the contribution comes from the architecture rather than simply using a stronger LLM.

---

# 28. Security Considerations

Because this is also a cybersecurity-oriented system, consider:

- prompt injection through uploaded documents,
- malicious evidence,
- poisoned legal knowledge,
- hallucinated legal claims,
- evidence manipulation,
- unauthorized access to DPIA information,
- audit-log integrity,
- model output validation.

The DPIA system itself processes potentially sensitive information, so the system should also consider:

- access control,
- data minimisation,
- secure storage,
- audit logging.

---

# 29. Patent Direction

The patent should NOT simply claim:

> "An AI system that automates DPIAs."

That is too broad and likely crowded.

A stronger direction is to focus on a concrete technical mechanism such as:

> A computer-implemented method for maintaining an evidence-linked DPIA state in which unresolved information gaps dynamically trigger targeted evidence acquisition, evidence conflicts and confidence levels control risk-assessment/human-review states, and processing-change events selectively reopen affected assessment components.

Potential claim building blocks:

1. Central evidence-linked DPIA state.
2. Evidence → fact → risk relationship model.
3. Adaptive question selection based on unresolved DPIA requirements/uncertainty.
4. Evidence conflict detection.
5. Confidence-based review gating.
6. Risk → mitigation → residual-risk linkage.
7. Change-event → affected-risk mapping.
8. Targeted reassessment rather than full DPIA regeneration.

A dedicated patent prior-art search is still required before making a novelty claim.

---

# 30. Important Distinctions to Preserve

Throughout the research paper and patent, clearly distinguish:

### Already implemented
- fixed interview,
- JSON legal knowledge base,
- MiniLM + FAISS retrieval,
- basic rule-based risk scoring,
- deterministic report generation,
- end-to-end prototype.

### Proposed architecture
- adaptive questioning,
- evidence graph,
- evidence fusion,
- contradiction detection,
- structured risk reasoning,
- confidence gate,
- continuous targeted reassessment.

### Future / experimental
- richer technical evidence collection,
- improved reranking,
- full LLM drafting,
- large-scale evaluation,
- additional jurisdictions.

Do not write proposed functionality as though it has already been implemented.

---

# 31. Core One-Paragraph Explanation

If the project needs to be explained quickly elsewhere:

> We are developing an evidence-centric agentic DPIA system that moves beyond fixed questionnaires and static report generation. The system maintains a persistent evidence graph linking user responses, documents, technical evidence, processing facts, legal requirements, risks, mitigations, residual risks, and human decisions. An adaptive interview mechanism identifies missing or uncertain information and selects targeted questions, while evidence fusion detects duplicate and conflicting findings. A hybrid risk engine combines AI-based interpretation with deterministic risk and residual-risk reasoning, and a confidence-based gate routes uncertain or high-risk cases to human review. Finally, processing changes can trigger targeted reassessment of only the affected DPIA components. The research evaluates whether this architecture improves information completeness, traceability, risk consistency, and reassessment efficiency compared with a conventional sequential RAG-based DPIA workflow.

---

# 32. Current Research Position

The project should be presented as:

> **A proposed evidence-centric adaptive architecture for agentic DPIA automation, supported by a functional baseline prototype and to be validated experimentally.**

Do not currently claim:

- that the architecture is proven superior,
- that the mechanism is definitely novel,
- that the patent is definitely novel,
- that adaptive questioning itself is novel,
- that evidence graphs themselves are novel.

Those claims require experimental evidence and dedicated prior-art/patent searching.

---

# 33. Immediate Next Steps

Recommended order of work:

1. **Freeze the architecture.**
2. Define the exact evidence graph schema.
3. Define module input/output interfaces.
4. Decide which proposed mechanisms will actually be implemented within the project timeline.
5. Define baseline vs proposed system.
6. Design evaluation dataset/cases.
7. Define metrics.
8. Conduct deeper academic and patent prior-art analysis.
9. Write the research paper around the three core mechanisms.
10. Draft patent claims around the concrete control mechanism rather than generic "AI DPIA."

## Core message to preserve

> **The contribution is not "AI for DPIA."**
>
> The contribution is a **closed-loop, evidence-centric DPIA architecture** in which the system can identify what it does not know, acquire the missing evidence, reason over linked evidence and risks, escalate uncertain decisions to humans, and selectively reassess the DPIA when the underlying processing environment changes.
