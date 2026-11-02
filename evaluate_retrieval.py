"""Test the REAL retrieval (MiniLM + FAISS) against the labels in each rule.

Run on your own computer:   python evaluate_retrieval.py

Every rule lists the corpus chunks that should support its finding (expected_chunk_ids).
We build cases that fire every rule, retrieve the top 3, and report:
  Recall@1 / Recall@3 : how often an expected chunk is in the top 1 / top 3
  MRR                 : average of 1 / (rank of the first expected chunk)
Then it lists the failures, and the similarity of right and wrong matches, so that you can
set STRONG_AT and MODERATE_AT in agents/retrieval.py from real numbers.
"""
from agents.profile import AssessmentProfile
from agents.retrieval import RetrievalAgent
from agents.scoring import RiskScoringAgent


def case(**changes):
    base = dict(is_sdf=True, large_scale=True, sensitive_data=True, children=True,
                processing_purpose="x", data_all_necessary=False, notice_given=False,
                consent_obtained=True, consent_withdrawal_supported=False, third_party_sharing=True,
                third_party_contract=False, retention_defined=False, cross_border_transfer=True,
                encryption=False, access_controls=False, breach_process=False, grievance_mechanism=False,
                rights_process=False, parental_consent=False)
    base.update(changes)
    return AssessmentProfile(asked_fields=list(base), **base)


def main(top_k=3):
    retriever = RetrievalAgent()
    cases = [case(),                                                      # fires most rules, incl. N4
             case(consent_obtained=False, other_legal_basis=None),        # N2
             case(consent_obtained=False, other_legal_basis="employment")]  # N3
    seen, rows = set(), []
    for profile in cases:
        for f in RiskScoringAgent().assess(profile):
            if f.rule_id in seen:
                continue
            seen.add(f.rule_id)
            results = retriever.retrieve(retriever.query_for(f), top_k=top_k)
            ids = [r["id"] for r in results]
            rank = next((i + 1 for i, cid in enumerate(ids) if cid in f.expected_chunk_ids), None)
            rows.append((f, results, rank))

    n = len(rows)
    r1 = sum(1 for _, _, rank in rows if rank == 1) / n
    r3 = sum(1 for _, _, rank in rows if rank) / n
    mrr = sum(1 / rank for _, _, rank in rows if rank) / n
    print(f"\nRules tested: {n}   Recall@1: {r1:.2f}   Recall@{top_k}: {r3:.2f}   MRR: {mrr:.2f}\n")
    print(f"{'Rule':5}{'Expected':12}{'Retrieved (id:sim)':44}Rank")
    for f, results, rank in rows:
        got = ", ".join(f"{r['id']}:{r['similarity']:.2f}" for r in results)
        print(f"{f.rule_id:5}{str(f.expected_chunk_ids):12}{got:44}{rank or 'MISS'}")

    right = [r["similarity"] for f, res, _ in rows for r in res if r["id"] in f.expected_chunk_ids]
    wrong = [r["similarity"] for f, res, _ in rows for r in res if r["id"] not in f.expected_chunk_ids]
    if right and wrong:
        print(f"\nSimilarity of correct matches : min {min(right):.2f}  mean {sum(right)/len(right):.2f}")
        print(f"Similarity of other matches   : max {max(wrong):.2f}  mean {sum(wrong)/len(wrong):.2f}")
    misses = [(f, res) for f, res, rank in rows if not rank]
    if misses:
        print("\nFAILURES (write these in your README as known limits):")
        for f, res in misses:
            print(f"  {f.rule_id} '{f.title}' expected {f.expected_chunk_ids}, got {[r['title'] for r in res]}")


if __name__ == "__main__":
    main()
