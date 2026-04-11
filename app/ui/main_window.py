from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.views.compliance_dashboard import ComplianceDashboardView
from app.ui.views.layout_workspace import LayoutWorkspaceView
from app.ui.views.optimization_control import OptimizationControlView
from app.ui.views.project_setup import ProjectSetupView
from app.ui.views.reports_export import ReportsExportView
from app.ui.views.rulepack_constraints import RulepackConstraintsView


APP_STYLESHEET = """
QMainWindow, QWidget {
    background: #0f1720;
    color: #d7e3ef;
    font-family: "Segoe UI";
    font-size: 13px;
}
QLabel[heading="h1"] {
    font-size: 22px;
    font-weight: 700;
    color: #eff6ff;
}
QLabel[heading="h2"] {
    font-size: 16px;
    font-weight: 600;
    color: #f0f7ff;
}
QLabel[muted="true"] {
    color: #95a7ba;
}
QFrame[card="true"] {
    background: #162231;
    border: 1px solid #23364a;
    border-radius: 12px;
}
QFrame#canvas {
    border: 1px dashed #4a6a87;
    border-radius: 12px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a2e42, stop:1 #243f59);
}
QFrame#viewport3d {
    border: 1px solid #49637f;
    border-radius: 12px;
    background: qradialgradient(cx:0.25, cy:0.2, radius:1.1,
        stop:0 #2a4b64, stop:0.45 #1f364a, stop:1 #0f1c2b);
}
QFrame#viewport_hud {
    background: rgba(10, 23, 36, 0.8);
    border: 1px solid #3f5b77;
    border-radius: 8px;
}
QFrame#overlay {
    border: 1px dashed #4a6a87;
    border-radius: 10px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #432548, stop:0.5 #8d2e4b, stop:1 #c26a42);
}
QPushButton {
    background: #203247;
    border: 1px solid #2f4761;
    border-radius: 8px;
    padding: 7px 12px;
    color: #e4edf6;
}
QPushButton:hover {
    background: #29425c;
}
QPushButton[accent="true"] {
    background: #24a1a8;
    border: 1px solid #2ab5bd;
    color: #052831;
    font-weight: 700;
}
QPushButton[accent="true"]:hover {
    background: #35b6bd;
}
QLineEdit, QComboBox, QSpinBox, QPlainTextEdit {
    background: #0f1b2a;
    border: 1px solid #2e4257;
    border-radius: 8px;
    padding: 6px 8px;
    color: #dbe8f4;
}
QTabWidget::pane {
    border: 1px solid #2b3f53;
    background: #101a25;
    border-radius: 10px;
    margin-top: 8px;
}
QTabBar::tab {
    background: #1a2838;
    border: 1px solid #2a3d52;
    padding: 8px 12px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background: #24405a;
}
QTableWidget, QListWidget {
    background: #0f1b2a;
    border: 1px solid #2d4156;
    border-radius: 8px;
    gridline-color: #284055;
}
QHeaderView::section {
    background: #21364c;
    color: #e7f1fa;
    border: none;
    padding: 6px;
}
QStatusBar {
    background: #111d2b;
    color: #a8bfd4;
}
QGroupBox {
    border: 1px solid #2e4257;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NSIE - Naval Spatial Intelligence Engine")
        self.resize(1400, 860)
        self.setStyleSheet(APP_STYLESHEET)

        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 14, 16, 10)
        root.setSpacing(12)

        header = QFrame()
        header.setProperty("card", True)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 12, 14, 12)

        title_wrap = QVBoxLayout()
        app_name = QLabel("NSIE Control Console")
        app_name.setProperty("heading", "h1")
        app_sub = QLabel("Visual frontend prototype for project setup, optimization, and compliance review.")
        app_sub.setProperty("muted", True)
        title_wrap.addWidget(app_name)
        title_wrap.addWidget(app_sub)
        header_layout.addLayout(title_wrap)
        header_layout.addStretch()

        self.high_contrast_toggle = QCheckBox("High Contrast")
        self.high_contrast_toggle.setChecked(False)
        self.high_contrast_toggle.stateChanged.connect(self._toggle_theme)
        header_layout.addWidget(self.high_contrast_toggle)

        root.addWidget(header)

        toolbar = QHBoxLayout()
        self.btn_new = QPushButton("New Project")
        self.btn_new.setProperty("accent", True)
        self.btn_load = QPushButton("Load")
        self.btn_save = QPushButton("Save Draft")
        self.btn_refresh = QPushButton("Refresh Visuals")
        toolbar.addWidget(self.btn_new)
        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_save)
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        self.notification = QLabel("Ready: frontend shell mode (no backend execution)")
        self.notification.setProperty("muted", True)
        toolbar.addWidget(self.notification)
        root.addLayout(toolbar)

        self.tabs = QTabWidget()
        self.tabs.addTab(ProjectSetupView(), "1. Project Setup")
        self.tabs.addTab(RulepackConstraintsView(), "2. Rulepack & Constraints")
        self.tabs.addTab(LayoutWorkspaceView(), "3. Layout Workspace")
        self.tabs.addTab(OptimizationControlView(), "4. Optimization Control")
        self.tabs.addTab(ComplianceDashboardView(), "5. Compliance Dashboard")
        self.tabs.addTab(ReportsExportView(), "6. Reports & Export")
        root.addWidget(self.tabs)

        self.setCentralWidget(central)

        status = QStatusBar(self)
        status.showMessage("Active Project: NSIE-2026-018 | Rulepack: starter-gsl-pack v1.2 | Run State: idle")
        self.setStatusBar(status)

        self.btn_new.clicked.connect(lambda: self._set_notice("UI action: New Project clicked"))
        self.btn_load.clicked.connect(lambda: self._set_notice("UI action: Load clicked"))
        self.btn_save.clicked.connect(lambda: self._set_notice("UI action: Save Draft clicked"))
        self.btn_refresh.clicked.connect(lambda: self._set_notice("UI action: Refresh Visuals clicked"))

    def _set_notice(self, message: str) -> None:
        self.notification.setText(message)

    def _toggle_theme(self, state: int) -> None:
        if state == Qt.Checked:
            self.setStyleSheet(APP_STYLESHEET + "QMainWindow, QWidget { color: #ffffff; }")
            self._set_notice("Theme: high contrast enabled")
        else:
            self.setStyleSheet(APP_STYLESHEET)
            self._set_notice("Theme: default engineering palette enabled")
