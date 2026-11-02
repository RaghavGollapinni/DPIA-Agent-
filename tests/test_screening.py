from agents.screening import parse_yes_no, decide, run_screening, QUESTIONS


def all_no(**changes):
    base = {f: False for f in QUESTIONS}
    base.update(changes)
    return base


def test_parse_yes():
    assert parse_yes_no("Yes") is True
    assert parse_yes_no("yes, about 50,000 users") is True
    assert parse_yes_no("  Y ") is True


def test_parse_no():
    assert parse_yes_no("No") is False
    assert parse_yes_no("no, never") is False
    assert parse_yes_no("NOPE") is False


def test_parse_unknown():
    # The old bug: "no" is inside "know" and "not". These must be unknown.
    assert parse_yes_no("I do not know") is None
    assert parse_yes_no("not sure") is None
    assert parse_yes_no("no idea") is None
    assert parse_yes_no("don't know") is None
    assert parse_yes_no("") is None
    assert parse_yes_no(None) is None


def test_sdf_required():
    assert decide(all_no(is_sdf=True))["outcome"] == "Required"


def test_sdf_required_even_with_other_unknowns():
    r = decide(all_no(is_sdf=True, large_scale=None))
    assert r["outcome"] == "Required"
    assert "large_scale" in r["unknowns"]


def test_recommended_when_one_trigger():
    r = decide(all_no(sensitive_data=True))
    assert r["outcome"] == "Recommended"
    assert any("financial, health or biometric" in x for x in r["reasons"])


def test_unknown_is_flagged_not_assumed_no():
    r = decide(all_no(large_scale=None))
    assert r["outcome"] == "Recommended"
    assert r["unknowns"] == ["large_scale"]


def test_unknown_sdf_status_is_not_required():
    # We cannot claim "Required" when SDF status is unknown. We flag it instead.
    r = decide(all_no(is_sdf=None))
    assert r["outcome"] == "Recommended"
    assert r["unknowns"] == ["is_sdf"]


def test_optional_when_all_no():
    r = decide(all_no())
    assert r["outcome"] == "Optional"
    assert r["unknowns"] == []


def test_missing_field_counts_as_unknown():
    r = decide({"is_sdf": False})
    assert set(r["unknowns"]) == {"large_scale", "sensitive_data", "children"}


def test_run_screening_with_fake_answers():
    fake = iter(["No", "yes, 2 lakh employees", "Yes, bank details", "no"])
    r = run_screening(ask=lambda prompt: next(fake))
    assert r["outcome"] == "Recommended"
    assert r["answers"] == {
        "is_sdf": False, "large_scale": True, "sensitive_data": True, "children": False,
    }
