from agents.interviewer import InterviewAgent
from agents.scoring import RiskScoringAgent

interview = InterviewAgent()
responses = interview.conduct_interview()

scorer = RiskScoringAgent()
results = scorer.score(responses, [])

for r in results:
    print(r)