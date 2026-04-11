from __future__ import annotations

import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class LayoutWorkspaceView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        # Header section
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("SPATIAL INTELLIGENCE DESIGN LAB")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Dedicated 2D/3D synchronization environment for hull compartmentalization.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        mode_label = QLabel("STATUS: SYNC_ENGAGED")
        mode_label.setStyleSheet("color: #00f0ff; font-family: 'Consolas'; font-size: 10px; font-weight: bold; background: rgba(0, 240, 255, 0.1); padding: 6px 12px; border: 1px solid #00f0ff; border-radius: 4px;")
        header.addWidget(mode_label, 0, Qt.AlignVCenter)

        header.addSpacing(10)
        self.btn_swap_view = QPushButton("SWAP TO 3D VIEW")
        self.btn_swap_view.setProperty("accent", True)
        self.btn_swap_view.setFixedWidth(140)
        self.btn_swap_view.clicked.connect(self._toggle_view)
        header.addWidget(self.btn_swap_view)

        root.addLayout(header)

        # Assets Path Calculation
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "assets")
        v3d_bg_path = os.path.join(assets_dir, "frigate_3d.png").replace("\\", "/")
        canvas_bg_path = os.path.join(assets_dir, "deck_2d.png").replace("\\", "/")

        # MAIN AREA: Horizontal Splitter (Viewports vs Right Analysis)
        self.main_h_splitter = QSplitter(Qt.Horizontal)
        self.main_h_splitter.setHandleWidth(1)
        self.main_h_splitter.setStyleSheet("QSplitter::handle { background: #1a2533; }")

        # LEFT PART: Stacked Viewports
        self.stacked_viewports = QStackedWidget()
        
        # A. 2D Workspace Panel
        pane_2d = QFrame()
        pane_2d.setProperty("card", True)
        lay_2d = QVBoxLayout(pane_2d)
        lay_2d.setContentsMargins(15, 15, 15, 15)
        
        hdr_2d = QHBoxLayout()
        lbl_2d = QLabel("2D_SCHEMATIC_CANVAS")
        lbl_2d.setStyleSheet("color: #4a5a6a; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
        hdr_2d.addWidget(lbl_2d)
        hdr_2d.addStretch()
        view_toggle = QPushButton("DRAFT_V2")
        view_toggle.setFixedWidth(80)
        hdr_2d.addWidget(view_toggle)
        lay_2d.addLayout(hdr_2d)

        canvas = QFrame()
        canvas.setObjectName("canvas")
        canvas.setStyleSheet(f"""
            #canvas {{
                background-color: #020406;
                border: 1px solid #1a2533;
                background-image: url({canvas_bg_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 4px;
            }}
        """)
        lay_2d.addWidget(canvas)
        
        # Tools row for 2D
        tools_2d = QHBoxLayout()
        for t in ["PAN", "ZOOM", "MSR", "CUT"]:
            tb = QPushButton(t)
            tb.setFixedWidth(45)
            tb.setStyleSheet("font-size: 8px; font-weight: bold;")
            tools_2d.addWidget(tb)
        tools_2d.addStretch()
        lay_2d.addLayout(tools_2d)

        self.stacked_viewports.addWidget(pane_2d)

        # B. 3D Viewport Panel
        pane_3d = QFrame()
        pane_3d.setProperty("card", True)
        pane_3d.setStyleSheet("border: 1px solid #1152d4;") # Highlight the 3D pane
        lay_3d = QVBoxLayout(pane_3d)
        lay_3d.setContentsMargins(15, 15, 15, 15)

        hdr_3d = QHBoxLayout()
        lbl_3d = QLabel("3D_NEURAL_VIEWPORT")
        lbl_3d.setStyleSheet("color: #4a5a6a; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
        hdr_3d.addWidget(lbl_3d)
        hdr_3d.addStretch()
        v_mode = QComboBox()
        v_mode.addItems(["ISOMETRIC", "WIRE_FRAME", "HEAT_MAP", "GHOSTED"])
        v_mode.setFixedWidth(100)
        hdr_3d.addWidget(v_mode)
        lay_3d.addLayout(hdr_3d)

        v3d = QFrame()
        v3d.setObjectName("viewport3d")
        v3d.setStyleSheet(f"""
            #viewport3d {{
                background-color: #020406;
                border: 1px solid #1a2533;
                background-image: url({v3d_bg_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 4px;
            }}
        """)
        
        # HUD Overlay for 3D
        v3d_inner = QVBoxLayout(v3d)
        hud = QFrame()
        hud.setStyleSheet("background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 4px;")
        hud.setFixedWidth(140)
        hud_lay = QVBoxLayout(hud)
        def h_lbl(t,v):
            r = QHBoxLayout()
            rl = QLabel(t); rl.setStyleSheet("color: #4a5a6a; font-size: 8px;")
            rv = QLabel(v); rv.setStyleSheet("color: #00f0ff; font-family: 'Consolas'; font-size: 8px;")
            r.addWidget(rl); r.addStretch(); r.addWidget(rv)
            return r
        hud_lay.addLayout(h_lbl("CAM_X", "44.2"))
        hud_lay.addLayout(h_lbl("CAM_Y", "-12.8"))
        hud_lay.addLayout(h_lbl("ZOOM", "1.4x"))
        v3d_inner.addWidget(hud, 0, Qt.AlignTop | Qt.AlignLeft)
        v3d_inner.addStretch()
        
        lay_3d.addWidget(v3d)
        
        # Tools row for 3D
        tools_3d = QHBoxLayout()
        tools_3d.addWidget(QPushButton("ORBIT"))
        tools_3d.addWidget(QPushButton("SNAPSHOT"))
        tools_3d.addStretch()
        lay_3d.addLayout(tools_3d)

        self.stacked_viewports.addWidget(pane_3d)
        self.main_h_splitter.addWidget(self.stacked_viewports)

        # RIGHT PART: Analysis Matrix & System Report
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(16)

        # 1. Candidate Table
        table_card = QFrame()
        table_card.setProperty("card", True)
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_tbl = QLabel("VECTOR CANDIDATE ANALYSIS MATRIX")
        lbl_tbl.setStyleSheet("color: #4a5a6a; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
        table_layout.addWidget(lbl_tbl)

        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["VECTOR_ID", "FEASIBLE", "FITNESS", "METACENTRIC", "STRESS"])
        self.table.horizontalHeader().setStretchLastSection(True)
        # We fill simple sample data
        sample = [
            ("V-201", "READY", "0.91", "1.21m", "0.29"),
            ("V-198", "READY", "0.90", "1.18m", "0.33"),
            ("V-194", "FAIL", "0.85", "0.74m", "0.58"),
            ("V-188", "READY", "0.84", "1.02m", "0.41"),
            ("V-181", "FAIL", "0.80", "0.68m", "0.62"),
        ]
        mono_font = QFont("Consolas")
        for r, cols in enumerate(sample):
            for c, val in enumerate(cols):
                item = QTableWidgetItem(val)
                item.setFont(mono_font)
                if c == 1:
                    item.setForeground(Qt.green if val == "READY" else Qt.red)
                self.table.setItem(r, c, item)
        table_layout.addWidget(self.table)
        right_layout.addWidget(table_card, 3)

        # 2. System Sync Report (Side)
        sync_card = QFrame()
        sync_card.setProperty("card", True)
        sync_layout = QVBoxLayout(sync_card)
        sync_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_sync = QLabel("SYNC_REPORT")
        lbl_sync.setStyleSheet("color: #4a5a6a; font-weight: 800; font-size: 10px; letter-spacing: 1.5px;")
        sync_layout.addWidget(lbl_sync)

        sync_box = QFrame()
        sync_box.setStyleSheet("background: #020406; border-radius: 4px; padding: 10px;")
        sb_lay = QVBoxLayout(sync_box)
        for t, v in [("HULL_A", "LOCKED"), ("ZONE_B", "VALID"), ("ROUTES", "OK")]:
            rl = QHBoxLayout()
            rl.addWidget(QLabel(t)); rl.addStretch()
            rv = QLabel(v); rv.setStyleSheet("color: #b0c4de; font-family: 'Consolas'; font-size: 10px;")
            rl.addWidget(rv)
            sb_lay.addLayout(rl)
        sync_layout.addWidget(sync_box)
        sync_layout.addStretch()
        sync_layout.addWidget(QPushButton("LOCK_DESIGN"))
        right_layout.addWidget(sync_card, 1)

        self.main_h_splitter.addWidget(right_panel)
        self.main_h_splitter.setSizes([900, 400])
        
        root.addWidget(self.main_h_splitter)

    def _toggle_view(self) -> None:
        idx = self.stacked_viewports.currentIndex()
        new_idx = 1 if idx == 0 else 0
        self.stacked_viewports.setCurrentIndex(new_idx)
        
        if new_idx == 0:
            self.btn_swap_view.setText("SWAP TO 3D VIEW")
        else:
            self.btn_swap_view.setText("SWAP TO 2D VIEW")
