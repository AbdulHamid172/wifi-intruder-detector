DARK_QSS = """
QMainWindow, QWidget { background: #1e1e2e; color: #cdd6f4; }
QLabel { color: #cdd6f4; }
QPushButton {
    background: #313244; color: #cdd6f4;
    border: 1px solid #45475a; border-radius: 6px;
    padding: 8px 16px; font-weight: 600;
}
QPushButton:hover { background: #45475a; }
QPushButton:pressed { background: #585b70; }
QPushButton:disabled { background: #26263a; color: #6c7086; }
QPushButton#primary { background: #89b4fa; color: #1e1e2e; }
QPushButton#primary:hover { background: #b4c8ff; }
QLineEdit {
    background: #313244; border: 1px solid #45475a;
    border-radius: 6px; padding: 6px; color: #cdd6f4;
}
QTableWidget {
    background: #181825; gridline-color: #313244;
    border: 1px solid #313244; border-radius: 6px;
}
QHeaderView::section {
    background: #313244; color: #cdd6f4;
    padding: 6px; border: none; font-weight: 600;
}
QTableWidget::item:selected { background: #45475a; }
QListWidget {
    background: #181825; border: none; padding: 8px;
}
QListWidget::item {
    padding: 12px; border-radius: 6px; margin: 2px 4px;
}
QListWidget::item:selected { background: #313244; color: #89b4fa; }
QStatusBar { background: #181825; color: #a6adc8; }
QProgressBar {
    background: #313244; border: none; border-radius: 4px; height: 8px;
}
QProgressBar::chunk { background: #89b4fa; border-radius: 4px; }
"""