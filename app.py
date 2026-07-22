from agents.interviewer import InterviewAgent
from agents.retrieval import RetrievalAgent
from agents.scoring import RiskScoringAgent
from agents.drafting import DraftingAgent
from agents.report import ReportAgent


def main():

    interviewer = InterviewAgent()
    retrieval = RetrievalAgent()
    scoring = RiskScoringAgent()
    drafting = DraftingAgent()
    report = ReportAgent()

    interview = interviewer.conduct_interview()

    findings = []

    for response in interview:

        retrieved = retrieval.retrieve(response["answer"], top_k=1)

        clause = retrieved[0]

        risk = scoring.score([response], retrieved)[0]["risk"]

        draft = drafting.generate(risk, clause)

        findings.append({
            "topic": clause["topic"],
            "risk_level": draft["risk_level"],
            "risk_summary": draft["risk_summary"],
            "recommendation": draft["recommendation"]
        })

    report.generate(interview, findings)


if __name__ == "__main__":
    main()