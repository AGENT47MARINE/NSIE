from __future__ import annotations

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Workspace2DView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("2D DESIGN SCHEMATIC")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Technical deck-plan drafting and compartment boundary definition.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        mode_label = QLabel("MODE: VECTOR_DRAFT")
        mode_label.setStyleSheet("color: #00f0ff; font-family: 'Consolas'; font-size: 10px; font-weight: bold; background: rgba(0, 240, 255, 0.1); padding: 4px 8px; border: 1px solid #00f0ff;")
        header.addWidget(mode_label, 0, Qt.AlignTop)
        root.addLayout(header)

        # Asset path
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "assets")
        canvas_bg_path = os.path.join(assets_dir, "deck_2d.png").replace("\\", "/")

        canvas_card = QFrame()
        canvas_card.setProperty("card", True)
        canvas_layout = QVBoxLayout(canvas_card)
        canvas_layout.setContentsMargins(20, 20, 20, 20)
        
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("LAYER: DECK_MAIN_01"))
        toolbar.addStretch()
        for t in ["COMPARTMENTS", "TANK_VALVES", "EGRESS_NODES"]:
            cb = QCheckBox(t)
            cb.setStyleSheet("font-size: 9px; color: #6a7c8e;")
            toolbar.addWidget(cb)
        canvas_layout.addLayout(toolbar)

        canvas = QFrame()
        canvas.setObjectName("canvas")
        canvas.setStyleSheet(f"""
            #canvas {{
                background-color: #020406;
                border: 1px solid #1a2533;
                background-image: url({canvas_bg_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 8px;
            }}
        """)
        
        cl = QVBoxLayout(canvas)
        cl.addStretch()
        cl.addWidget(QLabel(">> SCALING: 1:100\n>> SYNC: LOCAL_CACHE_OK"), 0, Qt.AlignRight | Qt.AlignBottom)
        
        canvas_layout.addWidget(canvas)
        root.addWidget(canvas_card)

        # Bottom Tools
        tools = QHBoxLayout()
        tools.addWidget(QPushButton("EXPORT_DXF"))
        tools.addWidget(QPushButton("MANUAL_CORRECT"))
        tools.addStretch()
        tools.addWidget(QPushButton("SYNC_TO_3D"), 0, Qt.AlignRight)
        root.addLayout(tools)
