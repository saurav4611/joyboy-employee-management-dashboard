from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QDialog
)
from controllers.employee_controller import EmployeeController
from ui.dialogs.employee_dialog import EmployeeDialog
from utils.logger import get_logger
from utils.error_handler import JoyBoyError

logger = get_logger("ui.employees")

class EmployeesPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self.refresh()

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
        layout.setSpacing(15)

        # Header
        title = QLabel("Employees")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Manage your organization's workforce")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        # Toolbar
        toolbar = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, email, or code...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.refresh)
        toolbar.addWidget(self.search_input)
        
        toolbar.addSpacing(10)
        
        self.dept_filter = QComboBox()
        self.dept_filter.addItem("All Departments")
        self.dept_filter.setMinimumWidth(200)
        self.dept_filter.currentTextChanged.connect(self.refresh)
        toolbar.addWidget(self.dept_filter)
        
        toolbar.addStretch()
        
        self.add_btn = QPushButton("+ Add Employee")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.on_add_employee)
        toolbar.addWidget(self.add_btn)
        
        layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Code", "Full Name", "Department", "Position", "Email", "Phone", "Status"])
        self.table.hideColumn(0)  # Hide ID
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.table, 1)

        # Action Buttons
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("primaryButton")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.clicked.connect(self.on_edit_employee)
        actions_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self.on_delete_employee)
        actions_layout.addWidget(self.delete_btn)
        
        layout.addLayout(actions_layout)

    def refresh(self) -> None:
        search = self.search_input.text().strip() or None
        dept = self.dept_filter.currentText()
        
        # Update departments in filter
        current_dept = self.dept_filter.currentText()
        self.dept_filter.blockSignals(True)
        self.dept_filter.clear()
        self.dept_filter.addItem("All Departments")
        departments = EmployeeController.get_departments()
        self.dept_filter.addItems(departments)
        if current_dept in departments or current_dept == "All Departments":
            self.dept_filter.setCurrentText(current_dept)
        self.dept_filter.blockSignals(False)
        
        employees = EmployeeController.get_employees(search=search, department=dept)
        
        self.table.setRowCount(0)
        for row, emp in enumerate(employees):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(emp["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(emp["employee_code"]))
            self.table.setItem(row, 2, QTableWidgetItem(emp["full_name"]))
            self.table.setItem(row, 3, QTableWidgetItem(emp["department"]))
            self.table.setItem(row, 4, QTableWidgetItem(emp.get("position", "")))
            self.table.setItem(row, 5, QTableWidgetItem(emp["email"]))
            self.table.setItem(row, 6, QTableWidgetItem(emp.get("phone", "")))
            
            status_item = QTableWidgetItem(emp["status_label"])
            if emp["is_active"]:
                status_item.setForeground(Qt.GlobalColor.green)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.table.setItem(row, 7, status_item)

    def on_add_employee(self) -> None:
        departments = EmployeeController.get_departments()
        dialog = EmployeeDialog(self, departments=departments)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                EmployeeController.create_employee(data)
                self.refresh()
                QMessageBox.information(self, "Success", "Employee added successfully.")
            except JoyBoyError as e:
                QMessageBox.warning(self, "Error", str(e))
            except Exception as e:
                logger.error("Failed to add employee: %s", str(e))
                QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")

    def on_edit_employee(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an employee to edit.")
            return
            
        row = selected[0].row()
        emp_id = int(self.table.item(row, 0).text())
        
        employees = EmployeeController.get_employees()
        emp_dict = next((e for e in employees if e["id"] == emp_id), None)
        if not emp_dict:
            QMessageBox.critical(self, "Error", "Could not find employee data.")
            return
            
        departments = EmployeeController.get_departments()
        dialog = EmployeeDialog(self, departments=departments, employee_data=emp_dict)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                EmployeeController.update_employee(emp_id, data)
                self.refresh()
                QMessageBox.information(self, "Success", "Employee updated successfully.")
            except JoyBoyError as e:
                QMessageBox.warning(self, "Error", str(e))
            except Exception as e:
                logger.error("Failed to update employee: %s", str(e))
                QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")

    def on_delete_employee(self) -> None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an employee to delete.")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this employee? This will also remove their attendance records.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            row = selected[0].row()
            emp_id = int(self.table.item(row, 0).text())
            try:
                EmployeeController.delete_employee(emp_id)
                self.refresh()
                QMessageBox.information(self, "Success", "Employee deleted successfully.")
            except JoyBoyError as e:
                QMessageBox.warning(self, "Error", str(e))
            except Exception as e:
                logger.error("Failed to delete employee: %s", str(e))
                QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")