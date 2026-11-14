from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setAlignment(Qt.AlignCenter)

        title = QLabel("🛡️  WiFi Intruder Detector")
        title.setStyleSheet("font-size: 28px; font-weight: 800;")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        sub = QLabel(
            "Version 1.0.0\n\n"
            "A desktop tool to scan your home WiFi\n"
            "and flag unauthorized devices.\n\n"
            "Runs on Linux • Windows • macOS"
        )
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #a6adc8; font-size: 13px;")
        v.addWidget(sub)

        dev = QLabel("Developed by Abdul Hamid")
        dev.setAlignment(Qt.AlignCenter)
        dev.setStyleSheet(
            "color: #89b4fa; font-size: 16px; font-weight: 700; margin-top: 24px;"
        )
        v.addWidget(dev)

        warn = QLabel("⚠️  Only scan networks you own.")
        warn.setAlignment(Qt.AlignCenter)
        warn.setStyleSheet("color: #f38ba8; font-size: 12px; margin-top: 16px;")
        v.addWidget(warn)