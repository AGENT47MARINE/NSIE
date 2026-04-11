from __future__ import annotations

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Viewport3DView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("3D NEURAL VIEWPORT")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Real-time volumetric render of frigate-class geometry with neural-pathing overlays.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        status_tag = QLabel("STREAM: 8K_NOMINAL")
        status_tag.setStyleSheet("color: #00f0ff; font-family: 'Consolas'; font-size: 10px; font-weight: bold; background: rgba(0, 240, 255, 0.1); padding: 4px 8px; border: 1px solid #00f0ff;")
        header.addWidget(status_tag, 0, Qt.AlignTop)
        root.addLayout(header)

        # Assets Path
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "assets")
        v3d_bg_path = os.path.join(assets_dir, "frigate_3d.png").replace("\\", "/")

        v3d_card = QFrame()
        v3d_card.setProperty("card", True)
        v3d_card.setStyleSheet("border: 1px solid #1152d4;")
        v3d_layout = QVBoxLayout(v3d_card)
        v3d_layout.setContentsMargins(10, 10, 10, 10)

        v3d = QFrame()
        v3d.setObjectName("viewport3d")
        v3d.setStyleSheet(f"""
            #viewport3d {{
                background-color: #020406;
                border: 1px solid #1a2533;
                background-image: url({v3d_bg_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 8px;
            }}
        """)
        
        # Expanded HUD
        v3d_inner = QVBoxLayout(v3d)
        hud = QFrame()
        hud.setObjectName("viewport_hud")
        hud.setFixedWidth(280)
        hud_lay = QGridLayout(hud)
        hud_lay.setContentsMargins(15, 12, 15, 12)
        
        def add_hud_row(r, label, val, color="#00f0ff"):
            l = QLabel(label); l.setStyleSheet("color: #4a5a6a; font-size: 9px; font-weight: bold;")
            v = QLabel(val); v.setStyleSheet(f"color: {color}; font-family: 'Consolas'; font-size: 10px;")
            hud_lay.addWidget(l, r, 0)
            hud_lay.addWidget(v, r, 1, Qt.AlignRight)

        add_hud_row(0, "CAM_COORD", "[142, -22, 18]")
        add_hud_row(1, "FOY_ANGLE", "45.0 DEG")
        add_hud_row(2, "RENDER_FPS", "142")
        add_hud_row(3, "VERTEX_CNT", "4.2M")
        
        v3d_inner.addWidget(hud, 0, Qt.AlignTop | Qt.AlignLeft)
        v3d_inner.addStretch()
        
        info_strip = QLabel(">> NEURAL_RENDER_STREAM: STABLE // ARCHITECTURE: FRIGATE_X_MOD_2")
        info_strip.setStyleSheet("color: #00f0ff88; font-family: 'Consolas'; font-size: 10px; padding: 10px;")
        v3d_inner.addWidget(info_strip, 0, Qt.AlignCenter)

        v3d_layout.addWidget(v3d)
        root.addWidget(v3d_card)

        # Navigation Tools
        tools = QHBoxLayout()
        tools.addWidget(QPushButton("ORBIT_CAM"))
        tools.addWidget(QPushButton("SNAPSHOT"))
        tools.addWidget(QPushButton("TOGGLE_WIREFRAME"))
        tools.addStretch()
        tools.addWidget(QPushButton("RE-CENTER VIEW"), 0, Qt.AlignRight)
        
        view_mode = QComboBox()
        view_mode.addItems(["ISOMETRIC", "TOP_ORTHO", "PORT_BOARD", "ENGINE_SECTION"])
        view_mode.setFixedWidth(160)
        tools.addWidget(view_mode)
        root.addLayout(tools)
