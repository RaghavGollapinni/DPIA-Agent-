"""Stage 7 - Report. Writes the DPIA as a Word file (python-docx)."""
import datetime
import os
from collections import Counter

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from agents.finding import BANDS
from agents.treatment import APPETITE_THRESHOLD, CONTROL_LIKELIHOOD_REDUCTION

LEVELS = [name for _, _, name in BANDS]
LEVEL_FILL = {"Low": "C6EFCE", "Medium": "FFEB9C", "High": "F8CBAD", "Critical": "FF9B9B"}
HEADER_FILL = "1F3864"

# Who should be consulted (DPIA step 3). The tool lists them. It does not consult them.
CONSULT = {
    "Security": "IT / information security lead",
    "Third-Party Sharing": "Vendor and procurement owner",
    "Children's Data": "Product owner and legal counsel",
    "Governance": "Senior management",
    "Cross-Border Transfer": "IT / hosting owner and legal counsel",
}


def _shade(cell, hex_color):
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shading)


def _write(cell, text, bold=False, size=9, color=None):
    cell.text = ""
    run = cell.paragraphs[0].add_run(str(text))
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def _table(doc, headers, rows, widths_cm, level_col=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.autofit = False
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        _write(cell, header, bold=True, color="FFFFFF")
        _shade(cell, HEADER_FILL)
    repeat = OxmlElement("w:tblHeader")                 # repeat the header row on each page
    repeat.set(qn("w:val"), "true")
    table.rows[0]._tr.get_or_add_trPr().append(repeat)
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            _write(cells[i], value)
            if i == level_col:
                level = str(value).split(" ")[0]
                if level in LEVEL_FILL:
                    _shade(cells[i], LEVEL_FILL[level])
    for i, width in enumerate(widths_cm):          # set the grid AND each cell (Word and LibreOffice differ)
        table.columns[i].width = Cm(width)
    for row in table.rows:
        for i, width in enumerate(widths_cm):
            row.cells[i].width = Cm(width)
    doc.add_paragraph()
    return table


def _bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def _yn(value):
    return {True: "Yes", False: "No", None: "Unknown"}[value]


class ReportAgent:
    def generate(self, profile, findings, open_questions, filename="outputs/DPIA_Report.docx"):
        doc = Document()
        section = doc.sections[0]
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width, section.page_height = section.page_height, section.page_width
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(section, side, Cm(1.8))
        section.footer.paragraphs[0].text = (
            "DRAFT - decision support only. A qualified person must review this report before use.")

        purpose = profile.processing_purpose or "(purpose not stated)"
        doc.add_heading("Data Protection Impact Assessment", level=0)
        doc.add_paragraph(f"Processing activity: {purpose}")
        doc.add_paragraph(
            f"Date: {datetime.date.today().strftime('%d %B %Y')}   |   Version: 0.1 DRAFT   |   "
            "Law: Digital Personal Data Protection Act, 2023 (India)   |   Prepared by: DPIA Assistant")

        self._summary(doc, profile, findings, open_questions)
        self._screening(doc, profile)
        self._processing(doc, profile)
        self._consultation(doc, findings)
        self._register(doc, findings)
        self._treatment(doc, findings)
        self._evidence(doc, findings)
        self._open_questions(doc, open_questions)
        self._signoff(doc, findings)
        self._method(doc)
        self._appendix(doc, profile)

        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        doc.save(filename)
        return filename

    # ------------------------------------------------------------ sections
    def _summary(self, doc, profile, findings, open_questions):
        doc.add_heading("1. Executive summary", level=1)
        now = Counter(f.level for f in findings)
        after = Counter(f.treatment["residual_level"] for f in findings)
        escalate = [f for f in findings if f.treatment.get("escalate")]
        doc.add_paragraph(
            f"Screening result: a DPIA is {profile.screening_outcome.lower()}. "
            f"The rules produced {len(findings)} finding(s). "
            f"Now: {now['Critical']} Critical, {now['High']} High, {now['Medium']} Medium, {now['Low']} Low. "
            f"After the recommended controls: {after['Critical']} Critical, {after['High']} High, "
            f"{after['Medium']} Medium, {after['Low']} Low.")
        if escalate:
            ids = ", ".join(f.id for f in escalate)
            doc.add_paragraph(
                f"{len(escalate)} finding(s) ({ids}) stay at or above the risk-appetite threshold "
                f"({APPETITE_THRESHOLD}) even after the recommended control. The project owner cannot "
                "accept them. They must go to senior management.")
        else:
            doc.add_paragraph("No finding stays at or above the risk-appetite threshold after the recommended controls.")
        if open_questions:
            doc.add_paragraph(f"{len(open_questions)} question(s) were not answered, so they could not be assessed. "
                              "See section 8. Unknown answers are never treated as safe.")
        if findings:
            doc.add_paragraph("Most serious findings now:")
            _bullets(doc, [f"{f.id} [{f.level}, {f.score}] {f.title}" for f in findings[:3]])

    def _screening(self, doc, profile):
        doc.add_heading("2. Screening (is a DPIA needed?)", level=1)
        doc.add_paragraph(f"Outcome: {profile.screening_outcome}")
        _bullets(doc, profile.screening_reasons)

    def _processing(self, doc, profile):
        doc.add_heading("3. Description of the processing", level=1)
        rows = [
            ("Purpose", profile.processing_purpose or "Not stated"),
            ("Personal data collected", ", ".join(profile.data_categories) or "Not stated"),
            ("Whose data", ", ".join(profile.data_principals) or "Not stated"),
            ("Notice given before collection", _yn(profile.notice_given)),
            ("Consent obtained", _yn(profile.consent_obtained)),
            ("Other legal basis", profile.other_legal_basis or "Not applicable / not stated"),
            ("Shared with third parties", _yn(profile.third_party_sharing)),
            ("Written contract with third party", _yn(profile.third_party_contract)),
            ("Retention rule defined", _yn(profile.retention_defined)),
            ("Stored or accessed outside India", _yn(profile.cross_border_transfer)),
            ("Encryption", _yn(profile.encryption)),
            ("Access controls and logging", _yn(profile.access_controls)),
            ("Breach process", _yn(profile.breach_process)),
            ("Grievance mechanism", _yn(profile.grievance_mechanism)),
            ("Rights requests handled", _yn(profile.rights_process)),
        ]
        _table(doc, ["Item", "Answer (as reported by the project owner)"], rows, [8, 17])

    def _consultation(self, doc, findings):
        doc.add_heading("4. Who should be consulted", level=1)
        doc.add_paragraph("This tool does not consult anyone. Based on the findings, these people should review the draft:")
        people = {"Project owner": "Owns the processing and accepts low risks.",
                  "Data Protection Officer or privacy lead": "Reviews all findings and accepts Medium residual risks."}
        for f in findings:
            role = CONSULT.get(f.category)
            if role and role not in people:
                people[role] = f"Needed for {f.category} findings."
        _bullets(doc, [f"{role}: {why}" for role, why in people.items()])

    def _register(self, doc, findings):
        doc.add_heading("5. Risk register", level=1)
        if not findings:
            doc.add_paragraph("The rules in this tool found no risks. This does not prove there are none.")
            return
        doc.add_paragraph(
            "Score = likelihood x impact (each 1 to 5). Bands: 1-4 Low, 5-9 Medium, 10-16 High, 17-25 Critical. "
            "These bands and values are this project's own rubric, not DPDP Act thresholds.")
        rows = []
        for f in findings:
            sections = ", ".join(sorted({f"s.{e['section']}" for e in f.evidence})) or "none retrieved"
            rows.append([f.id, f.category, f"{f.title}\n{f.observed_practice}", f.potential_risk,
                         f"{f.level} ({f.score}) L{f.likelihood} x I{f.impact}", sections])
        _table(doc, ["ID", "Category", "Finding and observed practice", "Potential risk", "Risk now", "Closest DPDP sections"],
               rows, [1.4, 3.2, 7.2, 6.2, 3.4, 3.6], level_col=4)

    def _treatment(self, doc, findings):
        doc.add_heading("6. Recommendations and residual risk", level=1)
        doc.add_paragraph(
            f"Residual risk is a projection. It assumes the recommended control is applied and lowers likelihood by "
            f"{CONTROL_LIKELIHOOD_REDUCTION} points (minimum 1). Impact does not change. The project owner may accept a "
            f"residual score below {APPETITE_THRESHOLD}. A score of {APPETITE_THRESHOLD} or more needs a senior decision.")
        rows = []
        for f in findings:
            t = f.treatment
            decision = "Escalate - owner cannot accept" if t["escalate"] else "Owner may accept after control"
            rows.append([f.id, f.draft["action"], t["treatment"],
                         f"{t['residual_level']} ({t['residual_score']})", decision, t["approver"], "Pending"])
        if rows:
            _table(doc, ["ID", "Recommended action", "Treatment", "Risk after control", "Decision rule", "Approver", "Review status"],
                   rows, [1.4, 9.5, 2.2, 3.0, 4.3, 3.2, 2.4], level_col=3)
        before = Counter(f.level for f in findings)
        after = Counter(f.treatment["residual_level"] for f in findings)
        _table(doc, ["Level", "Findings now", "Findings after controls"],
               [[lv, before[lv], after[lv]] for lv in reversed(LEVELS)], [4, 4, 5])
        doc.add_paragraph("Treatment options in risk management are Mitigate, Accept, Transfer and Avoid. "
                          "This tool suggests Mitigate or Accept. A reviewer decides on Transfer or Avoid.")

    def _evidence(self, doc, findings):
        doc.add_heading("7. Legal evidence for each finding", level=1)
        doc.add_paragraph("Evidence is found by text similarity. A high similarity means close wording. "
                          "It does not prove that the provision applies. A reviewer must confirm each one.")
        for f in findings:
            doc.add_heading(f"{f.id} - {f.title}", level=3)
            if not f.evidence:
                doc.add_paragraph("No legal text was retrieved.")
                continue
            rows = [[e["rank"], f"s.{e['section']}", e["title"], f"{e['similarity']:.2f} ({e['strength']})", e["text"]]
                    for e in f.evidence]
            _table(doc, ["Rank", "Section", "Provision", "Similarity", "Corpus text"], rows, [1.4, 1.8, 4.5, 3.2, 14.1])

    def _open_questions(self, doc, open_questions):
        doc.add_heading("8. Open questions (not assessed)", level=1)
        if not open_questions:
            doc.add_paragraph("All questions that were asked have an answer.")
            return
        doc.add_paragraph("These questions had no usable answer. They were not assessed and not assumed to be safe:")
        _bullets(doc, [name.replace("_", " ") for name in open_questions])

    def _signoff(self, doc, findings):
        doc.add_heading("9. Review and sign-off", level=1)
        doc.add_paragraph("Review again within 12 months, or sooner if the processing changes.")
        roles = ["Project owner", "Data Protection Officer / privacy lead"]
        if any(f.treatment.get("escalate") for f in findings):
            roles.append("Senior management (needed because of escalated findings)")
        _table(doc, ["Role", "Name", "Decision (Accept / Revise / Reject)", "Date", "Signature"],
               [[r, "", "", "", ""] for r in roles], [8, 5, 6, 3, 4])

    def _method(self, doc):
        doc.add_heading("10. Method and limits", level=1)
        _bullets(doc, [
            "Rules decide each risk. The retrieved law only supports it. No language model scores or writes anything.",
            "Unknown answers are listed as open questions. They are never treated as safe.",
            "The likelihood values, impact values, score bands, context uplift (+1 impact) and the effect of a control "
            "(-2 likelihood) are this project's own rubric. They are not DPDP Act thresholds.",
            "The legal corpus has 20 curated provisions. It is a summary, not the full Act. Check every cited section "
            "against the official text, and check whether the DPDP Rules or sector rules add duties.",
            "This tool covers screening, description, necessity, risk, evidence, treatment and sign-off. It does not "
            "consult people, and it does not check data accuracy, processor audits or sector-specific rules.",
            "This report is decision support. It is not legal advice or a compliance certificate.",
        ])

    def _appendix(self, doc, profile):
        doc.add_heading("Appendix A. Interview record", level=1)
        _table(doc, ["Question", "Answer as typed"], [[a["question"], a["answer"]] for a in profile.raw_answers], [14, 11])
