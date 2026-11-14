from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QLabel, QMessageBox,
    QInputDialog, QFrame,
)
from storage import load_known, save_known


class DevicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.devices = {}
        self.known = load_known()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        header = QLabel("Devices")
        header.setStyleSheet("font-size: 26px; font-weight: 800;")
        layout.addWidget(header)

        row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔎  Filter by IP, MAC, vendor, status…")
        self.search.textChanged.connect(self.populate)
        row.addWidget(self.search, 1)

        trust_btn = QPushButton("✅  Trust")
        trust_btn.clicked.connect(self.trust_selected)
        row.addWidget(trust_btn)

        untrust_btn = QPushButton("🗑  Untrust")
        untrust_btn.clicked.connect(self.untrust_selected)
        row.addWidget(untrust_btn)
        layout.addLayout(row)

        body = QHBoxLayout()

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["IP", "MAC", "Vendor", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.show_detail)
        body.addWidget(self.table, 3)

        self.detail = QFrame()
        self.detail.setStyleSheet(
            "QFrame { background: #313244; border-radius: 10px; }"
        )
        self.detail.setFixedWidth(280)
        dv = QVBoxLayout(self.detail)
        dv.setContentsMargins(16, 16, 16, 16)
        dv.addWidget(QLabel("Device details"))
        self.detail_text = QLabel("Select a device…")
        self.detail_text.setWordWrap(True)
        dv.addWidget(self.detail_text)
        dv.addStretch(1)
        body.addWidget(self.detail, 1)

        layout.addLayout(body)

    def update_devices(self, devices):
        self.devices = devices
        self.known = load_known()
        self.populate()

    def populate(self):
        q = self.search.text().lower()
        self.table.setRowCount(0)
        for mac, info in sorted(self.devices.items(), key=lambda x: x[1]["ip"] or ""):
            name = self.known.get(mac)
            status = f"Trusted ({name})" if name else "⚠️ UNKNOWN"
            haystack = f"{info['ip']} {mac} {info['vendor']} {status}".lower()
            if q and q not in haystack:
                continue
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, text in enumerate([info["ip"], mac, info["vendor"], status]):
                item = QTableWidgetItem(text)
                if not name:
                    item.setForeground(QColor("#f38ba8"))
                self.table.setItem(row, col, item)

    def show_detail(self):
        row = self.table.currentRow()
        if row < 0:
            return
        ip = self.table.item(row, 0).text()
        mac = self.table.item(row, 1).text()
        vendor = self.table.item(row, 2).text()
        status = self.table.item(row, 3).text()
        self.detail_text.setText(
            f"<b>IP:</b> {ip}<br>"
            f"<b>MAC:</b> {mac}<br>"
            f"<b>Vendor:</b> {vendor}<br>"
            f"<b>Status:</b> {status}"
        )

    def selected_mac(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No selection", "Select a device first.")
            return None
        return self.table.item(row, 1).text()

    def trust_selected(self):
        mac = self.selected_mac()
        if not mac:
            return
        name, ok = QInputDialog.getText(self, "Trust device", f"Name for {mac}:")
        if ok and name.strip():
            self.known[mac] = name.strip()
            save_known(self.known)
            self.populate()

    def untrust_selected(self):
        mac = self.selected_mac()
        if not mac:
            return
        if mac in self.known:
            del self.known[mac]
            save_known(self.known)
            self.populate()