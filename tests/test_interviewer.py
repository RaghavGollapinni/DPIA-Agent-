from agents.interviewer import InterviewAgent, parse_list, parse_text
from demo_answers import DEMO_ANSWERS, make_ask


def run(**overrides):
    answers = dict(DEMO_ANSWERS)
    answers.update(overrides)
    return InterviewAgent().run(ask=make_ask(answers, show=False), say=lambda *a, **k: None)


def test_parse_text():
    for blank in ["", "  ", "none", "No", "nothing", "N/A", "not sure", "I don't know", "no idea"]:
        assert parse_text(blank) is None, blank
    assert parse_text("  legal obligation ") == "legal obligation"


def test_parse_list():
    assert parse_list("name, phone; email\nsalary") == ["name", "phone", "email", "salary"]
    assert parse_list("not sure") == []


def test_demo_case_is_filled_correctly():
    p = run()
    assert p.screening_outcome == "Recommended"
    assert p.large_scale is True and p.sensitive_data is True and p.is_sdf is False
    assert p.data_categories[0] == "name" and len(p.data_categories) == 6
    assert p.consent_obtained is False and p.other_legal_basis == "employment"
    assert p.third_party_sharing is True and p.third_party_contract is None


def test_conditional_questions_are_skipped_not_unknown():
    p = run()
    for skipped in ("consent_withdrawal_supported", "retention_period", "parental_consent"):
        assert skipped not in p.asked_fields
        assert skipped not in p.unknown_fields()
    assert p.unknown_fields() == ["third_party_contract"]


def test_conditions_open_when_relevant():
    p = run(**{"obtain consent before": "Yes", "children's personal data": "Yes"})
    assert "consent_withdrawal_supported" in p.asked_fields
    assert "other_legal_basis" not in p.asked_fields
    assert "parental_consent" in p.asked_fields
    p = run(**{"obtain consent before": "not sure"})            # unknown consent still asks about withdrawal
    assert "consent_withdrawal_supported" in p.asked_fields


def test_every_typed_answer_is_recorded():
    p = run()
    assert len(p.raw_answers) == len(p.asked_fields) == 20
    assert p.raw_answers[0]["answer"] == "No, I think not"
