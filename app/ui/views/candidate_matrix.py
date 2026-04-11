from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CandidateMatrixView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("ENGINEERING CANDIDATE MATRIX")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Comparative vector analysis for structural feasibility and metacentric stability.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        root.addLayout(header)

        mtx_card = QFrame()
        mtx_card.setProperty("card", True)
        mtx_layout = QVBoxLayout(mtx_card)
        mtx_layout.setContentsMargins(20, 20, 20, 20)
        mtx_layout.setSpacing(16)
        
        self.table = QTableWidget(12, 6)
        self.table.setHorizontalHeaderLabels([
            "VECTOR_ID", "FEASIBILITY", "FITNESS_SCORE", 
            "METACENTRIC_HEIGHT", "STRESS_INDEX", "DYNAMICS"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        
        sample = [
            ("V-201_NOMINAL", "READY", "0.917", "1.21m", "0.29", "STABLE"),
            ("V-198_OPTIMAL", "READY", "0.904", "1.18m", "0.33", "STABLE"),
            ("V-194_CONFLICT", "REJECT", "0.851", "0.74m", "0.58", "WARNING"),
            ("V-188_NOMINAL", "READY", "0.844", "1.02m", "0.41", "STABLE"),
            ("V-181_CONFLICT", "REJECT", "0.807", "0.68m", "0.62", "CRITICAL"),
            ("V-176_NOMINAL", "READY", "0.801", "1.09m", "0.49", "STABLE"),
            ("V-169_CONFLICT", "REJECT", "0.775", "0.61m", "0.64", "WARNING"),
            ("V-161_NOMINAL", "READY", "0.761", "0.92m", "0.52", "STABLE"),
        ]
        
        mono_font = QFont("Consolas")
        for r, cols in enumerate(sample):
            for c, val in enumerate(cols):
                item = QTableWidgetItem(val)
                item.setFont(mono_font)
                if c == 1:
                    item.setForeground(Qt.green if val == "READY" else Qt.red)
                if c == 5:
                    if val == "CRITICAL": item.setForeground(Qt.red)
                    elif val == "WARNING": item.setForeground(Qt.yellow)
                    else: item.setForeground(Qt.green)
                self.table.setItem(r, c, item)

        mtx_layout.addWidget(self.table)
        root.addWidget(mtx_card)

        btns = QHBoxLayout()
        btns.addWidget(QPushButton("EXPORT_CSV"))
        btns.addWidget(QPushButton("AUTO_SELECT_BEST"))
        btns.addStretch()
        btns.addWidget(QPushButton("FILTER_BY_FITNESS"))
        root.addLayout(btns)
