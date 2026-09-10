from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Literal, Mapping, Optional

Coord = tuple[int, int]
Pauli = Literal["X", "Y", "Z"]
PauliMap = Mapping[Pauli, Pauli]

PAULIS: tuple[Pauli, ...] = ("X", "Y", "Z")

# Single-qubit clifford deformations
IDENTITY: PauliMap = {"X": "X", "Y": "Y", "Z": "Z"}
H: PauliMap = {"X": "Z", "Y": "Y", "Z": "X"}


@dataclass(frozen=True)
class CodeDefinition:
    name: str
    distance: int

    data_qubits: dict[Coord, int]
    ancilla_qubits: dict[Coord, int]

    stabilizers: dict[Coord, dict[Coord, Pauli]]
    logical_x: dict[Coord, Pauli]
    logical_z: dict[Coord, Pauli]

    schedule: dict[Coord, list[Optional[Coord]]] = field(default_factory=dict)
    deformation: dict[Coord, PauliMap] = field(default_factory=dict)

    def deformation_of(self, q: Coord) -> PauliMap:
        # The clifford deformation on data qubit q. Unrecorded qubits are undeformed.
        return self.deformation.get(q, IDENTITY)

    def with_schedule(
        self, schedule: dict[Coord, list[Optional[Coord]]]
    ) -> CodeDefinition:
        # Return a copy carrying the given extraction schedule.
        return replace(self, schedule=schedule)


def _deform(
    operator: dict[Coord, Pauli], deformation: Mapping[Coord, PauliMap]
) -> dict[Coord, Pauli]:
    # Apply a per-qubit deformation to one Pauli operator, preserving key order.
    return {q: deformation[q][p] if q in deformation else p for q, p in operator.items()}


def apply_deformation(
    code: CodeDefinition,
    deformation: Mapping[Coord, PauliMap],
    *,
    name: Optional[str] = None,
) -> CodeDefinition:
    # Deform the Paulis on the given data qubits.
    unknown = set(deformation) - set(code.data_qubits)
    if unknown:
        raise ValueError(
            f"deformation refers to coordinates that are not data qubits: {sorted(unknown)}"
        )

    composed = dict(code.deformation)
    for q, relabeling in deformation.items():
        current = code.deformation_of(q)
        composed[q] = {p: relabeling[current[p]] for p in PAULIS}

    return replace(
        code,
        name=code.name if name is None else name,
        stabilizers={
            ancilla: _deform(legs, deformation)
            for ancilla, legs in code.stabilizers.items()
        },
        logical_x=_deform(code.logical_x, deformation),
        logical_z=_deform(code.logical_z, deformation),
        deformation=composed,
    )
