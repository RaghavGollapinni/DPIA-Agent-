import pytest
from agents.treatment import score, level, treat, APPETITE_THRESHOLD


def test_score_is_likelihood_times_impact():
    assert score(4, 5) == 20
    assert score(1, 1) == 1


def test_level_band_edges():
    assert level(4) == "Low"
    assert level(5) == "Medium"
    assert level(9) == "Medium"
    assert level(10) == "High"
    assert level(16) == "High"
    assert level(17) == "Critical"
    assert level(25) == "Critical"


def test_unencrypted_bank_details_still_needs_escalation():
    # Likelihood 4, impact 5 -> 20 Critical. After control: 2 x 5 = 10 High.
    r = treat(4, 5)
    assert (r["inherent_score"], r["inherent_level"]) == (20, "Critical")
    assert (r["residual_score"], r["residual_level"]) == (10, "High")
    assert r["escalate"] is True
    assert r["owner_can_accept"] is False
    assert r["approver"] == "Senior management"


def test_consent_withdrawal_can_be_handled_by_dpo():
    # 4 x 3 = 12 High. After control: 2 x 3 = 6 Medium.
    r = treat(4, 3)
    assert (r["inherent_score"], r["inherent_level"]) == (12, "High")
    assert (r["residual_score"], r["residual_level"]) == (6, "Medium")
    assert r["escalate"] is False
    assert r["treatment"] == "Mitigate"
    assert r["approver"] == "Privacy lead / DPO"


def test_low_risk_is_accepted():
    r = treat(1, 2)
    assert r["treatment"] == "Accept"
    assert r["residual_score"] == 2
    assert r["approver"] == "Project owner"
    assert r["owner_can_accept"] is True


def test_likelihood_never_drops_below_one():
    assert treat(2, 3)["residual_score"] == 3   # 1 x 3
    assert treat(1, 3)["residual_score"] == 3   # stays 1 x 3


def test_residual_never_exceeds_inherent():
    for l in range(1, 6):
        for i in range(1, 6):
            r = treat(l, i)
            assert r["residual_score"] <= r["inherent_score"]


def test_no_control_means_no_change():
    r = treat(4, 5, control_applied=False)
    assert r["residual_score"] == r["inherent_score"] == 20
    assert r["escalate"] is True


def test_appetite_threshold_edge():
    # 5 x 2 = 10 inherent, residual 3 x 2 = 6 -> owner may not need to escalate.
    assert treat(5, 2)["escalate"] is False
    # Residual of exactly the threshold must escalate (2 x 5 = 10).
    assert treat(4, 5)["residual_score"] == APPETITE_THRESHOLD
    assert treat(4, 5)["escalate"] is True


def test_invalid_inputs_are_rejected():
    for bad in [(0, 3), (6, 3), (3, 0), (3, 6), (2.5, 3), ("4", 3), (True, 3)]:
        with pytest.raises(ValueError):
            treat(*bad)
