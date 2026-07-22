class InterviewAgent:

    def __init__(self):
        self.questions = [
            "Do you collect personal data?",
            "What types of personal data do you collect?",
            "Why do you collect this data?",
            "Do you obtain user consent before collecting data?",
            "Can users withdraw their consent?",
            "Do you share data with third parties?",
            "How long do you retain personal data?",
            "Do you encrypt or otherwise protect stored data?",
            "Do you process children's personal data?",
            "Do you have a grievance or complaint mechanism?"
        ]

    def conduct_interview(self):
        responses = []

        print("\n===== DPIA Interview =====\n")

        for question in self.questions:
            answer = input(question + "\n> ")

            responses.append({
                "question": question,
                "answer": answer
            })

        return responses