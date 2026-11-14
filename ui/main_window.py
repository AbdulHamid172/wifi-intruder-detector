import sys
sys.path.append(".")

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QStatusBar,
)
from ui.dashboard import DashboardPage
from ui.devices_page import DevicesPage
from ui.settings_page import SettingsPage
from ui.about_page import AboutPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛡️  WiFi Intruder Detector")
        self.resize(1100, 720)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItems([
            "📊  Dashboard", "📱  Devices", "⚙️  Settings", "ℹ️  About",
        ])
        self.sidebar.currentRowChanged.connect(self.switch_page)
        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.pages = {
            "dashboard": DashboardPage(),
            "devices":   DevicesPage(),
            "settings":  SettingsPage(),
            "about":     AboutPage(),
        }
        for p in self.pages.values():
            self.stack.addWidget(p)
        root.addWidget(self.stack, 1)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready. Developed by Abdul Hamid.")

        self.pages["dashboard"].scan_finished.connect(
            self.pages["devices"].update_devices
        )

        self.sidebar.setCurrentRow(0)

    def switch_page(self, idx):
        self.stack.setCurrentIndex(idx)