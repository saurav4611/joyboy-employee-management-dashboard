from datetime import date
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QComboBox, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QTabWidget, QSpinBox
)
from controllers.attendance_controller import AttendanceController
from controllers.employee_controller import EmployeeController
from utils.logger import get_logger
from utils.error_handler import JoyBoyError

logger = get_logger("ui.attendance")

class AttendancePage(QWidget):
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
        title = QLabel("Attendance")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Track and manage employee attendance")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        # Quick Marking Section
        mark_frame = QFrame()
        mark_frame.setObjectName("statCardAccent")
        mark_layout = QHBoxLayout(mark_frame)
        mark_layout.setContentsMargins(20, 15, 20, 15)
        
        self.emp_combo = QComboBox()
        self.emp_combo.setMinimumWidth(300)
        mark_layout.addWidget(QLabel("Employee:"))
        mark_layout.addWidget(self.emp_combo, 1)
        
        mark_layout.addSpacing(15)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        mark_layout.addWidget(QLabel("Date:"))
        mark_layout.addWidget(self.date_edit)
        
        mark_layout.addSpacing(15)
        
        self.btn_present = QPushButton("Mark Present")
        self.btn_present.setObjectName("successButton")
        self.btn_present.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_present.clicked.connect(self.on_mark_present)
        mark_layout.addWidget(self.btn_present)
        
        self.btn_absent = QPushButton("Mark Absent")
        self.btn_absent.setObjectName("dangerButton")
        self.btn_absent.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_absent.clicked.connect(self.on_mark_absent)
        mark_layout.addWidget(self.btn_absent)
        
        layout.addWidget(mark_frame)

        # Tabs for History and Summary
        self.tabs = QTabWidget()
        
        # History Tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Date", "Employee", "Department", "Status", "Notes"])
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        history_layout.addWidget(self.history_table)
        self.tabs.addTab(history_tab, "Recent History (30 Days)")

        # Summary Tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout(summary_tab)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Year:"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(date.today().year)
        filter_layout.addWidget(self.year_spin)
        
        filter_layout.addSpacing(10)
        
        filter_layout.addWidget(QLabel("Month:"))
        self.month_combo = QComboBox()
        for m in range(1, 13):
            self.month_combo.addItem(date(2000, m, 1).strftime("%B"), m)
        self.month_combo.setCurrentIndex(date.today().month - 1)
        filter_layout.addWidget(self.month_combo)
        
        filter_layout.addStretch()
        
        self.btn_refresh_summary = QPushButton("Refresh Summary")
        self.btn_refresh_summary.setObjectName("primaryButton")
        self.btn_refresh_summary.clicked.connect(self.load_monthly_summary)
        filter_layout.addWidget(self.btn_refresh_summary)
        
        summary_layout.addLayout(filter_layout)
        
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(6)
        self.summary_table.setHorizontalHeaderLabels(["Code", "Name", "Department", "Present", "Absent", "Rate %"])
        self.summary_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.summary_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.summary_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        summary_layout.addWidget(self.summary_table)
        
        self.tabs.addTab(summary_tab, "Monthly Summary")
        
        layout.addWidget(self.tabs, 1)

    def refresh(self) -> None:
        self._load_employees()
        self.load_history()
        self.load_monthly_summary()

    def _load_employees(self) -> None:
        employees = EmployeeController.get_employees(active_only=True)
        self.emp_combo.clear()
        for emp in employees:
            self.emp_combo.addItem(f"{emp['full_name']} ({emp['employee_code']})", emp["id"])

    def load_history(self) -> None:
        records = AttendanceController.get_history(days=30)
        self.history_table.setRowCount(0)
        for row, rec in enumerate(records):
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(rec.get("date", "")))
            self.history_table.setItem(row, 1, QTableWidgetItem(rec.get("employee_name", "")))
            self.history_table.setItem(row, 2, QTableWidgetItem(rec.get("department", "")))
            
            status_item = QTableWidgetItem(rec.get("status_label", ""))
            if rec.get("status") == "present":
                status_item.setForeground(Qt.GlobalColor.green)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.history_table.setItem(row, 3, status_item)
            
            self.history_table.setItem(row, 4, QTableWidgetItem(rec.get("notes", "")))

    def load_monthly_summary(self) -> None:
        year = self.year_spin.value()
        month = self.month_combo.currentData()
        
        summaries = AttendanceController.get_monthly_summary(year, month)
        self.summary_table.setRowCount(0)
        for row, s in enumerate(summaries):
            self.summary_table.insertRow(row)
            self.summary_table.setItem(row, 0, QTableWidgetItem(s["employee_code"]))
            self.summary_table.setItem(row, 1, QTableWidgetItem(s["employee_name"]))
            self.summary_table.setItem(row, 2, QTableWidgetItem(s["department"]))
            self.summary_table.setItem(row, 3, QTableWidgetItem(str(s["present"])))
            self.summary_table.setItem(row, 4, QTableWidgetItem(str(s["absent"])))
            
            rate_item = QTableWidgetItem(f"{s['rate']:.1f}%")
            if s["rate"] >= 80:
                rate_item.setForeground(Qt.GlobalColor.green)
            elif s["rate"] >= 50:
                rate_item.setForeground(Qt.GlobalColor.yellow)
            else:
                rate_item.setForeground(Qt.GlobalColor.red)
            self.summary_table.setItem(row, 5, rate_item)

    def _mark(self, status: str) -> None:
        if self.emp_combo.count() == 0:
            QMessageBox.warning(self, "No Employees", "There are no active employees to mark attendance for.")
            return
            
        emp_id = self.emp_combo.currentData()
        qdate = self.date_edit.date()
        att_date = date(qdate.year(), qdate.month(), qdate.day())
        
        try:
            AttendanceController.mark_attendance(emp_id, att_date, status)
            self.refresh()  
            self.tabs.setCurrentIndex(0)  
            QMessageBox.information(self, "Success", f"Attendance marked as {status}.")
        except JoyBoyError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            logger.error("Failed to mark attendance: %s", str(e))
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")

    def on_mark_present(self) -> None:
        self._mark("present")

    def on_mark_absent(self) -> None:
        self._mark("absent")