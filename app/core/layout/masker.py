from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MaskGrid:
    width: int
    height: int
    legal_cells: set[tuple[int, int]]

    def is_legal(self, cell: tuple[int, int]) -> bool:
        return cell in self.legal_cells


class ConstraintMasker:
    def legal_positions(
        self, component_type: str, layout_state: dict, context: dict
    ) -> MaskGrid:
        width = int(context.get("grid_width", 20))
        height = int(context.get("grid_height", 10))
        forbidden = set(context.get("forbidden_cells", []))
        legal = {(x, y) for x in range(width) for y in range(height) if (x, y) not in forbidden}
        return MaskGrid(width=width, height=height, legal_cells=legal)

