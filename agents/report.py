from docx import Document


class ReportAgent:

    def generate(self, interview, findings, filename="DPIA_Report.docx"):

        doc = Document()

        doc.add_heading("Data Protection Impact Assessment Report", level=1)

        doc.add_heading("Interview Responses", level=2)

        for item in interview:
            doc.add_paragraph(f"Q: {item['question']}")
            doc.add_paragraph(f"A: {item['answer']}")
            doc.add_paragraph()

        doc.add_heading("Risk Assessment", level=2)

        for item in findings:
            doc.add_heading(item["topic"], level=3)
            doc.add_paragraph(f"Risk Level: {item['risk_level']}")
            doc.add_paragraph(f"Summary: {item['risk_summary']}")
            doc.add_paragraph(f"Recommendation: {item['recommendation']}")
            doc.add_paragraph("-" * 50)

        doc.save(filename)

        print(f"Report saved as {filename}")