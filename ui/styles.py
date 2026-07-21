STYLESHEET = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}
QMainWindow {
    background-color: #1e1e2e;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #585b70;
}
QPushButton:pressed {
    background-color: #181825;
}
QPushButton#primaryButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
    font-weight: 600;
}
QPushButton#dangerButton {
    background-color: #f38ba8;
    color: #1e1e2e;
    border: none;
    font-weight: 600;
}
QPushButton#successButton {
    background-color: #a6e3a1;
    color: #1e1e2e;
    border: none;
    font-weight: 600;
}
QLabel#pageTitle {
    color: #cdd6f4;
    font-size: 24px;
    font-weight: bold;
}
QLabel#pageSubtitle {
    color: #6c7086;
    font-size: 13px;
    padding-bottom: 8px;
}
QFrame#sidebar {
    background-color: #181825;
    border-right: 1px solid #313244;
}
QLabel#appTitle {
    color: #89b4fa;
    font-size: 20px;
    font-weight: bold;
    padding: 8px 0px;
}
QPushButton#navButton {
    text-align: left;
    padding: 14px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #a6adc8;
    background: transparent;
    margin: 2px 8px;
}
QPushButton#navButton:hover {
    background-color: #313244;
    color: #cdd6f4;
}
QPushButton#navButton:checked {
    background-color: #313244;
    color: #89b4fa;
    border-left: 3px solid #89b4fa;
}
QFrame#statCardAccent {
    background-color: #313244;
    border-radius: 12px;
    border-left: 4px solid #89b4fa;
}
QLabel#statTitle {
    color: #a6adc8;
    font-size: 12px;
    font-weight: 500;
}
QLabel#statValue {
    color: #cdd6f4;
    font-size: 32px;
    font-weight: bold;
}
QLabel#statSubtitle {
    color: #6c7086;
    font-size: 11px;
}
QTableView {
    background-color: #313244;
    alternate-background-color: #2a2a3c;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
    gridline-color: #45475a;
    selection-background-color: #45475a;
}
QHeaderView::section {
    background-color: #181825;
    color: #a6adc8;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid #45475a;
    font-weight: 600;
    font-size: 12px;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QDateEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus, QDateEdit:focus {
    border: 1px solid #89b4fa;
}
"""