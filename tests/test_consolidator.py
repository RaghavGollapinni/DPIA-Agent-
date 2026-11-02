from agents.consolidator import consolidate, group_by_category
from agents.finding import Finding


def finding(rule, category, cause, likelihood=4, impact=3, facts=None, chunks=None):
    return Finding(rule_id=rule, category=category, cause=cause, title=rule, observed_practice="o",
                   potential_risk="r", recommendation="a", likelihood=likelihood, impact=impact,
                   facts=facts or {}, expected_chunk_ids=chunks or [])


def test_same_category_and_cause_are_merged_keeping_the_worst():
    a = finding("A", "Consent", "no-withdrawal", 3, 3, {"x": 1}, [3])
    b = finding("B", "Consent", "no-withdrawal", 5, 4, {"y": 2}, [3, 2])
    out = consolidate([a, b])
    assert len(out) == 1 and out[0].rule_id == "B" and out[0].score == 20
    assert out[0].facts == {"y": 2, "x": 1} and out[0].expected_chunk_ids == [3, 2]
    assert "Merged 1 duplicate" in out[0].notes[-1]


def test_same_category_different_cause_stays_separate():
    out = consolidate([finding("A", "Consent", "no-withdrawal"), finding("B", "Consent", "over-collection")])
    assert len(out) == 2


def test_six_consent_findings_cannot_come_back():
    six = [finding(f"R{i}", "Consent", "no-withdrawal") for i in range(6)]
    assert len(consolidate(six)) == 1


def test_sorted_and_ids_reassigned():
    out = consolidate([finding("L", "A", "a", 1, 1), finding("H", "B", "b", 5, 5), finding("M", "C", "c", 3, 3)])
    assert [(f.id, f.rule_id) for f in out] == [("F-01", "H"), ("F-02", "M"), ("F-03", "L")]


def test_group_by_category_keeps_severity_order():
    out = consolidate([finding("A", "Security", "s1", 2, 2), finding("B", "Consent", "c1", 5, 5),
                       finding("C", "Security", "s2", 4, 4)])
    groups = group_by_category(out)
    assert list(groups) == ["Consent", "Security"]
    assert [f.rule_id for f in groups["Security"]] == ["C", "A"]
