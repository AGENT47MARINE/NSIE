from __future__ import annotations

from statistics import mean
from typing import Any

from app.models import NavalMetrics


class NavalCalcService:
    def quick_metrics(self, layout: dict[str, Any], weights: dict[str, Any] | None = None) -> NavalMetrics:
        placements = layout.get("placements", [])
        xs = [float(p.position_xyz[0]) for p in placements] or [0.0]
        ys = [float(p.position_xyz[1]) for p in placements] or [0.0]
        zs = [float(p.position_xyz[2]) for p in placements] or [0.0]
        gm = float(1.0 + (len(placements) / 100.0))
        return NavalMetrics(
            cog_xyz=(mean(xs), mean(ys), mean(zs)),
            gm=gm,
            draft=float(3.5 + len(placements) * 0.01),
            trim=0.1,
            stress_index=min(1.0, len(placements) / 1000.0),
        )

    def final_check(self, layout: dict[str, Any], weights: dict[str, Any] | None = None) -> NavalMetrics:
        return self.quick_metrics(layout, weights)

