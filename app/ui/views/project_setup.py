from __future__ import annotations

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ProjectSetupView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("VESSEL PROJECT REGISTRY")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Initializing naval architectural projects and synchronizing hull-specific configuration sets.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        id_tag = QLabel("SYS_REG: NSIE-2026-X812")
        id_tag.setStyleSheet("color: #6a7c8e; font-family: 'Consolas'; font-size: 10px; font-weight: bold; border-left: 2px solid #1a2533; padding-left: 15px;")
        header.addWidget(id_tag)
        root.addLayout(header)

        content = QHBoxLayout()
        content.setSpacing(24)
        root.addLayout(content)

        # Left Column: Registry Form
        form_card = QFrame()
        form_card.setProperty("card", True)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(20)

        form_title = QLabel("PROJECT METADATA")
        form_title.setProperty("heading", "h2")
        form_layout.addWidget(form_title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(16)

        def create_form_label(txt):
            l = QLabel(txt.upper())
            l.setStyleSheet("color: #4a5a6a; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
            return l

        grid.addWidget(create_form_label("Project Name"), 0, 0)
        grid.addWidget(QLineEdit("FRIGATE_INS_BRAHMAPUTRA_MOD"), 0, 1)

        grid.addWidget(create_form_label("Vessel Class"), 1, 0)
        vessel_class = QComboBox()
        vessel_class.addItems(["FRIGATE_CLASS_III", "DESTROYER_V2", "CORVETTE_LITE", "AUXILIARY_SUPPLY"])
        grid.addWidget(vessel_class, 1, 1)

        grid.addWidget(create_form_label("Draft Baseline"), 2, 0)
        grid.addWidget(QLineEdit("8.42m"), 2, 1)

        grid.addWidget(create_form_label("Deployment Sector"), 3, 0)
        sector = QComboBox()
        sector.addItems(["INDIAN_OCEAN_NORTH", "ARABIAN_SEA", "BAY_OF_BENGAL", "PACIFIC_TRANSIT"])
        grid.addWidget(sector, 3, 1)

        form_layout.addLayout(grid)
        form_layout.addStretch()

        btns = QHBoxLayout()
        btns.setSpacing(12)
        save_btn = QPushButton("SAVE_REGISTRY")
        save_btn.setProperty("accent", True)
        btns.addWidget(save_btn)
        btns.addWidget(QPushButton("DISCARD_CHANGES"))
        btns.addStretch()
        form_layout.addLayout(btns)

        content.addWidget(form_card, 2)

        # Right Column: Vessel Snapshot / Radar
        snapshot_card = QFrame()
        snapshot_card.setProperty("card", True)
        snapshot_layout = QVBoxLayout(snapshot_card)
        snapshot_layout.setContentsMargins(24, 24, 24, 24)
        snapshot_layout.setSpacing(16)

        snap_hdr = QLabel("VESSEL_SYSTEM_SNAPSHOT")
        snap_hdr.setProperty("heading", "h2")
        snapshot_layout.addWidget(snap_hdr)

        radar_frame = QFrame()
        radar_frame.setObjectName("radar")
        radar_frame.setMinimumSize(320, 240) # Changed to rectangle-like
        
        # Assets path
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "assets")
        radar_path = os.path.join(assets_dir, "radar.png").replace("\\", "/")
        
        radar_frame.setStyleSheet(f"""
            #radar {{
                background-color: #020406;
                border: 2px solid #1a2533;
                background-image: url({radar_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 8px; /* Rounded rectangle */
            }}
        """)
        snapshot_layout.addWidget(radar_frame, 0, Qt.AlignCenter)

        stats = QGridLayout()
        stats.setSpacing(10)
        for i, (l, v) in enumerate([("HULL_INT", "98%"), ("ENG_READY", "YES"), ("SYNC", "ACTIVE")]):
            label = QLabel(l)
            label.setStyleSheet("color: #4a5a6a; font-size: 9px; font-weight: 800;")
            val = QLabel(v)
            val.setStyleSheet("color: #00f0ff; font-family: 'Consolas'; font-size: 11px; font-weight: bold;")
            stats.addWidget(label, i, 0)
            stats.addWidget(val, i, 1)
        snapshot_layout.addLayout(stats)
        snapshot_layout.addStretch()

        content.addWidget(snapshot_card, 1)
