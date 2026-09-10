from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .definition import CodeDefinition, Coord, Pauli

# Distance-preserving 4-step CNOT schedule.
# Maps a leg's relative offset (dx, dy) -> time step.
STEP_OF_OFFSET_ROW = {(-1, -1): 0, (+1, -1): 1, (-1, +1): 2, (+1, +1): 3}  # Row-major
STEP_OF_OFFSET_COL = {(-1, -1): 0, (-1, +1): 1, (+1, -1): 2, (+1, +1): 3}  # Column-major


@dataclass(frozen=True)
class Lattice:
    # Data qubit placement for a surface code of the given distance.
    distance: int
    data_qubits: dict[Coord, int]


def rotated_lattice(distance: int) -> Lattice:
    # Place the d*d data qubits of a rotated lattice.
    # Data qubits sit at (2c+1, 2r+1) for r, c in 0..d-1
    data: dict[Coord, int] = {}
    for r in range(distance):
        for c in range(distance):
            data[(2 * c + 1, 2 * r + 1)] = len(data)
    return Lattice(distance=distance, data_qubits=data)


def checkerboard_parity(q: Coord) -> int:
    # Checkerboard colour of a data qubit at (2c+1, 2r+1).
    x, y = q
    return (((x - 1) // 2) + ((y - 1) // 2)) % 2


def checkerboard_stabilizers(
    lattice: Lattice, *, name: Optional[str] = None
) -> CodeDefinition:
    # Build the CSS rotated surface code on a rotated lattice.
    distance = lattice.distance
    data = lattice.data_qubits

    ancillas: dict[Coord, int] = {}
    stabilizers: dict[Coord, dict[Coord, Pauli]] = {}

    next_ancilla = len(data)
    for r in range(0, distance + 1):
        for c in range(0, distance + 1):
            x, y = 2 * c, 2 * r
            # data neighbours = the 4 diagonal data sites
            neighbours = [
                (x - 1, y - 1), (x + 1, y - 1),
                (x - 1, y + 1), (x + 1, y + 1),
            ]
            present = [q for q in neighbours if q in data]
            if len(present) <= 1:
                continue
            # Checkerboard type by (r+c) parity
            stabilizer_type: Pauli = "Z" if (r + c) % 2 == 0 else "X"
            # Boundary handling: keep weight-2 checks only on the right boundaries.
            if len(present) == 2:
                on_vertical_boundary = (c == 0 or c == distance) # left/right edge
                on_horizontal_boundary = (r == 0 or r == distance) # top/bottom edge
                if on_horizontal_boundary and stabilizer_type != "Z":
                    continue
                if on_vertical_boundary and stabilizer_type != "X":
                    continue
                # reject corners with only the wrong-type 2-body check
                if on_horizontal_boundary and on_vertical_boundary:
                    continue

            ancillas[(x, y)] = next_ancilla
            next_ancilla += 1
            stabilizers[(x, y)] = {q: stabilizer_type for q in present}

    return CodeDefinition(
        name=f"rotated_surface_d{distance}" if name is None else name,
        distance=distance,
        data_qubits=dict(data),
        ancilla_qubits=ancillas,
        stabilizers=stabilizers,
        logical_x={(2 * c + 1, 1): "X" for c in range(distance)},
        logical_z={(1, 2 * r + 1): "Z" for r in range(distance)},
    )


def default_rotated_schedule(
    code: CodeDefinition,
) -> dict[Coord, list[Optional[Coord]]]:
    # Assign each stabilizer's legs to one of 4 parallel time steps.
    schedule: dict[Coord, list[Optional[Coord]]] = {}
    for (x, y), legs in code.stabilizers.items():
        parity = ((x // 2) + (y // 2)) % 2
        step_of_offset = STEP_OF_OFFSET_ROW if parity == 0 else STEP_OF_OFFSET_COL
        steps: list[Optional[Coord]] = [None, None, None, None]
        for (leg_x, leg_y) in legs:
            steps[step_of_offset[(leg_x - x, leg_y - y)]] = (leg_x, leg_y)
        schedule[(x, y)] = steps
    return schedule
