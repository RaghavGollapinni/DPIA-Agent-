"""One Finding = one possible privacy risk, found by one rule.

A finding keeps its own reasoning: which facts triggered it, how the score was built,
and (later) which DPDP text supports it. Nothing here comes from a language model.
"""
from dataclasses import dataclass, field, asdict

# Score bands for likelihood x impact (each 1-5, so score is 1-25).
# This is OUR rubric. It is not a DPDP Act threshold.
BANDS = [(1, 4, "Low"), (5, 9, "Medium"), (10, 16, "High"), (17, 25, "Critical")]


def level_for(score):
    for low, high, name in BANDS:
        if low <= score <= high:
            return name
    raise ValueError(f"score must be from 1 to 25, got {score!r}")


@dataclass
class Finding:
    rule_id: str                 # which rule created it, for example "N4"
    category: str                # same names as risk_category in the corpus
    cause: str                   # the specific reason. Two findings with different causes stay separate.
    title: str
    observed_practice: str       # what the owner reported
    potential_risk: str          # why that may be a problem for the people concerned
    recommendation: str          # the first-draft fix (Stage 6 improves the wording)
    likelihood: int              # 1-5
    impact: int                  # 1-5
    facts: dict = field(default_factory=dict)             # profile fields that triggered the rule
    notes: list = field(default_factory=list)             # how the score was built
    expected_chunk_ids: list = field(default_factory=list)  # for testing retrieval in Stage 5 only
    id: str = ""                 # set after sorting, for example "F-01"
    evidence: list = field(default_factory=list)          # filled in Stage 5
    draft: dict = field(default_factory=dict)             # filled in Stage 6 (drafting)
    treatment: dict = field(default_factory=dict)         # filled in Stage 6 (GRC: residual risk)

    def __post_init__(self):
        for name in ("likelihood", "impact"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                raise ValueError(f"{name} must be a whole number from 1 to 5, got {value!r}")

    @property
    def score(self):
        return self.likelihood * self.impact

    @property
    def level(self):
        return level_for(self.score)

    def to_dict(self):
        data = asdict(self)
        data["score"] = self.score
        data["level"] = self.level
        return data
