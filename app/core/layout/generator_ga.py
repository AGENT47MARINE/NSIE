from __future__ import annotations

import random
import uuid
from dataclasses import asdict
from typing import Any

from app.core.layout.masker import ConstraintMasker
from app.models import LayoutCandidate, LayoutPlacement


class LayoutGenerator:
    def __init__(self, masker: ConstraintMasker | None = None, seed: int = 42) -> None:
        self.masker = masker or ConstraintMasker()
        self._rng = random.Random(seed)

    def seed_population(self, project_spec: dict[str, Any], size: int = 10) -> list[LayoutCandidate]:
        population: list[LayoutCandidate] = []
        components = project_spec.get("components", [])
        context = project_spec.get("context", {})
        for _ in range(size):
            placements: list[LayoutPlacement] = []
            for comp in components:
                mask = self.masker.legal_positions(comp["type"], {"placements": placements}, context)
                if not mask.legal_cells:
                    continue
                x, y = self._rng.choice(tuple(mask.legal_cells))
                placements.append(
                    LayoutPlacement(
                        component_id=comp["id"],
                        component_type=comp["type"],
                        position_xyz=(float(x), float(y), 0.0),
                        orientation="0,0,0",
                    )
                )
            population.append(
                LayoutCandidate(
                    id=str(uuid.uuid4()),
                    genome={"seeded": True},
                    placements=placements,
                    feasible=False,
                    fitness=0.0,
                )
            )
        return population

    def evolve(
        self, population: list[LayoutCandidate], feedback: dict[str, Any] | None = None
    ) -> list[LayoutCandidate]:
        feedback = feedback or {}
        mutation_rate = float(feedback.get("mutation_rate", 0.1))
        new_population: list[LayoutCandidate] = []
        for candidate in population:
            mutated = LayoutCandidate(
                id=str(uuid.uuid4()),
                genome=dict(candidate.genome, parent_id=candidate.id),
                placements=[LayoutPlacement(**asdict(p)) for p in candidate.placements],
                feasible=False,
                fitness=0.0,
            )
            if mutated.placements and self._rng.random() < mutation_rate:
                idx = self._rng.randrange(len(mutated.placements))
                p = mutated.placements[idx]
                mutated.placements[idx] = LayoutPlacement(
                    component_id=p.component_id,
                    component_type=p.component_type,
                    position_xyz=(p.position_xyz[0] + 1.0, p.position_xyz[1], p.position_xyz[2]),
                    orientation=p.orientation,
                )
            new_population.append(mutated)
        return new_population

