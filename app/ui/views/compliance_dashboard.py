from __future__ import annotations

from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget


class ComplianceDashboardView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Compliance Dashboard"))
        self.violations_list = QListWidget()
        layout.addWidget(self.violations_list)

    def show_violations(self, violations: list[dict]) -> None:
        self.violations_list.clear()
        if not violations:
            self.violations_list.addItem("No hard-rule violations.")
            return
        for v in violations:
            text = f"[{v.get('rule_id')}] {v.get('message')} @ {v.get('location')}"
            self.violations_list.addItem(text)

