"""Stage 4 - Finding consolidator.

Rule: findings with the SAME category AND the SAME cause are one risk. Merge them.
Findings with the same category but a DIFFERENT cause stay separate, because they need
different fixes (for example "no withdrawal" and "no notice").

With one rule per cause, duplicates are already rare. This step is a safety net. It also
guarantees the old fault (the same Consent text repeated six times) cannot return.
"""
from collections import OrderedDict


def consolidate(findings):
    groups = OrderedDict()
    for finding in findings:
        groups.setdefault((finding.category, finding.cause), []).append(finding)

    merged = []
    for items in groups.values():
        base = max(items, key=lambda f: f.score)          # keep the most serious one
        if len(items) > 1:
            others = [f for f in items if f is not base]
            for other in others:
                base.facts.update(other.facts)
                for chunk_id in other.expected_chunk_ids:
                    if chunk_id not in base.expected_chunk_ids:
                        base.expected_chunk_ids.append(chunk_id)
            base.notes.append(
                f"Merged {len(others)} duplicate finding(s) from rule(s) "
                f"{', '.join(o.rule_id for o in others)}."
            )
        merged.append(base)

    merged.sort(key=lambda f: -f.score)                    # stable: ties keep earlier order
    for number, finding in enumerate(merged, start=1):
        finding.id = f"F-{number:02d}"
    return merged


def group_by_category(findings):
    """Return {category: [findings]} in order of the most serious finding in each category."""
    groups = OrderedDict()
    for finding in findings:                               # findings are already sorted by score
        groups.setdefault(finding.category, []).append(finding)
    return groups
