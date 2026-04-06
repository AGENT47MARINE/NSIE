from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.application_service import ApplicationService
from app.ui.controllers import ComplianceController, OptimizationController, ProjectController, ReportController
from app.ui.views.compliance_dashboard import ComplianceDashboardView
from app.ui.views.layout_workspace import LayoutWorkspaceView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NSIE - Naval Spatial Intelligence Engine")
        self.resize(1200, 760)

        self.service = ApplicationService()
        self.project_controller = ProjectController(self.service)
        self.optimization_controller = OptimizationController(self.service, self.project_controller)
        self.compliance_controller = ComplianceController(self.service, self.optimization_controller)
        self.report_controller = ReportController(self.service, self.optimization_controller)

        central = QWidget(self)
        root_layout = QVBoxLayout(central)

        toolbar_row = QHBoxLayout()
        self.btn_init = QPushButton("Initialize Project")
        self.btn_run = QPushButton("Run Optimization")
        self.btn_refresh = QPushButton("Refresh Views")
        toolbar_row.addWidget(self.btn_init)
        toolbar_row.addWidget(self.btn_run)
        toolbar_row.addWidget(self.btn_refresh)
        toolbar_row.addStretch()
        root_layout.addLayout(toolbar_row)

        self.status_label = QLabel("Status: waiting for initialization")
        root_layout.addWidget(self.status_label)

        self.tabs = QTabWidget()
        self.layout_view = LayoutWorkspaceView()
        self.compliance_view = ComplianceDashboardView()
        self.report_view = QTextEdit()
        self.report_view.setReadOnly(True)
        self.tabs.addTab(self.layout_view, "Layout Workspace")
        self.tabs.addTab(self.compliance_view, "Compliance Dashboard")
        self.tabs.addTab(self.report_view, "Run Report")
        root_layout.addWidget(self.tabs)

        self.setCentralWidget(central)
        self._wire_events()

    def _wire_events(self) -> None:
        self.btn_init.clicked.connect(self.initialize_project)
        self.btn_run.clicked.connect(self.run_optimization)
        self.btn_refresh.clicked.connect(self.refresh_views)

    def initialize_project(self) -> None:
        project_id = self.project_controller.create_default_project()
        self.project_controller.load_default_rules(project_id)
        self.status_label.setText(f"Status: initialized {project_id} with starter rule pack")

    def run_optimization(self) -> None:
        if not self.project_controller.project_id:
            QMessageBox.warning(self, "NSIE", "Initialize project first.")
            return
        run_id = self.optimization_controller.start_default_run()
        self.status_label.setText(f"Status: optimization complete for run {run_id}")
        self.refresh_views()

    def refresh_views(self) -> None:
        status = self.optimization_controller.status()
        rows = self.optimization_controller.top_layouts(10)
        self.layout_view.set_layout_rows(rows)
        violations = self.compliance_controller.latest_violations()
        self.compliance_view.show_violations(violations)
        self.report_view.setPlainText(self.report_controller.build_summary())
        if status:
            self.status_label.setText(
                f"Status: gen={status.get('generation', 0)} "
                f"feasible={status.get('feasible_rate', 0.0):.2%} "
                f"best={status.get('best_score', 0.0):.3f}"
            )

