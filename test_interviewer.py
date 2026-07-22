from agents.interviewer import InterviewAgent

agent = InterviewAgent()

responses = agent.conduct_interview()

print("\nResponses:\n")

for response in responses:
    print(response)