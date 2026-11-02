"""DPIA Assistant - runs the full assessment.

    python app.py            interactive interview
    python app.py --demo     built-in sample case (payroll for 8,000 employees)
"""
import argparse

from agents.interviewer import InterviewAgent
from agents.pipeline import assess_profile
from agents.report import ReportAgent


def load_retriever():
    try:
        from agents.retrieval import RetrievalAgent
        return RetrievalAgent()
    except ImportError as error:
        print(f"\nWarning: legal evidence is OFF ({error}). Run: pip install -r requirements.txt\n")
        return None


def main():
    parser = argparse.ArgumentParser(description="DPDP DPIA assistant")
    parser.add_argument("--demo", action="store_true", help="use the built-in sample answers")
    parser.add_argument("--out", default="outputs/DPIA_Report.docx", help="report file")
    args = parser.parse_args()

    # Stages 1-2: screening and interview -> AssessmentProfile
    if args.demo:
        from demo_answers import make_ask
        profile = InterviewAgent().run(ask=make_ask())
    else:
        profile = InterviewAgent().run()

    # Stages 3-6: rules, merge, legal evidence, draft, residual risk
    findings, open_questions = assess_profile(profile, load_retriever())

    print("\n===== Findings =====\n")
    for f in findings:
        t = f.treatment
        flag = "  <- ESCALATE" if t["escalate"] else ""
        print(f"{f.id}  {f.level:8} {f.score:2} -> {t['residual_level']:8} {t['residual_score']:2}  "
              f"[{f.category}] {f.title}  (approver: {t['approver']}){flag}")
    if not findings:
        print("No findings.")
    if open_questions:
        print("\nOpen questions (not assessed):", ", ".join(open_questions))

    # Stage 7: report
    path = ReportAgent().generate(profile, findings, open_questions, filename=args.out)
    print(f"\nReport saved: {path}")


if __name__ == "__main__":
    main()
