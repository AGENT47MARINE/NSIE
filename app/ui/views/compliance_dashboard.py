from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ComplianceDashboardView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("COMPLIANCE & AUDIT TERMINAL")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Cross-referencing candidate vector sets against international regulatory archives (SOLAS, MARPOL).")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        btn_report = QPushButton("GENERATE ARCHIVE REPORT")
        btn_report.setProperty("accent", True)
        header.addWidget(btn_report, 0, Qt.AlignBottom)
        root.addLayout(header)

        filters = QHBoxLayout()
        filters.setSpacing(16)
        
        def create_filter_lbl(txt):
            l = QLabel(txt.upper())
            l.setStyleSheet("color: #4a5a6a; font-size: 9px; font-weight: 800; letter-spacing: 1px;")
            return l

        domain = QComboBox()
        domain.addItems(["ALL_DOMAINS", "SOLAS_ST_7", "MARPOL_V22", "CLASS_RULES", "MIL_SPEC_08"])
        severity = QComboBox()
        severity.addItems(["ALL_SEVERITIES", "CRITICAL_ONLY", "HIGH_ONLY", "ADVISORY"])
        
        filters.addWidget(create_filter_lbl("Filter Domain"))
        filters.addWidget(domain)
        filters.addWidget(create_filter_lbl("Filter Severity"))
        filters.addWidget(severity)
        filters.addStretch()
        filters.addWidget(QPushButton("REFRESH_AUDIT"))
        root.addLayout(filters)

        split = QSplitter()
        split.setHandleWidth(1)
        split.setStyleSheet("QSplitter::handle { background: #1a2533; }")

        # Main Matrix
        matrix_card = QFrame()
        matrix_card.setProperty("card", True)
        matrix_layout = QVBoxLayout(matrix_card)
        matrix_layout.setContentsMargins(20, 20, 20, 20)
        matrix_layout.setSpacing(16)
        
        mtx_hdr = QLabel("REGULATORY OUTCOME MATRIX")
        mtx_hdr.setProperty("heading", "h2")
        matrix_layout.addWidget(mtx_hdr)

        self.matrix = QTableWidget(10, 4)
        self.matrix.setHorizontalHeaderLabels(["VECTOR_ID", "CANDIDATE", "OUTCOME", "EVIDENCE_STRING"])
        self.matrix.horizontalHeader().setStretchLastSection(True)
        
        rows = [
            ("SOLAS_EGRESS_001", "V-201", "PASS", "CORRIDOR: 1.32m"),
            ("MARPOL_TANK_001", "V-201", "PASS", "SPACING: 0.9m"),
            ("CLASS_GM_001", "V-201", "PASS", "GM: 1.21"),
            ("FIRE_ZONE_006", "V-201", "FLAG", "ZONE_CONFLICT: B3"),
            ("SOLAS_EGRESS_001", "V-194", "FAIL", "CORRIDOR: 1.05m"),
            ("MARPOL_TANK_001", "V-194", "PASS", "SPACING: 0.82m"),
            ("CLASS_GM_001", "V-194", "FAIL", "GM: 0.74"),
            ("CARGO_CLEAR_011", "V-194", "FAIL", "CLEARANCE: 0.5m"),
            ("STRUCT_LOAD_09", "V-188", "PASS", "STRESS: 0.41"),
            ("NAV_OPS_RANGE", "V-188", "PASS", "REACH: 4200nm"),
        ]
        mono_font = QFont("Consolas")
        for r, cols in enumerate(rows):
            for c, val in enumerate(cols):
                item = QTableWidgetItem(val)
                item.setFont(mono_font)
                if c == 2:
                    if val == "PASS": item.setForeground(Qt.green)
                    elif val == "FAIL": item.setForeground(Qt.red)
                    else: item.setForeground(Qt.yellow)
                self.matrix.setItem(r, c, item)

        matrix_layout.addWidget(self.matrix)
        split.addWidget(matrix_card)

        # Side: Violations list
        side_card = QFrame()
        side_card.setProperty("card", True)
        side_layout = QVBoxLayout(side_card)
        side_layout.setContentsMargins(20, 20, 20, 20)
        side_layout.setSpacing(16)
        
        v_hdr = QLabel("VIOLATION_STREAM")
        v_hdr.setProperty("heading", "h2")
        side_layout.addWidget(v_hdr)

        self.violations_list = QListWidget()
        self.violations_list.setStyleSheet("""
            QListWidget {
                background: #020406;
                border: 1px solid #1a2533;
                border-radius: 6px;
                color: #ff3b30;
                font-family: 'Consolas';
                font-size: 10px;
                padding: 10px;
            }
        """)
        self.violations_list.addItems(
            [
                ">> [FIRE_ZONE_006] OVERLAP DETECTED @ B3",
                ">> [CLASS_GM_001] CRITICAL GM UNDERFLOW",
                ">> [CARGO_CLEAR_011] CLEARANCE BREACH @ L_A",
                ">> [SOLAS_PATH_X] UNREACHABLE NODE @ D4",
            ]
        )
        side_layout.addWidget(self.violations_list)

        overlay_container = QFrame()
        overlay_container.setStyleSheet("background: #020406; border: 1px dashed #1a2533; border-radius: 6px; padding: 15px;")
        overlay_layout = QVBoxLayout(overlay_container)
        overlay_layout.addWidget(QLabel("RISK_MAP_OVERLAY"))
        
        overlay = QFrame()
        overlay.setObjectName("overlay")
        overlay.setMinimumHeight(140)
        overlay.setStyleSheet("""
            QFrame#overlay {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #432548, stop:1 #c26a42);
                border-radius: 4px;
                opacity: 0.6;
            }
        """)
        overlay_layout.addWidget(overlay)
        side_layout.addWidget(overlay_container)

        split.addWidget(side_card)
        split.setSizes([900, 400])
        root.addWidget(split)
