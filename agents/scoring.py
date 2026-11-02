"""Stage 3 - Necessity and proportionality rules.

Each rule reads NAMED FACTS from the AssessmentProfile and returns zero or one Finding.
A rule fires only when the answer is a clear "no" (False). An unknown answer (None)
never fires a rule and is never treated as safe: it goes to the report as an OPEN QUESTION.
(For example, a purpose that is not stated is an open question, not a finding.)

Scoring rubric (our own, not a DPDP rule):
  likelihood : 1-5, set by each rule. A missing control is rated 4.
  impact     : 1-5, a base value set by each rule.
                 +1 if the processing involves sensitive data, children's data or
                 large scale. If one of those is unknown, we assume yes.
  score      : likelihood x impact (1-25). Bands are in finding.py.
"""
from agents.finding import Finding

CONTEXT_FLAGS = {
    "sensitive_data": "sensitive (financial, health or biometric) data",
    "children": "children's data",
    "large_scale": "large-scale processing",
}


def _blank(value):
    return value is None or str(value).strip() == ""


def _context_uplift(profile):
    """Return (extra_impact, notes). The uplift is +1 at most, however many flags apply."""
    applied = []
    for name, label in CONTEXT_FLAGS.items():
        value = getattr(profile, name)
        if value is True:
            applied.append(label)
        elif value is None:
            applied.append(f"{label} (unknown, assumed yes)")
    if not applied:
        return 0, []
    return 1, [f"Impact +1 context: {'; '.join(applied)}."]


def _make(profile, base_impact, **kwargs):
    uplift, notes = _context_uplift(profile)
    impact = min(5, base_impact + uplift)
    all_notes = [f"Likelihood {kwargs['likelihood']} set by rule {kwargs['rule_id']}.",
                 f"Base impact {base_impact}."] + notes
    return Finding(impact=impact, notes=all_notes, **kwargs)


# ---------------------------------------------------------------- rules
# Each rule: (profile) -> Finding or None.

def rule_notice(p):
    if p.notice_given is False:
        return _make(
            p, 2, rule_id="N1", category="Notice & Transparency", cause="no-notice", likelihood=4,
            title="No notice before collection",
            observed_practice="People are not told what data is collected and why, before or when it is collected.",
            potential_risk="People cannot make an informed choice or exercise their rights.",
            recommendation="Give a plain-language notice at the point of collection: data collected, purpose, how to exercise rights, how to complain.",
            facts={"notice_given": False}, expected_chunk_ids=[1])


def rule_no_lawful_basis(p):
    if p.consent_obtained is False and _blank(p.other_legal_basis):
        return _make(
            p, 4, rule_id="N2", category="Legal Basis", cause="no-lawful-basis", likelihood=5,
            title="No consent and no other legal basis",
            observed_practice="Consent is not obtained and no other legal basis was given.",
            potential_risk="The processing may have no lawful ground at all.",
            recommendation="Identify the legal basis for each purpose: obtain valid consent, or document which legitimate use applies.",
            facts={"consent_obtained": False, "other_legal_basis": p.other_legal_basis},
            expected_chunk_ids=[2, 5])


def rule_legal_basis_to_confirm(p):
    if p.consent_obtained is False and not _blank(p.other_legal_basis):
        return _make(
            p, 2, rule_id="N3", category="Legal Basis", cause="legitimate-use-unconfirmed", likelihood=2,
            title="Legal basis other than consent needs confirmation",
            observed_practice=f"Consent is not obtained. The stated basis is: {p.other_legal_basis}.",
            potential_risk="The stated basis may not match a legitimate use allowed by the Act.",
            recommendation="Record which legitimate use applies and who confirmed it. Have a privacy professional review it.",
            facts={"consent_obtained": False, "other_legal_basis": p.other_legal_basis},
            expected_chunk_ids=[5])


def rule_withdrawal(p):
    if p.consent_obtained is True and p.consent_withdrawal_supported is False:
        return _make(
            p, 3, rule_id="N4", category="Consent", cause="no-withdrawal", likelihood=4,
            title="Consent cannot be withdrawn",
            observed_practice="Consent is obtained, but people cannot withdraw it as easily as they gave it.",
            potential_risk="Consent may not be valid, and people lose control of their data.",
            recommendation="Add a simple withdrawal option, and stop processing that relies on the consent when it is withdrawn.",
            facts={"consent_obtained": True, "consent_withdrawal_supported": False},
            expected_chunk_ids=[3])


def rule_over_collection(p):
    if p.data_all_necessary is False:
        return _make(
            p, 3, rule_id="N5", category="Purpose & Minimisation", cause="over-collection", likelihood=4,
            title="More data collected than the purpose needs",
            observed_practice="Some of the data collected is not needed for the stated purpose.",
            potential_risk="Extra data increases exposure in a breach and may fall outside what people agreed to.",
            recommendation="List each data field against the purpose. Stop collecting and delete fields that are not needed.",
            facts={"data_all_necessary": False}, expected_chunk_ids=[2])


def rule_retention(p):
    if p.retention_defined is False:
        return _make(
            p, 3, rule_id="N7", category="Retention", cause="no-retention-rule", likelihood=4,
            title="No defined retention period",
            observed_practice="There is no defined retention period or deletion rule.",
            potential_risk="Data may be kept after the purpose ends, which breaks the erasure duty and increases breach impact.",
            recommendation="Set a retention period tied to the purpose, and delete or anonymise data when it ends, unless a law requires longer.",
            facts={"retention_defined": False}, expected_chunk_ids=[7])


# ---- Stage 4: security, third parties, rights, children, transfer, governance

def rule_encryption(p):
    if p.encryption is False:
        return _make(
            p, 4, rule_id="S1", category="Security", cause="no-encryption", likelihood=4,
            title="Stored personal data is not encrypted",
            observed_practice="Stored personal data is not encrypted.",
            potential_risk="If the data is stolen or leaked, anyone can read it.",
            recommendation="Encrypt personal data at rest and in transit, and keep the keys separate from the data.",
            facts={"encryption": False}, expected_chunk_ids=[6])


def rule_access_controls(p):
    if p.access_controls is False:
        return _make(
            p, 4, rule_id="S2", category="Security", cause="no-access-control", likelihood=4,
            title="Access to personal data is not controlled or logged",
            observed_practice="Access to personal data is not limited to authorised staff, or access is not logged.",
            potential_risk="Staff or others may view or copy data without a business need, and misuse cannot be traced.",
            recommendation="Give access by role, require multi-factor authentication for administrators, and review access logs.",
            facts={"access_controls": False}, expected_chunk_ids=[6])


def rule_breach_process(p):
    if p.breach_process is False:
        return _make(
            p, 4, rule_id="S3", category="Security", cause="no-breach-process", likelihood=4,
            title="No data-breach response process",
            observed_practice="There is no process to detect, report and respond to a personal data breach.",
            potential_risk="A breach may go unnoticed or unreported, and the Data Protection Board and affected people may not be told.",
            recommendation="Write a breach process: detect, assess, contain, notify the Board and affected people, and keep a record.",
            facts={"breach_process": False}, expected_chunk_ids=[6, 19])


def rule_processor_contract(p):
    if p.third_party_sharing is True and p.third_party_contract is False:
        return _make(
            p, 4, rule_id="T1", category="Third-Party Sharing", cause="no-processor-contract", likelihood=4,
            title="No written contract with the data processor",
            observed_practice="Data is shared with a third party, and there is no written data-protection contract.",
            potential_risk="The organisation stays fully responsible, but has no written control over how the vendor handles the data.",
            recommendation="Sign a data-processing agreement: purpose, security, sub-processors, breach notice and deletion.",
            facts={"third_party_sharing": True, "third_party_contract": False}, expected_chunk_ids=[17])


def rule_children(p):
    if p.children is True and p.parental_consent is False:
        return _make(
            p, 4, rule_id="C1", category="Children's Data", cause="no-parental-consent", likelihood=5,
            title="Children's data without verified parental consent",
            observed_practice="Children's data is processed without verified parental or guardian consent.",
            potential_risk="The processing may have no valid consent, and children may be harmed.",
            recommendation="Add age checks and verifiable parental consent. Do not track or target children with advertising.",
            facts={"children": True, "parental_consent": False}, expected_chunk_ids=[10])


def rule_rights(p):
    if p.rights_process is False:
        return _make(
            p, 3, rule_id="R1", category="Data Principal Rights", cause="no-rights-process", likelihood=4,
            title="No process for access, correction or erasure requests",
            observed_practice="People cannot ask to see, correct or delete their data, or requests are not acted on.",
            potential_risk="People cannot use their rights, and requests may go unanswered.",
            recommendation="Create a request process with a named owner and a response deadline.",
            facts={"rights_process": False}, expected_chunk_ids=[12, 13])


def rule_grievance(p):
    if p.grievance_mechanism is False:
        return _make(
            p, 2, rule_id="G1", category="Accountability", cause="no-grievance", likelihood=4,
            title="No grievance mechanism",
            observed_practice="People have no way to make a complaint about their data.",
            potential_risk="People cannot raise a concern with the organisation first, so complaints may go straight to the Board.",
            recommendation="Publish the contact details of a responsible officer and set a response time for complaints.",
            facts={"grievance_mechanism": False}, expected_chunk_ids=[9, 14])


def rule_cross_border(p):
    # This is a "to confirm" item, not a proven gap, so likelihood is low.
    if p.cross_border_transfer is True:
        return _make(
            p, 3, rule_id="X1", category="Cross-Border Transfer", cause="transfer-to-confirm", likelihood=2,
            title="Data is stored or accessed outside India",
            observed_practice="Personal data is stored or accessed outside India.",
            potential_risk="The government may restrict transfers to some countries.",
            recommendation="Check that the destination country is not restricted, and record the check.",
            facts={"cross_border_transfer": True}, expected_chunk_ids=[16])


def rule_sdf(p):
    # This is a "to confirm" item, not a proven gap, so likelihood is low.
    if p.is_sdf is True:
        return _make(
            p, 3, rule_id="D1", category="Governance", cause="sdf-duties", likelihood=2,
            title="Significant Data Fiduciary duties apply",
            observed_practice="The organisation is a Significant Data Fiduciary.",
            potential_risk="Extra duties apply, and missing any of them is a compliance gap.",
            recommendation="Confirm that an India-based Data Protection Officer is appointed, an independent data audit is planned, and DPIAs are repeated on a schedule.",
            facts={"is_sdf": True}, expected_chunk_ids=[11])


RULES = [rule_notice, rule_no_lawful_basis, rule_legal_basis_to_confirm, rule_withdrawal,
         rule_over_collection, rule_retention,
         rule_encryption, rule_access_controls, rule_breach_process, rule_processor_contract,
         rule_children, rule_rights, rule_grievance, rule_cross_border, rule_sdf]


class RiskScoringAgent:
    def assess(self, profile):
        """Run every rule. Return findings sorted by score (highest first), with IDs."""
        findings = [f for rule in RULES if (f := rule(profile)) is not None]
        findings.sort(key=lambda f: -f.score)          # stable: ties keep rule order
        for number, finding in enumerate(findings, start=1):
            finding.id = f"F-{number:02d}"
        return findings

    def open_questions(self, profile):
        """Facts that were asked but not answered. These could not be assessed."""
        return profile.unknown_fields()
