from agents.retrieval import RetrievalAgent

agent = RetrievalAgent()

query = "We never ask users for consent."

results = agent.retrieve(query)

for r in results:
    print("=" * 50)
    print(r["topic"])
    print(r["section"])
    print(r["text"])