from __future__ import annotations

from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class LayoutWorkspaceView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Layout Workspace (2D/3D placeholder)"))

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Candidate", "Feasible", "Fitness", "GM", "Stress"])
        layout.addWidget(self.table)

    def set_layout_rows(self, rows: list[dict]) -> None:
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row.get("id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(row.get("feasible", False))))
            self.table.setItem(i, 2, QTableWidgetItem(f"{float(row.get('fitness', 0.0)):.3f}"))
            self.table.setItem(i, 3, QTableWidgetItem(str(row.get("gm", ""))))
            self.table.setItem(i, 4, QTableWidgetItem(str(row.get("stress_index", ""))))

