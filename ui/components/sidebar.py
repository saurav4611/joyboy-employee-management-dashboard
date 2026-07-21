from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QButtonGroup, QSpacerItem, QSizePolicy

class Sidebar(QFrame):
    page_changed = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(240)
        self._buttons = []
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(0)

        title = QLabel("JoyBoy Flow")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        nav_items = [("Dashboard", 0), ("Employees", 1), ("Attendance", 2), ("Reports", 3)]
        for label, idx in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, i=idx: self._on_nav_clicked(i))
            self._button_group.addButton(btn, idx)
            self._buttons.append(btn)
            layout.addWidget(btn)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self._buttons[0].setChecked(True)

    def _on_nav_clicked(self, index: int) -> None:
        self.page_changed.emit(index)