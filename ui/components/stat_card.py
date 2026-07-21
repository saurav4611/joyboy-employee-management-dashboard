from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

class StatCard(QFrame):
    def __init__(self, title: str = "", value: str = "0", subtitle: str = "", icon: str = "", accent_color: str = "#89b4fa", parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statCardAccent")
        self._accent_color = accent_color
        self._build_ui(title, value, subtitle, icon)

    def _build_ui(self, title: str, value: str, subtitle: str, icon: str) -> None:
        self.setStyleSheet(f"QFrame#statCardAccent {{ border-left: 4px solid {self._accent_color}; }}")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        top_row = QHBoxLayout()
        self._title_label = QLabel(title)
        self._title_label.setObjectName("statTitle")
        top_row.addWidget(self._title_label)
        top_row.addStretch()
        
        self._icon_label = QLabel(icon)
        self._icon_label.setObjectName("statIcon")
        self._icon_label.setStyleSheet(f"color: {self._accent_color}; font-size: 28px;")
        top_row.addWidget(self._icon_label)
        layout.addLayout(top_row)

        self._value_label = QLabel(value)
        self._value_label.setObjectName("statValue")
        layout.addWidget(self._value_label)

        self._subtitle_label = QLabel(subtitle)
        self._subtitle_label.setObjectName("statSubtitle")
        layout.addWidget(self._subtitle_label)

    def set_value(self, value: str) -> None:
        self._value_label.setText(value)