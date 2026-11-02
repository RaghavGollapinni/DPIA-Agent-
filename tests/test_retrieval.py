import pytest

import agents.retrieval as retrieval
from agents.finding import Finding
from agents.retrieval import RetrievalAgent, strength


@pytest.fixture(params=["numpy", "faiss"])
def agent(request, embedder, monkeypatch):
    if request.param == "numpy":
        monkeypatch.setattr(retrieval, "faiss", None)
    elif retrieval.faiss is None:
        pytest.skip("faiss is not installed")
    return RetrievalAgent(embedder=embedder)


def test_returns_top_k_sorted_with_metadata(agent):
    results = agent.retrieve("notice about what data is collected and why", top_k=3)
    assert len(results) == 3
    assert [r["rank"] for r in results] == [1, 2, 3]
    sims = [r["similarity"] for r in results]
    assert sims == sorted(sims, reverse=True)
    assert all(-1.0001 <= s <= 1.0001 for s in sims)
    assert all(r["section"] and r["title"] and r["source"] for r in results)


def test_a_chunk_finds_itself_first(agent):
    for chunk in agent.corpus:
        top = agent.retrieve(RetrievalAgent._doc_text(chunk), top_k=1)[0]
        assert top["id"] == chunk["id"] and top["similarity"] > 0.99


def test_attach_evidence_fills_the_finding(agent):
    f = Finding(rule_id="S1", category="Security", cause="no-encryption", title="t",
                observed_practice="Stored personal data is not encrypted.", potential_risk="Data can be read if stolen.",
                recommendation="Encrypt", likelihood=4, impact=4)
    evidence = agent.attach_evidence(f, top_k=3)
    assert evidence is f.evidence and len(evidence) == 3
    for e in evidence:
        assert {"chunk_id", "section", "title", "text", "similarity", "rank", "strength"} <= set(e)


def test_top_k_is_capped_by_corpus_size(agent):
    assert len(agent.retrieve("anything", top_k=500)) == len(agent.corpus)


def test_strength_labels():
    assert strength(0.9) == "Strong" and strength(0.4) == "Moderate" and strength(0.1) == "Weak"


def test_faiss_and_numpy_agree(embedder, monkeypatch):
    if retrieval.faiss is None:
        pytest.skip("faiss is not installed")
    with_faiss = RetrievalAgent(embedder=embedder).retrieve("breach notification", top_k=5)
    monkeypatch.setattr(retrieval, "faiss", None)
    without = RetrievalAgent(embedder=embedder).retrieve("breach notification", top_k=5)
    assert [r["id"] for r in with_faiss] == [r["id"] for r in without]
