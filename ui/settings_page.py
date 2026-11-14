import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
)
from storage import load_known


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(12)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 26px; font-weight: 800;")
        v.addWidget(title)

        v.addWidget(QLabel("Default subnet:"))
        self.subnet = QLineEdit("192.168.1.0/24")
        v.addWidget(self.subnet)

        export_btn = QPushButton("📤  Export known devices to JSON")
        export_btn.clicked.connect(self.export)
        v.addWidget(export_btn)

        v.addStretch(1)

    def export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export", "known_devices.json", "JSON (*.json)"
        )
        if path:
            with open(path, "w") as f:
                json.dump(load_known(), f, indent=2)