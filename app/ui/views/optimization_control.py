from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class OptimizationControlView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(24)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("OPTIMIZATION ENGINE CONTROL")
        title.setProperty("heading", "h1")
        subtitle = QLabel("Synchronizing heuristic weights and controlling evolutionary runtime cycles.")
        subtitle.setProperty("muted", True)
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        
        load_label = QLabel("THREAD_ID: OX_442 // LOAD: 14%")
        load_label.setStyleSheet("color: #6a7c8e; font-family: 'Consolas'; font-size: 10px; font-weight: bold; border-right: 2px solid #1a2533; padding-right: 15px;")
        header.addWidget(load_label)
        root.addLayout(header)

        content = QHBoxLayout()
        content.setSpacing(24)
        root.addLayout(content)

        # Left Column: Config
        config_card = QFrame()
        config_card.setProperty("card", True)
        config_layout = QVBoxLayout(config_card)
        config_layout.setContentsMargins(24, 24, 24, 24)
        config_layout.setSpacing(20)

        cfg_title = QLabel("ENGINE HYPERPARAMETERS")
        cfg_title.setProperty("heading", "h2")
        config_layout.addWidget(cfg_title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(16)

        def create_param_label(txt):
            l = QLabel(txt.upper())
            l.setStyleSheet("color: #4a5a6a; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
            return l

        self.population = QSpinBox()
        self.population.setRange(10, 5000)
        self.population.setValue(256)
        
        self.generations = QSpinBox()
        self.generations.setRange(1, 1000)
        self.generations.setValue(128)

        self.seed = QSpinBox()
        self.seed.setRange(0, 9999999)
        self.seed.setValue(4288)

        stability = QSlider(Qt.Horizontal)
        stability.setRange(0, 100)
        stability.setValue(75)

        stress = QSlider(Qt.Horizontal)
        stress.setRange(0, 100)
        stress.setValue(45)

        grid.addWidget(create_param_label("Population Pool"), 0, 0)
        grid.addWidget(self.population, 0, 1)
        grid.addWidget(create_param_label("Cycle Iterations"), 1, 0)
        grid.addWidget(self.generations, 1, 1)
        grid.addWidget(create_param_label("Entropy Seed"), 2, 0)
        grid.addWidget(self.seed, 2, 1)
        grid.addWidget(create_param_label("Stability Bias"), 3, 0)
        grid.addWidget(stability, 3, 1)
        grid.addWidget(create_param_label("Structural Bias"), 4, 0)
        grid.addWidget(stress, 4, 1)

        config_layout.addLayout(grid)

        checks = QHBoxLayout()
        for check_txt in ["STRICT_FEASIBILITY", "TRACE_EXPORT", "AUTO_DAMPEN"]:
            cb = QCheckBox(check_txt)
            cb.setStyleSheet("font-size: 9px; color: #6a7c8e; font-weight: bold;")
            checks.addWidget(cb)
        checks.addStretch()
        config_layout.addLayout(checks)

        config_layout.addStretch()

        btns = QHBoxLayout()
        btns.setSpacing(12)
        run_btn = QPushButton("INITIALIZE RUN")
        run_btn.setProperty("accent", True)
        btns.addWidget(run_btn)
        btns.addWidget(QPushButton("PAUSE"))
        btns.addWidget(QPushButton("TERMINATE"))
        btns.addStretch()
        config_layout.addLayout(btns)

        content.addWidget(config_card, 2)

        # Right Column: Live KPIs
        kpi_wrap = QVBoxLayout()
        kpi_wrap.setSpacing(16)
        
        live_hdr = QLabel("RUNTIME TELEMETRY")
        live_hdr.setStyleSheet("color: #4a5a6a; font-size: 10px; font-weight: 800; letter-spacing: 2px;")
        kpi_wrap.addWidget(live_hdr)

        for label, value, color in [
            ("CYCLE_PROGRESS", "ITER_72 / 128", "#00f0ff"),
            ("FEASIBILITY_YIELD", "68.2%", "#00f0ff"),
            ("PEAK_FITNESS", "0.942", "#00f0ff"),
            ("REJECTION_ALRT", "ST_02_GM_LOW", "#ff3b30"),
        ]:
            card = QFrame()
            card.setProperty("card", True)
            card.setStyleSheet("background: #020406; border-radius: 8px;")
            lay = QVBoxLayout(card)
            lay.setContentsMargins(16, 16, 16, 16)
            lay.setSpacing(4)
            name = QLabel(label)
            name.setStyleSheet("color: #4a5a6a; font-size: 9px; font-weight: bold; letter-spacing: 1px;")
            metric = QLabel(value)
            metric.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: 800; font-family: 'Consolas';")
            lay.addWidget(name)
            lay.addWidget(metric)
            kpi_wrap.addWidget(card)

        kpi_wrap.addStretch()
        content.addLayout(kpi_wrap, 1)
