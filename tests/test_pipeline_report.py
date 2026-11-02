from docx import Document

from agents.interviewer import InterviewAgent
from agents.pipeline import assess_profile
from agents.report import ReportAgent
from agents.retrieval import RetrievalAgent
from demo_answers import make_ask


def demo(embedder, with_evidence=True):
    profile = InterviewAgent().run(ask=make_ask(show=False), say=lambda *a, **k: None)
    retriever = RetrievalAgent(embedder=embedder) if with_evidence else None
    findings, open_questions = assess_profile(profile, retriever)
    return profile, findings, open_questions


def test_demo_findings_and_scores(embedder):
    _, findings, open_questions = demo(embedder)
    assert [f.rule_id for f in findings] == ["S3", "N5", "N7", "R1", "N1", "G1", "N3"]
    assert [f.id for f in findings] == [f"F-0{i}" for i in range(1, 8)]
    assert [f.score for f in findings] == [20, 16, 16, 16, 12, 12, 6]
    assert open_questions == ["third_party_contract"]          # unknown contract: no finding, one open question


def test_every_finding_is_complete(embedder):
    _, findings, _ = demo(embedder)
    for f in findings:
        assert len(f.evidence) == 3 and f.draft["action"] and f.draft["law"].startswith("DPDP Act s.")
        assert f.treatment["residual_score"] <= f.score


def test_grc_gate_in_the_demo(embedder):
    _, findings, _ = demo(embedder)
    breach = findings[0]
    assert (breach.score, breach.level) == (20, "Critical")
    assert (breach.treatment["residual_score"], breach.treatment["residual_level"]) == (10, "High")
    assert breach.treatment["escalate"] is True and breach.treatment["approver"] == "Senior management"
    assert [f.id for f in findings if f.treatment["escalate"]] == ["F-01"]
    assert findings[-1].treatment["owner_can_accept"] is True        # N3: 6 -> 3


def test_report_is_written_and_complete(embedder, tmp_path):
    profile, findings, open_questions = demo(embedder)
    path = ReportAgent().generate(profile, findings, open_questions, filename=str(tmp_path / "out" / "r.docx"))
    doc = Document(path)
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    for title in ("1. Executive summary", "5. Risk register", "6. Recommendations and residual risk",
                  "7. Legal evidence for each finding", "8. Open questions (not assessed)",
                  "9. Review and sign-off", "10. Method and limits"):
        assert title in headings, title
    table_text = " ".join(c.text for t in doc.tables for row in t.rows for c in row.cells)
    for f in findings:
        assert f.id in table_text and f.title in table_text
    assert "Escalate - owner cannot accept" in table_text and "Senior management" in table_text
    assert "third party contract" in " ".join(p.text for p in doc.paragraphs)
    assert "own rubric" in " ".join(p.text for p in doc.paragraphs)


def test_report_works_without_legal_evidence(embedder, tmp_path):
    profile, findings, open_questions = demo(embedder, with_evidence=False)
    assert all(f.evidence == [] and f.draft["law"] is None for f in findings)
    path = ReportAgent().generate(profile, findings, open_questions, filename=str(tmp_path / "r.docx"))
    assert "No legal text was retrieved" in " ".join(p.text for p in Document(path).paragraphs)


def test_report_with_no_findings(embedder, tmp_path):
    profile, findings, _ = demo(embedder)
    ReportAgent().generate(profile, [], [], filename=str(tmp_path / "empty.docx"))
