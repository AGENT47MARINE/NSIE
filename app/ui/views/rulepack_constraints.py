from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class RulepackConstraintsView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        title_container = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("RULESET & REGULATORY CONSTRAINTS")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Inspecting heuristic boundaries and regulatory thresholds for spatial logic engines.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        title_container.addLayout(title_box)
        title_container.addStretch()
        
        btn_audit = QPushButton("EXPORT AUDIT LOG")
        title_container.addWidget(btn_audit, 0, Qt.AlignBottom)
        root.addLayout(title_container)

        body = QHBoxLayout()
        body.setSpacing(24)
        root.addLayout(body)

        # Left Column: Selector
        left = QFrame()
        left.setProperty("card", True)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(16)
        
        sel_label = QLabel("ACTIVE ARCHIVE")
        sel_label.setStyleSheet("color: #4a5a6a; font-size: 10px; font-weight: 800; letter-spacing: 1.5px;")
        left_layout.addWidget(sel_label)

        selector = QComboBox()
        selector.addItems(["STARTER_GSL_PACK_V12", "CLASS_EXTENDED_PRO_V09", "OFFSHORE_SAFETY_V20"])
        left_layout.addWidget(selector)

        info_box = QFrame()
        info_box.setStyleSheet("background: #020406; border-radius: 6px; padding: 12px;")
        info_layout = QVBoxLayout(info_box)
        for label_t, value_t in [
            ("VERSION", "SC_1.2.0"),
            ("AUTHOR", "COMPLIANCE_A7"),
            ("DOMAINS", "SOLAS / MARPOL"),
            ("RULES", "48_HARD_ACTIVE"),
        ]:
            row = QHBoxLayout()
            l = QLabel(label_t)
            l.setStyleSheet("color: #4a5a6a; font-size: 9px; font-weight: 800;")
            v = QLabel(value_t)
            v.setStyleSheet("color: #b0c4de; font-size: 10px; font-family: 'Consolas';")
            v.setAlignment(Qt.AlignRight)
            row.addWidget(l)
            row.addWidget(v)
            info_layout.addLayout(row)
        left_layout.addWidget(info_box)

        left_layout.addSpacing(10)
        btn_load = QPushButton("PULL ARCHIVE")
        btn_load.setProperty("accent", True)
        left_layout.addWidget(btn_load)
        left_layout.addWidget(QPushButton("VALIDATE INTEGRITY"))
        left_layout.addWidget(QPushButton("ENGINE_OVERRIDE"))
        left_layout.addStretch()

        body.addWidget(left, 1)

        # Center Column: Table
        center = QFrame()
        center.setProperty("card", True)
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(16)

        table_hdr = QLabel("BOUNDARY PARAMETER MATRIX")
        table_hdr.setProperty("heading", "h2")
        center_layout.addWidget(table_hdr)

        self.table = QTableWidget(8, 4)
        self.table.setHorizontalHeaderLabels(["VECTOR_ID", "DOMAIN", "SEVERITY", "RUNTIME_STATUS"])
        self.table.horizontalHeader().setStretchLastSection(True)

        rows = [
            ("SOLAS_EGRESS_HB_001", "SOLAS", "CRITICAL", "STABLE"),
            ("MARPOL_TANK_DS_001", "MARPOL", "HIGH", "STABLE"),
            ("CLASS_GM_ST_001", "CLASS", "CRITICAL", "STABLE"),
            ("MLC_CABIN_PX_004", "MLC", "ADVISORY", "STABLE"),
            ("CARGO_CLEAR_AX_011", "NAVY_OPS", "HIGH", "BYPASS"),
            ("FIRE_ZONE_P7_006", "SOLAS", "CRITICAL", "STABLE"),
            ("STRUCT_LOAD_X_092", "CLASS", "HIGH", "STABLE"),
            ("SENS_CALIB_L_002", "CORE", "ADVISORY", "STABLE"),
        ]
        mono_font = QFont("Consolas")
        for r, cols in enumerate(rows):
            for c, val in enumerate(cols):
                item = QTableWidgetItem(val)
                item.setFont(mono_font)
                if c == 2:
                    if val == "CRITICAL": item.setForeground(Qt.red)
                    elif val == "HIGH": item.setForeground(Qt.yellow)
                self.table.setItem(r, c, item)

        center_layout.addWidget(self.table)
        body.addWidget(center, 3)

        # Right Column: Details
        right = QFrame()
        right.setProperty("card", True)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)
        
        hdr = QLabel("PARAMETER_INSIGHT")
        hdr.setProperty("heading", "h2")
        right_layout.addWidget(hdr)

        details_code = QPlainTextEdit()
        details_code.setReadOnly(True)
        details_code.setStyleSheet("""
            QPlainTextEdit {
                background: #020406;
                color: #00f0ff;
                font-family: 'Consolas';
                border: 1px solid #1a2533;
                border-radius: 4px;
            }
        """)
        details_code.setPlainText(
            "// VECTOR: SOLAS_EGRESS_HB_001\n"
            "// DESCRIPTION: Evacuation corridor logic\n"
            "\n"
            "DEFINE CONSTRAINT c0:\n"
            "  PARAM min_width = 1.25m\n"
            "  PARAM path_type = PRIMARY\n"
            "  ASSERT corridor.width >= min_width\n"
            "  FAIL_MODE: ABORT_GEN\n"
            "\n"
            "// RUNTIME: PASSED\n"
            "// LAST_CHECK: 0.12s AGO"
        )
        right_layout.addWidget(details_code)
        
        guide_box = QFrame()
        guide_box.setStyleSheet("background: #111e2b; border-radius: 6px; padding: 12px;")
        guide_layout = QVBoxLayout(guide_box)
        guide_layout.addWidget(QLabel("PRIMARY CONSTRAINTS: 32\nADVISORY NOTES: 16\nTOTAL REJECTION RATIO: 12.4%"))
        right_layout.addWidget(guide_box)
        
        body.addWidget(right, 2)

