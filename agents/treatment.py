"""Stage 6 - Risk treatment (the GRC part).

Three GRC ideas live here:
  1. INHERENT risk   = score for the practice as reported (before the recommended control).
  2. RESIDUAL risk   = projected score AFTER the recommended control is applied.
  3. RISK APPETITE   = the highest residual score the project owner may accept alone.
                       Above it, a more senior person must decide.

Every number below is OUR rubric. It is not a DPDP Act rule. The README must say so.
"""

from agents.finding import BANDS, level_for      # one set of bands for the whole project

# Risk appetite: a residual score at or above this cannot be accepted by the project owner.
APPETITE_THRESHOLD = 10

# Assumption: one recommended control lowers LIKELIHOOD by this many points.
# Impact does not change, because the same data is still at stake.
CONTROL_LIKELIHOOD_REDUCTION = 2

# Who may accept the remaining (residual) risk.
APPROVER_BY_LEVEL = {
    "Low": "Project owner",
    "Medium": "Privacy lead / DPO",
    "High": "Senior management",
    "Critical": "Senior management",
}


def _check(value, name):
    if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
        raise ValueError(f"{name} must be a whole number from 1 to 5, got {value!r}")


def score(likelihood, impact):
    _check(likelihood, "likelihood")
    _check(impact, "impact")
    return likelihood * impact


def level(value):
    return level_for(value)


def treat(likelihood, impact, control_applied=True):
    """Work out inherent risk, residual risk, treatment and approver.

    Returns a dict that the report can print as one row of the risk register.
    """
    inherent = score(likelihood, impact)
    inherent_level = level(inherent)

    residual_likelihood = (
        max(1, likelihood - CONTROL_LIKELIHOOD_REDUCTION) if control_applied else likelihood
    )
    residual = score(residual_likelihood, impact)
    residual_level = level(residual)

    # Treatment: a Low risk may be accepted as it is. Anything higher needs a control.
    treatment = "Accept" if inherent_level == "Low" else "Mitigate"
    owner_can_accept = residual < APPETITE_THRESHOLD
    escalate = not owner_can_accept

    if treatment == "Accept":
        note = "Low risk. Accept and monitor."
    elif escalate:
        note = (
            f"Residual score {residual} is at or above the appetite threshold "
            f"({APPETITE_THRESHOLD}). The project owner cannot accept it. Escalate."
        )
    else:
        note = f"Residual score {residual} is below the appetite threshold ({APPETITE_THRESHOLD})."

    return {
        "inherent_score": inherent,
        "inherent_level": inherent_level,
        "residual_score": residual,
        "residual_level": residual_level,
        "treatment": treatment,
        "owner_can_accept": owner_can_accept,
        "escalate": escalate,
        "approver": APPROVER_BY_LEVEL[residual_level],
        "note": note,
    }


def treat_finding(finding, control_applied=True):
    """Compute the treatment for a Finding and store it on the finding."""
    finding.treatment = treat(finding.likelihood, finding.impact, control_applied)
    return finding.treatment
