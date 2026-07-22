class RiskScoringAgent:

    def score(self, interview_responses, retrieved_chunks):
        risks = []

        for response in interview_responses:
            answer = response["answer"].lower()

            risk = "Low"

            if "no" in answer:
                risk = "High"

            elif "yes" in answer:
                risk = "Low"

            risks.append({
                "question": response["question"],
                "answer": response["answer"],
                "risk": risk
            })

        return risks