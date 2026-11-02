"""Stage 1 - Screening.

Real-DPIA question answered here: "Do we need a DPIA at all?"
Four yes/no questions decide the outcome: Required, Recommended or Optional.
"""
import re

QUESTIONS = {
    "is_sdf": "Is your organisation a Significant Data Fiduciary?",
    "large_scale": "Do you process the data of a large number of people?",
    "sensitive_data": "Do you process financial, health or biometric data?",
    "children": "Do you process children's personal data?",
}

# Text shown in the report when a screening field is "yes".
YES_REASONS = {
    "is_sdf": "Organisation is a Significant Data Fiduciary (DPDP Act s.10 requires a DPIA).",
    "large_scale": "Processing is large scale.",
    "sensitive_data": "Processing includes financial, health or biometric data.",
    "children": "Processing includes children's data (DPDP Act s.9).",
}

YES_WORDS = {"yes", "y", "yeah", "yep", "yup"}
NO_WORDS = {"no", "n", "nope", "nah"}
# "no idea" and "no clue" start with "no" but mean "unknown".
UNKNOWN_AFTER_NO = {"idea", "clue"}


def parse_yes_no(text):
    """Return True (yes), False (no) or None (unknown).

    Reads the FIRST WORD only. It does not search for "no" inside the text,
    because "no" is inside "know" and "not".
    """
    words = re.findall(r"[a-z']+", (text or "").lower())
    if not words:
        return None
    first = words[0]
    if first in YES_WORDS:
        return True
    if first in NO_WORDS:
        if len(words) > 1 and words[1] in UNKNOWN_AFTER_NO:
            return None
        return False
    return None


def decide(answers):
    """Decide the screening outcome.

    answers: dict of field -> True / False / None. A missing field counts as None.
    Returns: {"outcome", "reasons", "unknowns", "answers"}

    Rules:
      is_sdf is True                    -> Required
      any field True, or any unknown    -> Recommended
      all fields False                  -> Optional
    "Unknown" is never treated as "No". It counts as a possible yes.
    """
    clean = {field: answers.get(field) for field in QUESTIONS}
    unknowns = [f for f, v in clean.items() if v is None]
    reasons = [YES_REASONS[f] for f, v in clean.items() if v is True]
    reasons += [f"Unknown: {QUESTIONS[f]} (treated as a possible yes)" for f in unknowns]

    if clean["is_sdf"] is True:
        outcome = "Required"
    elif reasons:
        outcome = "Recommended"
    else:
        outcome = "Optional"
        reasons = ["No screening trigger found. A DPIA is not required, but a short assessment is still useful."]

    return {"outcome": outcome, "reasons": reasons, "unknowns": unknowns, "answers": clean}


def run_screening(ask=input):
    """Ask the four questions and return the decision.

    `ask` is a function that shows a prompt and returns text. It is a parameter
    so that tests can give fake answers instead of typing.
    """
    answers = {}
    for field, question in QUESTIONS.items():
        answers[field] = parse_yes_no(ask(question + "\n> "))
    return decide(answers)