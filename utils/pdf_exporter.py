from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from utils.logger import get_logger

logger = get_logger("utils.pdf_exporter")

class PDFExporter:
    @staticmethod
    def _get_styles() -> dict:
        styles = getSampleStyleSheet()
        
        # Yahan ParagraphStyle use kiya hai dict ki jagah
        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor("#1e1e2e"),
            spaceAfter=10
        ))
        styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor("#6c7086"),
            spaceAfter=20
        ))
        return styles

    @staticmethod
    def _get_table_style() -> TableStyle:
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e1e2e")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f9fa")),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#313244")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#e9ecef")]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ])

    @staticmethod
    def export_employees(file_path: str, data: list[dict]) -> bool:
        try:
            doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            styles = PDFExporter._get_styles()
            elements = []

            elements.append(Paragraph("Employee Directory", styles['ReportTitle']))
            elements.append(Paragraph(f"Total Employees: {len(data)}", styles['ReportSubtitle']))
            elements.append(Spacer(1, 0.2 * inch))

            headers = ["Code", "Full Name", "Department", "Position", "Email", "Phone", "Status"]
            table_data = [headers]

            for emp in data:
                table_data.append([
                    str(emp.get("employee_code", "")),
                    str(emp.get("full_name", "")),
                    str(emp.get("department", "")),
                    str(emp.get("position", "")),
                    str(emp.get("email", "")),
                    str(emp.get("phone", "")),
                    str(emp.get("status_label", ""))
                ])

            col_widths = [0.8*inch, 1.5*inch, 1.5*inch, 1.5*inch, 2.5*inch, 1.2*inch, 0.8*inch]
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(PDFExporter._get_table_style())
            elements.append(table)

            doc.build(elements)
            logger.info("Employee PDF exported successfully to %s", file_path)
            return True
        except Exception as e:
            logger.error("Failed to export employee PDF: %s", str(e), exc_info=True)
            return False

    @staticmethod
    def export_attendance(file_path: str, data: list[dict]) -> bool:
        try:
            doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            styles = PDFExporter._get_styles()
            elements = []

            elements.append(Paragraph("Attendance History", styles['ReportTitle']))
            elements.append(Paragraph(f"Total Records: {len(data)}", styles['ReportSubtitle']))
            elements.append(Spacer(1, 0.2 * inch))

            headers = ["Date", "Employee", "Department", "Status", "Notes"]
            table_data = [headers]

            for rec in data:
                table_data.append([
                    str(rec.get("date", "")),
                    str(rec.get("employee_name", "")),
                    str(rec.get("department", "")),
                    str(rec.get("status_label", "")),
                    str(rec.get("notes", ""))
                ])

            col_widths = [1.2*inch, 2.0*inch, 1.5*inch, 1.0*inch, 3.5*inch]
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(PDFExporter._get_table_style())
            elements.append(table)

            doc.build(elements)
            logger.info("Attendance PDF exported successfully to %s", file_path)
            return True
        except Exception as e:
            logger.error("Failed to export attendance PDF: %s", str(e), exc_info=True)
            return False