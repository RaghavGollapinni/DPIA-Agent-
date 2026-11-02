"""Stage 2 - Assessment profile.

One AssessmentProfile = one case file. It holds NAMED FACTS about the processing
activity, not loose sentences. Rules in later stages read these fields.

Value meaning for yes/no fields:
    True  = yes
    False = no
    None  = unknown (the owner did not know, or the question was not answered)
"""
from dataclasses import dataclass, field, asdict


@dataclass
class AssessmentProfile:
    # --- Stage 1: screening ---
    is_sdf: bool | None = None
    large_scale: bool | None = None
    sensitive_data: bool | None = None
    children: bool | None = None
    screening_outcome: str = ""
    screening_reasons: list = field(default_factory=list)

    # --- DPIA step 2: describe the processing ---
    processing_purpose: str | None = None
    data_categories: list = field(default_factory=list)
    data_principals: list = field(default_factory=list)
    data_all_necessary: bool | None = None       # is every data type needed for the purpose?

    # --- DPIA step 4: necessity and proportionality ---
    notice_given: bool | None = None
    consent_obtained: bool | None = None
    other_legal_basis: str | None = None          # asked only if consent_obtained is False
    consent_withdrawal_supported: bool | None = None
    third_party_sharing: bool | None = None
    third_party_contract: bool | None = None      # asked only if sharing is True
    retention_defined: bool | None = None
    retention_period: str | None = None           # asked only if retention_defined is True
    cross_border_transfer: bool | None = None

    # --- Security and accountability ---
    encryption: bool | None = None
    access_controls: bool | None = None
    breach_process: bool | None = None
    grievance_mechanism: bool | None = None
    rights_process: bool | None = None            # access, correction and erasure requests
    parental_consent: bool | None = None          # asked only if children is True

    # --- Record keeping ---
    asked_fields: list = field(default_factory=list)   # fields the interview actually asked
    raw_answers: list = field(default_factory=list)    # [{"question", "answer"}] exactly as typed

    def unknown_fields(self):
        """Fields that were asked but have no usable answer. They go in 'open questions'."""
        unknown = []
        for name in self.asked_fields:
            value = getattr(self, name)
            if value is None or value == [] or value == "":
                unknown.append(name)
        return unknown

    def to_dict(self):
        return asdict(self)
