"""Stage 6 - Drafting.

Template-based. Every sentence comes from the rule or from the retrieved legal text.
No language model writes any text, so nothing can be invented.

Structure of one draft:  observed practice -> risk -> legal text -> action.
"""


class DraftingAgent:
    def draft(self, finding):
        top = finding.evidence[0] if finding.evidence else None
        if top:
            law = f"DPDP Act s.{top['section']} - {top['title']}: {top['text']}"
            citation = f"s.{top['section']} (corpus chunk {top['chunk_id']})"
            note = (f"Closest provision by text similarity ({top['similarity']:.2f}, {top['strength']}). "
                    "A reviewer must confirm that it applies.")
            hint = top.get("mitigation_hint", "")
        else:
            law, citation = None, "none retrieved"
            note = "No legal text was retrieved for this finding. A reviewer must find the provision."
            hint = ""

        finding.draft = {
            "observed": finding.observed_practice,
            "risk": finding.potential_risk,
            "law": law,
            "citation": citation,
            "action": finding.recommendation,
            "extra_guidance": hint if hint and hint != finding.recommendation else "",
            "evidence_note": note,
        }
        return finding.draft
