class DraftingAgent:

    def generate(self, risk, clause):

        return {
            "risk_level": risk,
            "risk_summary": clause["text"],
            "recommendation": clause["mitigation_hint"]
        }