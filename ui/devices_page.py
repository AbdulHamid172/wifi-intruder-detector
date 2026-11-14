import csv
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QLabel, QMessageBox,
    QInputDialog, QFrame, QFileDialog,
)
from storage import (
    load_known, save_known, update_seen, trust_device,
    untrust_device, friendly_time,
)


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

        # --- Search + actions ---
        row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔎  Filter by IP, MAC, hostname, vendor, status…")
        self.search.textChanged.connect(self.populate)
        row.addWidget(self.search, 1)

        trust_btn = QPushButton("✅  Trust")
        trust_btn.clicked.connect(self.trust_selected)
        row.addWidget(trust_btn)

        untrust_btn = QPushButton("🗑  Untrust")
        untrust_btn.clicked.connect(self.untrust_selected)
        row.addWidget(untrust_btn)

        export_btn = QPushButton("📤  Export CSV")
        export_btn.clicked.connect(self.export_csv)
        row.addWidget(export_btn)
        layout.addLayout(row)

        # --- Table + detail ---
        body = QHBoxLayout()

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["IP", "MAC", "Hostname", "Vendor", "Status", "Last seen"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
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

    # ---------- data update ----------
    def update_devices(self, devices):
        self.devices = devices
        self.known = load_known()
        self.known = update_seen(self.known, devices.keys())
        save_known(self.known)
        self.populate()

    def populate(self):
        q = self.search.text().lower()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for mac, info in self.devices.items():
            entry = self.known.get(mac, {})
            name = entry.get("name") if isinstance(entry, dict) else entry
            status = f"Trusted ({name})" if name else "⚠️ UNKNOWN"
            last_seen = friendly_time(
                entry.get("last_seen") if isinstance(entry, dict) else None
            )
            hostname = info.get("hostname") or "—"
            vendor = info.get("vendor") or "—"

            haystack = f"{info['ip']} {mac} {hostname} {vendor} {status}".lower()
            if q and q not in haystack:
                continue

            r = self.table.rowCount()
            self.table.insertRow(r)
            values = [info["ip"], mac, hostname, vendor, status, last_seen]
            for c, text in enumerate(values):
                item = QTableWidgetItem(text)
                if not name:
                    item.setForeground(QColor("#f38ba8"))
                self.table.setItem(r, c, item)

        self.table.setSortingEnabled(True)

    def show_detail(self):
        row = self.table.currentRow()
        if row < 0:
            return
        ip      = self.table.item(row, 0).text()
        mac     = self.table.item(row, 1).text()
        host    = self.table.item(row, 2).text()
        vendor  = self.table.item(row, 3).text()
        status  = self.table.item(row, 4).text()
        entry = self.known.get(mac, {})
        first_seen = friendly_time(
            entry.get("first_seen") if isinstance(entry, dict) else None
        )
        last_seen = friendly_time(
            entry.get("last_seen") if isinstance(entry, dict) else None
        )
        self.detail_text.setText(
            f"<b>IP:</b> {ip}<br>"
            f"<b>MAC:</b> {mac}<br>"
            f"<b>Hostname:</b> {host}<br>"
            f"<b>Vendor:</b> {vendor}<br>"
            f"<b>Status:</b> {status}<br><br>"
            f"<b>First seen:</b> {first_seen}<br>"
            f"<b>Last seen:</b> {last_seen}"
        )

    # ---------- actions ----------
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
            self.known = trust_device(self.known, mac, name.strip())
            save_known(self.known)
            self.populate()

    def untrust_selected(self):
        mac = self.selected_mac()
        if not mac:
            return
        self.known = untrust_device(self.known, mac)
        save_known(self.known)
        self.populate()

    def export_csv(self):
        if not self.devices:
            QMessageBox.information(self, "Nothing to export",
                                    "Run a scan first.")
            return
        default = f"wifi_scan_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", default, "CSV (*.csv)"
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["IP", "MAC", "Hostname", "Vendor",
                            "Status", "Trusted Name",
                            "First Seen", "Last Seen"])
                for mac, info in sorted(
                    self.devices.items(),
                    key=lambda x: x[1]["ip"] or "",
                ):
                    entry = self.known.get(mac, {})
                    name = entry.get("name") if isinstance(entry, dict) else entry
                    status = "Trusted" if name else "UNKNOWN"
                    w.writerow([
                        info["ip"], mac,
                        info.get("hostname") or "",
                        info.get("vendor") or "",
                        status, name or "",
                        friendly_time(entry.get("first_seen") if isinstance(entry, dict) else None),
                        friendly_time(entry.get("last_seen") if isinstance(entry, dict) else None),
                    ])
            QMessageBox.information(self, "Exported", f"Saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export failed", str(e))
