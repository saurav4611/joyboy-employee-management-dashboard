from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QStatusBar, QFrame
from ui.components.sidebar import Sidebar
from ui.dashboard import DashboardPage
from ui.employees import EmployeesPage
from ui.attendance import AttendancePage
from ui.reports import ReportsPage
from utils.logger import get_logger

logger = get_logger("ui.main_window")

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("JoyBoy Flow - Employee Management Dashboard")
        self.setMinimumSize(1280, 780)
        self._build_ui()
        self._on_page_changed(0)  # Initialize with dashboard

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        layout.addWidget(self.sidebar)

        content_frame = QFrame()
        content_frame.setObjectName("contentArea")
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.content_stack = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.employees_page = EmployeesPage()
        self.attendance_page = AttendancePage()
        self.reports_page = ReportsPage()

        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.employees_page)
        self.content_stack.addWidget(self.attendance_page)
        self.content_stack.addWidget(self.reports_page)

        content_layout.addWidget(self.content_stack)
        layout.addWidget(content_frame, 1)

        self.setStatusBar(QStatusBar())

    def _on_page_changed(self, index: int) -> None:
        self.content_stack.setCurrentIndex(index)
        if index == 0:
            self.dashboard_page.refresh()
        elif index == 1:
            self.employees_page.refresh()
        elif index == 2:
            self.attendance_page.refresh()
        elif index == 3:
            self.reports_page.refresh()