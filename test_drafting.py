from agents.drafting import DraftingAgent
import json

with open("knowledge/privacy_corpus.json", "r", encoding="utf-8") as f:
    corpus = json.load(f)

agent = DraftingAgent()

result = agent.generate(
    "High",
    corpus[1]
)

print(result)