import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, 
    QScrollArea, QGridLayout
)
from controllers.dashboard_controller import DashboardController
from ui.components.stat_card import StatCard
from utils.logger import get_logger

logger = get_logger("ui.dashboard")

# Configure pyqtgraph for dark theme
pg.setConfigOption("background", QColor("#313244"))
pg.setConfigOption("foreground", QColor("#a6adc8"))
pg.setConfigOption("antialias", True)

class DepartmentChart(pg.PlotWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(280)
        self.setMaximumHeight(320)
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=False, y=True, alpha=0.15)
        self.getAxis("left").setTextPen(QColor("#6c7086"))
        self.getAxis("bottom").setTextPen(QColor("#6c7086"))
        self.setLabel("left", "Employees", color="#a6adc8")
        self.setLabel("bottom", "Department", color="#a6adc8")

    def update_chart(self, data: list[tuple[str, int]]) -> None:
        self.clear()
        if not data:
            return
        departments = [d[0] for d in data]
        counts = [d[1] for d in data]
        x = list(range(len(departments)))
        
        bar_item = pg.BarGraphItem(
            x=x, height=counts, width=0.55,
            brush=QColor(137, 180, 250, 200),
            pen=pg.mkPen(QColor(180, 190, 254), width=1)
        )
        self.addItem(bar_item)
        
        ticks = [[(i, dept) for i, dept in enumerate(departments)]]
        self.getAxis("bottom").setTicks(ticks)
        
        max_count = max(counts) if counts else 1
        self.setYRange(0, max_count + max(1, max_count * 0.15))
        
        for i, count in enumerate(counts):
            text_item = pg.TextItem(str(count), color=QColor("#cdd6f4"), anchor=(0.5, 1.0))
            text_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            text_item.setPos(i, count + 0.3)
            self.addItem(text_item)

class AttendanceTrendChart(pg.PlotWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(280)
        self.setMaximumHeight(320)
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.hideButtons()
        self.showGrid(x=False, y=True, alpha=0.15)
        self.getAxis("left").setTextPen(QColor("#6c7086"))
        self.getAxis("bottom").setTextPen(QColor("#6c7086"))
        self.setLabel("left", "Present", color="#a6adc8")
        self.setLabel("bottom", "Date", color="#a6adc8")

    def update_chart(self, data: list[tuple[str, int]]) -> None:
        self.clear()
        if not data:
            return
        dates = [d[0] for d in data]
        counts = [d[1] for d in data]
        x = list(range(len(dates)))
        
        fill_brush = pg.mkBrush(QColor(166, 227, 161, 40))
        pen = pg.mkPen(QColor(166, 227, 161), width=2)
        
        self.plot(x, counts, pen=pen, fillLevel=0, brush=fill_brush)
        
        step = max(1, len(dates) // 6)
        ticks = [[(i, dates[i]) for i in range(0, len(dates), step)]]
        self.getAxis("bottom").setTicks(ticks)
        
        max_count = max(counts) if counts else 1
        self.setYRange(0, max_count + max(1, max_count * 0.15))

class DashboardPage(QWidget):
    def __init__(self, parent=None) -> None:
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

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Overview of your organization at a glance")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)
        
        self.card_total = StatCard("Total Employees", "0", "All registered", "\u25C8", "#89b4fa")
        self.card_active = StatCard("Active Employees", "0", "Currently employed", "\u25C9", "#a6e3a1")
        self.card_departments = StatCard("Departments", "0", "Distinct departments", "\u25A4", "#f9e2af")
        self.card_today = StatCard("Today's Attendance", "0", "Present today", "\u2713", "#f38ba8")
        
        cards_layout.addWidget(self.card_total, 0, 0)
        cards_layout.addWidget(self.card_active, 0, 1)
        cards_layout.addWidget(self.card_departments, 0, 2)
        cards_layout.addWidget(self.card_today, 0, 3)
        layout.addLayout(cards_layout)

        dept_label = QLabel("Employee Distribution by Department")
        dept_label.setObjectName("pageTitle")
        dept_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(dept_label)
        
        self.dept_chart = DepartmentChart()
        layout.addWidget(self.dept_chart)

        trend_label = QLabel("Attendance Trend (Last 30 Days)")
        trend_label.setObjectName("pageTitle")
        trend_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(trend_label)
        
        self.trend_chart = AttendanceTrendChart()
        layout.addWidget(self.trend_chart)

    def refresh(self) -> None:
        data = DashboardController.get_dashboard_data()
        self.card_total.set_value(str(data.get("total_employees", 0)))
        self.card_active.set_value(str(data.get("active_employees", 0)))
        self.card_departments.set_value(str(data.get("department_count", 0)))
        self.card_today.set_value(str(data.get("today_attendance", 0)))
        self.dept_chart.update_chart(data.get("department_distribution", []))
        self.trend_chart.update_chart(data.get("attendance_trend", []))