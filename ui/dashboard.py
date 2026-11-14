from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QProgressBar, QMessageBox,
)
from scanner import scan_network, detect_subnet
from storage import load_known
from notifier import notify


class ScanWorker(QThread):
    progress = Signal(str)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, subnet):
        super().__init__()
        self.subnet = subnet

    def run(self):
        try:
            devices = scan_network(self.subnet, progress_cb=self.progress.emit)
            self.finished.emit(devices)
        except Exception as e:
            self.error.emit(str(e))


class StatCard(QFrame):
    def __init__(self, title, value="0", color="#89b4fa"):
        super().__init__()
        self.setStyleSheet(
            "QFrame { background: #313244; border-radius: 10px; }"
            f"QLabel#value {{ color: {color}; font-size: 28px; font-weight: 800; }}"
            "QLabel#title { color: #a6adc8; font-size: 12px; }"
        )
        v = QVBoxLayout(self)
        v.setContentsMargins(16, 16, 16, 16)
        self.value_label = QLabel(value)
        self.value_label.setObjectName("value")
        title_label = QLabel(title)
        title_label.setObjectName("title")
        v.addWidget(self.value_label)
        v.addWidget(title_label)

    def set_value(self, val):
        self.value_label.setText(str(val))


class DashboardPage(QWidget):
    scan_finished = Signal(dict)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Dashboard")
        header.setStyleSheet("font-size: 26px; font-weight: 800; color: #cdd6f4;")
        layout.addWidget(header)

        # --- Stat cards ---
        cards = QHBoxLayout()
        self.total_card   = StatCard("Total devices", "0", "#89b4fa")
        self.trusted_card = StatCard("Trusted",       "0", "#a6e3a1")
        self.unknown_card = StatCard("Unknown ⚠️",    "0", "#f38ba8")
        cards.addWidget(self.total_card)
        cards.addWidget(self.trusted_card)
        cards.addWidget(self.unknown_card)
        layout.addLayout(cards)

        # --- Scan controls ---
        scan_row = QHBoxLayout()
        scan_row.addWidget(QLabel("Subnet:"))
        self.subnet_input = QLineEdit(detect_subnet() or "192.168.1.0/24")
        scan_row.addWidget(self.subnet_input, 1)
        self.scan_btn = QPushButton("🔍  Scan Network")
        self.scan_btn.setObjectName("primary")
        self.scan_btn.clicked.connect(self.start_scan)
        scan_row.addWidget(self.scan_btn)
        layout.addLayout(scan_row)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)   # indeterminate spinner
        self.progress.hide()
        layout.addWidget(self.progress)

        self.status = QLabel("")
        layout.addWidget(self.status)
        layout.addStretch(1)

    # ---------- scanning ----------
    def start_scan(self):
        subnet = self.subnet_input.text().strip()
        if not subnet:
            QMessageBox.warning(self, "No subnet",
                                "Enter a subnet like 192.168.1.0/24")
            return
        self.scan_btn.setEnabled(False)
        self.scan_btn.setText("Scanning…")
        self.progress.show()
        self.status.setText("Starting scan…")

        self.worker = ScanWorker(subnet)
        self.worker.progress.connect(self.status.setText)
        self.worker.finished.connect(self.on_done)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_error(self, msg):
        self._reset()
        QMessageBox.critical(self, "Scan failed", msg)

    def on_done(self, devices):
        self._reset()

        known = load_known()
        # A device is "trusted" only if it has a non-empty name.
        unknown = sum(
            1 for m in devices
            if not (known.get(m) or {}).get("name")
        )

        self.total_card.set_value(len(devices))
        self.trusted_card.set_value(len(devices) - unknown)
        self.unknown_card.set_value(unknown)
        self.status.setText(f"Scan complete — {len(devices)} device(s).")

        # Notify the user if strangers are on the network
        if unknown > 0:
            notify(
                "⚠️ WiFi Alert",
                f"{unknown} unknown device(s) on your network!",
            )

        self.scan_finished.emit(devices)

    def _reset(self):
        self.scan_btn.setEnabled(True)
        self.scan_btn.setText("🔍  Scan Network")
        self.progress.hide()
