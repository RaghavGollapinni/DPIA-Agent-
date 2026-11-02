"""Scripted answers for `python app.py --demo`: a payroll system for 8,000 employees.

Each key is a piece of a question. The longest matching key wins. A blank answer means unknown.
"""
DEMO_ANSWERS = {
    "significant data fiduciary": "No, I think not",
    "large number of people": "Yes, 8000 employees",
    "financial, health or biometric": "Yes, bank details",
    "children's personal data": "No",
    "purpose of this processing": "Paying monthly salaries",
    "types of personal data": "name, phone, email, salary, bank account, insurance",
    "whose data": "employees",
    "really needed": "No, insurance details are not needed for salary",
    "tell people what data": "No",
    "obtain consent before": "No",
    "what is your legal basis": "employment",
    "share the data with third": "Yes, a payroll vendor",
    "written contract": "not sure",
    "defined retention": "No",
    "outside india": "No",
    "encrypted": "Yes",
    "access limited": "Yes",
    "data breach": "No",
    "complaint": "No",
    "ask to see, correct or delete": "No",
}


def make_ask(answers=None, show=True):
    answers = answers or DEMO_ANSWERS

    def ask(prompt):
        question = prompt.split("\n")[0]
        hits = [key for key in answers if key in question.lower()]
        answer = answers[max(hits, key=len)] if hits else ""
        if show:
            print(f"{question}\n> {answer}")
        return answer

    return ask
