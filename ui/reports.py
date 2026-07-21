from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QPushButton, QFileDialog, QMessageBox
)
from controllers.reports_controller import ReportsController
from utils.logger import get_logger

logger = get_logger("ui.reports")

class ReportCard(QFrame):
    def __init__(self, title: str, description: str, button_text: str, icon: str, accent_color: str, on_click) -> None:
        super().__init__()
        self.setObjectName("statCardAccent")
        self.setStyleSheet(f"QFrame#statCardAccent {{ border-left: 4px solid {accent_color}; }}")
        self._build_ui(title, description, button_text, icon, accent_color, on_click)

    def _build_ui(self, title: str, description: str, button_text: str, icon: str, accent_color: str, on_click) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        top = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {accent_color}; font-size: 32px;")
        top.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #cdd6f4;")
        top.addWidget(title_label)
        top.addStretch()
        layout.addLayout(top)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #a6adc8; font-size: 13px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()

        btn = QPushButton(button_text)
        btn.setObjectName("primaryButton")
        btn.setMinimumHeight(40)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(on_click)
        layout.addWidget(btn)

class ReportsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        title = QLabel("Reports")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Export employee and attendance data to PDF and Excel formats")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        # Employee Exports
        emp_header = QLabel("Employee Reports")
        emp_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #cdd6f4; padding-top: 10px;")
        layout.addWidget(emp_header)

        emp_cards_layout = QHBoxLayout()
        emp_cards_layout.setSpacing(16)

        pdf_card = ReportCard(
            "Employee PDF", 
            "Export the full employee directory to a professionally formatted PDF document.",
            "Export to PDF", "\u25A4", "#f38ba8",
            self.on_export_employee_pdf
        )
        emp_cards_layout.addWidget(pdf_card)

        excel_card = ReportCard(
            "Employee Excel", 
            "Export the full employee directory to an Excel spreadsheet for data processing.",
            "Export to Excel", "\u25A6", "#a6e3a1",
            self.on_export_employee_excel
        )
        emp_cards_layout.addWidget(excel_card)

        layout.addLayout(emp_cards_layout)

        # Attendance Exports
        att_header = QLabel("Attendance Reports")
        att_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #cdd6f4; padding-top: 20px;")
        layout.addWidget(att_header)

        att_cards_layout = QHBoxLayout()
        att_cards_layout.setSpacing(16)

        att_pdf_card = ReportCard(
            "Attendance PDF", 
            "Export the last 30 days of attendance history to a PDF document.",
            "Export to PDF", "\u25C9", "#89b4fa",
            self.on_export_attendance_pdf
        )
        att_cards_layout.addWidget(att_pdf_card)

        # Add an empty spacer card to maintain grid alignment if needed
        spacer_card = QFrame()
        spacer_card.setVisible(False)
        att_cards_layout.addWidget(spacer_card)

        layout.addLayout(att_cards_layout)
        layout.addStretch()

    def refresh(self) -> None:
        pass

    def _save_file(self, default_name: str, file_filter: str) -> str | None:
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", default_name, file_filter)
        return file_path if file_path else None

    def on_export_employee_pdf(self) -> None:
        file_path = self._save_file("employees.pdf", "PDF Files (*.pdf)")
        if file_path:
            if ReportsController.generate_employee_pdf(file_path):
                QMessageBox.information(self, "Success", f"Employee PDF exported successfully to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to export Employee PDF.")

    def on_export_employee_excel(self) -> None:
        file_path = self._save_file("employees.xlsx", "Excel Files (*.xlsx)")
        if file_path:
            if ReportsController.generate_employee_excel(file_path):
                QMessageBox.information(self, "Success", f"Employee Excel exported successfully to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to export Employee Excel.")

    def on_export_attendance_pdf(self) -> None:
        file_path = self._save_file("attendance_history.pdf", "PDF Files (*.pdf)")
        if file_path:
            if ReportsController.generate_attendance_pdf(file_path):
                QMessageBox.information(self, "Success", f"Attendance PDF exported successfully to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to export Attendance PDF.")