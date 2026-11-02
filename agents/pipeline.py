"""Runs stages 3 to 6 on a finished profile. app.py and the tests both call this."""
from agents.consolidator import consolidate
from agents.drafting import DraftingAgent
from agents.scoring import RiskScoringAgent
from agents.treatment import treat_finding


def assess_profile(profile, retriever=None, top_k=3):
    """Return (findings, open_questions).

    retriever: a RetrievalAgent, or None to skip legal evidence.
    """
    scoring = RiskScoringAgent()
    findings = consolidate(scoring.assess(profile))     # Stage 3-4: rules, then merge
    drafter = DraftingAgent()
    for finding in findings:
        if retriever is not None:
            retriever.attach_evidence(finding, top_k=top_k)   # Stage 5: legal evidence
        drafter.draft(finding)                                # Stage 6: draft text
        treat_finding(finding)                                # Stage 6: residual risk (GRC)
    return findings, scoring.open_questions(profile)
