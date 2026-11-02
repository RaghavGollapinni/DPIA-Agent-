"""Stage 2 - Interview.

Runs screening first, then a fixed list of questions. Answers are converted into
the named fields of an AssessmentProfile. Two questions are CONDITIONAL: they are
asked only when an earlier answer makes them relevant.
"""
import re

from agents.profile import AssessmentProfile
from agents.screening import run_screening, parse_yes_no

UNKNOWN_TEXT = {"", "unknown", "not sure", "dont know", "don't know", "i don't know",
                "i do not know", "na", "n/a", "none given",
                "no", "none", "nothing", "nil", "no idea", "not applicable"}

# (field, kind, question, condition)
# kind: "yesno" | "text" | "list".  condition: None, or a function(profile) -> bool.
QUESTIONS = [
    # DPIA step 2 - describe the processing
    ("processing_purpose", "text", "What is the purpose of this processing? (for example: salary payment)", None),
    ("data_categories", "list", "List the types of personal data you collect (separate with commas).", None),
    ("data_principals", "list", "Whose data is it? (for example: employees, customers)", None),

    # DPIA step 4 - necessity and proportionality
    ("data_all_necessary", "yesno", "Is every data type you listed really needed for that purpose?", None),
    ("notice_given", "yesno", "Do you tell people what data you collect and why, before or when you collect it?", None),
    ("consent_obtained", "yesno", "Do you obtain consent before collecting the data?", None),
    ("other_legal_basis", "text", "If you do not obtain consent, what is your legal basis? (for example: employment, legal obligation)",
        lambda p: p.consent_obtained is False),
    ("consent_withdrawal_supported", "yesno", "Can people withdraw consent as easily as they gave it?",
        lambda p: p.consent_obtained is not False),
    ("third_party_sharing", "yesno", "Do you share the data with third parties or processors?", None),
    ("third_party_contract", "yesno", "Is there a written contract with them that covers data protection?",
        lambda p: p.third_party_sharing is True),
    ("retention_defined", "yesno", "Do you have a defined retention period or deletion rule?", None),
    ("retention_period", "text", "What is the retention period or rule?",
        lambda p: p.retention_defined is True),
    ("cross_border_transfer", "yesno", "Is the data stored or accessed outside India?", None),

    # Security and accountability
    ("encryption", "yesno", "Is stored personal data encrypted?", None),
    ("access_controls", "yesno", "Is access limited to authorised staff, and is access logged?", None),
    ("breach_process", "yesno", "Do you have a process to detect, report and respond to a data breach?", None),
    ("grievance_mechanism", "yesno", "Do people have a way to make a complaint about their data?", None),
    ("rights_process", "yesno", "Can people ask to see, correct or delete their data, and do you act on those requests?", None),
    ("parental_consent", "yesno", "Do you verify parental or guardian consent before processing a child's data?",
        lambda p: p.children is True),
]


def parse_text(text):
    cleaned = (text or "").strip()
    return None if cleaned.lower() in UNKNOWN_TEXT else cleaned


def parse_list(text):
    cleaned = parse_text(text)
    if cleaned is None:
        return []
    return [item.strip() for item in re.split(r"[,;\n]", cleaned) if item.strip()]


PARSERS = {"yesno": parse_yes_no, "text": parse_text, "list": parse_list}


class InterviewAgent:
    def run(self, ask=input, say=print):
        """Return a filled AssessmentProfile.

        ask and say are parameters so that a test can give fake answers
        instead of typing.
        """
        profile = AssessmentProfile()

        def logged_ask(prompt):
            answer = ask(prompt)
            profile.raw_answers.append({"question": prompt.split("\n")[0], "answer": answer})
            return answer

        say("\n===== Step 1: Screening =====\n")
        screening = run_screening(ask=logged_ask)
        for name, value in screening["answers"].items():
            setattr(profile, name, value)
            profile.asked_fields.append(name)
        profile.screening_outcome = screening["outcome"]
        profile.screening_reasons = screening["reasons"]
        say(f"\nScreening result: DPIA {screening['outcome']}")
        for reason in screening["reasons"]:
            say(f"  - {reason}")

        say("\n===== Step 2: Describe the processing and controls =====\n")
        for name, kind, question, condition in QUESTIONS:
            if condition is not None and not condition(profile):
                continue                      # not relevant, so not asked and not "unknown"
            answer = logged_ask(question + "\n> ")
            setattr(profile, name, PARSERS[kind](answer))
            profile.asked_fields.append(name)

        return profile
