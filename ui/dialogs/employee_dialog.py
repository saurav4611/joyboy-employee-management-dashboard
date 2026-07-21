from datetime import date
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, 
    QDoubleSpinBox, QDateEdit, QDialogButtonBox, QMessageBox, QCheckBox
)
from utils.logger import get_logger

logger = get_logger("ui.dialogs.employee_dialog")

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, departments: list[str] = None, employee_data: dict | None = None) -> None:
        super().__init__(parent)
        self.departments = departments or []
        self.employee_data = employee_data
        self.setWindowTitle("Add Employee" if not employee_data else "Edit Employee")
        self.setMinimumWidth(450)
        self._build_ui()
        if employee_data:
            self._populate_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g., EMP0001")
        
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        self.dept_input = QComboBox()
        self.dept_input.setEditable(True)
        self.dept_input.addItems(self.departments)
        
        self.position_input = QLineEdit()
        
        self.salary_input = QDoubleSpinBox()
        self.salary_input.setRange(0.0, 999999.99)
        self.salary_input.setPrefix("$ ")
        self.salary_input.setDecimals(2)
        
        self.hire_date_input = QDateEdit()
        self.hire_date_input.setCalendarPopup(True)
        self.hire_date_input.setDate(QDate.currentDate())
        self.hire_date_input.setDisplayFormat("yyyy-MM-dd")
        
        self.active_input = QCheckBox("Active")
        self.active_input.setChecked(True)

        form.addRow("Code*:", self.code_input)
        form.addRow("First Name*:", self.first_name_input)
        form.addRow("Last Name*:", self.last_name_input)
        form.addRow("Email*:", self.email_input)
        form.addRow("Phone:", self.phone_input)
        form.addRow("Department*:", self.dept_input)
        form.addRow("Position:", self.position_input)
        form.addRow("Salary:", self.salary_input)
        form.addRow("Hire Date:", self.hire_date_input)
        form.addRow("", self.active_input)
        
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Save")
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate_data(self) -> None:
        d = self.employee_data
        self.code_input.setText(d.get("employee_code", ""))
        self.first_name_input.setText(d.get("first_name", ""))
        self.last_name_input.setText(d.get("last_name", ""))
        self.email_input.setText(d.get("email", ""))
        self.phone_input.setText(d.get("phone", ""))
        
        dept = d.get("department", "")
        if dept:
            idx = self.dept_input.findText(dept)
            if idx >= 0:
                self.dept_input.setCurrentIndex(idx)
            else:
                self.dept_input.setEditText(dept)
                
        self.position_input.setText(d.get("position", ""))
        self.salary_input.setValue(d.get("salary", 0.0))
        
        hd = d.get("hire_date")
        if hd:
            if isinstance(hd, str):
                parts = hd.split("-")
                if len(parts) == 3:
                    self.hire_date_input.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
            elif isinstance(hd, date):
                self.hire_date_input.setDate(QDate(hd.year, hd.month, hd.day))
                
        self.active_input.setChecked(d.get("is_active", True))

    def _validate_and_accept(self) -> None:
        if not self.code_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Employee Code is required.")
            return
        if not self.first_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "First Name is required.")
            return
        if not self.last_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Last Name is required.")
            return
        if not self.email_input.text().strip() or "@" not in self.email_input.text():
            QMessageBox.warning(self, "Validation Error", "A valid Email is required.")
            return
        if not self.dept_input.currentText().strip():
            QMessageBox.warning(self, "Validation Error", "Department is required.")
            return
            
        self.accept()

    def get_data(self) -> dict:
        qdate = self.hire_date_input.date()
        py_date = date(qdate.year(), qdate.month(), qdate.day())
        
        return {
            "employee_code": self.code_input.text(),
            "first_name": self.first_name_input.text(),
            "last_name": self.last_name_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "department": self.dept_input.currentText(),
            "position": self.position_input.text(),
            "salary": self.salary_input.value(),
            "hire_date": py_date.isoformat(),
            "is_active": self.active_input.isChecked()
        }