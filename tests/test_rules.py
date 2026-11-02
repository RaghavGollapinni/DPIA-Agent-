import pytest

from agents.finding import Finding
from agents.profile import AssessmentProfile
from agents.scoring import RiskScoringAgent


def profile(**changes):
    """A well-run case. Every field is marked as asked. Tests change one fact at a time."""
    base = dict(
        is_sdf=False, large_scale=False, sensitive_data=False, children=False,
        processing_purpose="Salary payment", data_categories=["name"], data_principals=["employees"],
        data_all_necessary=True, notice_given=True, consent_obtained=True,
        consent_withdrawal_supported=True, third_party_sharing=False, retention_defined=True,
        cross_border_transfer=False, encryption=True, access_controls=True, breach_process=True,
        grievance_mechanism=True, rights_process=True,
    )
    base.update(changes)
    return AssessmentProfile(asked_fields=list(base), **base)


def rule_ids(p):
    return [f.rule_id for f in RiskScoringAgent().assess(p)]


def test_well_run_case_has_no_findings():
    assert rule_ids(profile()) == []


@pytest.mark.parametrize("field,rule", [
    ("notice_given", "N1"), ("data_all_necessary", "N5"), ("retention_defined", "N7"),
    ("encryption", "S1"), ("access_controls", "S2"), ("breach_process", "S3"),
    ("grievance_mechanism", "G1"), ("rights_process", "R1"),
])
def test_clear_no_fires_the_rule(field, rule):
    assert rule_ids(profile(**{field: False})) == [rule]


@pytest.mark.parametrize("field", [
    "notice_given", "data_all_necessary", "retention_defined", "encryption", "access_controls",
    "breach_process", "grievance_mechanism", "rights_process",
])
def test_unknown_never_fires_and_is_an_open_question(field):
    p = profile(**{field: None})
    assert rule_ids(p) == []
    assert field in RiskScoringAgent().open_questions(p)


def test_no_consent_and_no_basis_is_n2_not_n3():
    assert rule_ids(profile(consent_obtained=False, other_legal_basis=None)) == ["N2"]
    assert rule_ids(profile(consent_obtained=False, other_legal_basis="")) == ["N2"]


def test_no_consent_with_basis_is_n3_not_n2():
    assert rule_ids(profile(consent_obtained=False, other_legal_basis="employment")) == ["N3"]


def test_withdrawal_needs_consent_to_be_true():
    assert rule_ids(profile(consent_withdrawal_supported=False)) == ["N4"]
    assert rule_ids(profile(consent_obtained=None, consent_withdrawal_supported=False)) == []
    assert rule_ids(profile(consent_obtained=False, other_legal_basis="x", consent_withdrawal_supported=False)) == ["N3"]


def test_processor_contract_rule():
    assert rule_ids(profile(third_party_sharing=True, third_party_contract=False)) == ["T1"]
    p = profile(third_party_sharing=True, third_party_contract=None)
    assert rule_ids(p) == []
    assert "third_party_contract" in RiskScoringAgent().open_questions(p)
    assert rule_ids(profile(third_party_sharing=False, third_party_contract=False)) == []


def test_children_rule():
    assert rule_ids(profile(children=True, parental_consent=False)) == ["C1"]
    assert rule_ids(profile(children=True, parental_consent=None)) == []


def test_confirm_items_have_low_likelihood():
    cross = [f for f in RiskScoringAgent().assess(profile(cross_border_transfer=True)) if f.rule_id == "X1"][0]
    sdf = [f for f in RiskScoringAgent().assess(profile(is_sdf=True)) if f.rule_id == "D1"][0]
    assert cross.likelihood == 2 and sdf.likelihood == 2


def test_context_uplift_is_plus_one_at_most():
    none = RiskScoringAgent().assess(profile(notice_given=False))[0]
    one = RiskScoringAgent().assess(profile(notice_given=False, sensitive_data=True))[0]
    three = RiskScoringAgent().assess(profile(notice_given=False, sensitive_data=True, children=True, large_scale=True))[0]
    assert (none.impact, one.impact, three.impact) == (2, 3, 3)


def test_unknown_context_flag_is_assumed_yes_and_explained():
    f = RiskScoringAgent().assess(profile(notice_given=False, large_scale=None))[0]
    assert f.impact == 3
    assert any("unknown, assumed yes" in note for note in f.notes)


def test_impact_is_capped_at_five():
    f = RiskScoringAgent().assess(profile(consent_obtained=False, sensitive_data=True))[0]   # base 4 +1
    assert f.rule_id == "N2" and f.impact == 5 and f.score == 25 and f.level == "Critical"


def test_findings_are_sorted_with_ids():
    findings = RiskScoringAgent().assess(profile(notice_given=False, encryption=False, grievance_mechanism=False))
    assert [f.id for f in findings] == ["F-01", "F-02", "F-03"]
    assert [f.score for f in findings] == sorted([f.score for f in findings], reverse=True)


def test_every_finding_explains_itself():
    for f in RiskScoringAgent().assess(profile(notice_given=False, encryption=False)):
        assert f.facts and f.notes and f.expected_chunk_ids and f.recommendation


def test_finding_rejects_bad_scores():
    base = dict(rule_id="X", category="c", cause="c", title="t", observed_practice="o",
                potential_risk="r", recommendation="a")
    for bad in (0, 6, 2.5, True, "3"):
        with pytest.raises(ValueError):
            Finding(likelihood=bad, impact=3, **base)
    assert Finding(likelihood=4, impact=4, **base).level == "High"
