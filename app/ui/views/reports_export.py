from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
)


class ReportsExportView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("SYSTEM REPORTS & ARCHIVING")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Finalizing optimization artifacts and generating encrypted handoff packages.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        status_tag = QLabel("EXPORT_SERVER: ONLINE")
        status_tag.setStyleSheet("color: #00f0ff; font-family: 'Consolas'; font-size: 10px; font-weight: bold;")
        header.addWidget(status_tag, 0, Qt.AlignTop)
        root.addLayout(header)

        # Action Grid
        actions_p = QFrame()
        actions_p.setProperty("card", True)
        action_layout = QVBoxLayout(actions_p)
        action_layout.setContentsMargins(24, 24, 24, 24)
        action_layout.setSpacing(20)
        
        act_hdr = QLabel("AVAILABLE EXPORT MODULES")
        act_hdr.setProperty("heading", "h2")
        action_layout.addWidget(act_hdr)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)

        button_configs = [
            ("COMPLIANCE_DOSSIER (PDF)", True),
            ("VECTOR_CANDIDATE_SET (CSV)", False),
            ("SOLVER_TRACE_HISTORY (JSON)", False),
            ("SECURE_PROJECT_BUNDLE (ZIP)", False),
        ]
        
        for i, (label, is_accent) in enumerate(button_configs):
            btn = QPushButton(label)
            btn.setFixedHeight(50)
            if is_accent:
                btn.setProperty("accent", True)
            grid.addWidget(btn, i // 2, i % 2)

        action_layout.addLayout(grid)
        root.addWidget(actions_p)

        # Bottom section: Preview Info
        metadata_p = QFrame()
        metadata_p.setProperty("card", True)
        metadata_layout = QVBoxLayout(metadata_p)
        metadata_layout.setContentsMargins(24, 24, 24, 24)
        metadata_layout.setSpacing(16)

        hdr = QLabel("MANIFEST_PREVIEW")
        hdr.setProperty("heading", "h2")
        metadata_layout.addWidget(hdr)

        meta_list = QListWidget()
        meta_list.setStyleSheet("""
            QListWidget {
                background: #020406;
                border: 1px solid #1a2533;
                border-radius: 6px;
                color: #b0c4de;
                font-family: 'Consolas';
                font-size: 11px;
                padding: 15px;
            }
        """)
        meta_list.addItems(
            [
                ">> PROJECT_ID: UUID-2026-X812",
                ">> RUN_SEQUENCE: SEQ_442_B",
                ">> RULEPACK_SIG: 0x8F22A1_GSL_1.2",
                ">> TIMESTAMP: 2026-04-11T01:50:00Z",
                ">> SOLVER_METRIC: FIT_0.94 // GM_1.18",
                ">> INTEGRITY_HASH: SHA256_F182"
            ]
        )
        metadata_layout.addWidget(meta_list)

        root.addWidget(metadata_p)
        root.addStretch()
