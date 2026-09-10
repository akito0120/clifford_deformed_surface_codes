# Multi-round structure and the time boundaries

from __future__ import annotations
from typing import Callable
import stim
from ..codes.definition import CodeDefinition, Coord, Pauli
from .fragments import prep_basis_of
from .record import MeasurementLog


def eligible_boundary_stabilizers(
    code: CodeDefinition, basis: Pauli
) -> list[Coord]:
    # Stabilizers whose value is fixed by the product-state preparation.
    prep = {q: prep_basis_of(code, q, basis) for q in code.data_qubits}
    return [
        ancilla
        for ancilla, legs in code.stabilizers.items()
        if all(pauli == prep[q] for q, pauli in legs.items())
    ]


def initial_boundary_detectors(
    code: CodeDefinition, log: MeasurementLog, basis: Pauli
) -> stim.Circuit:
    # Bottom time boundary: round 0 against the known preparation.
    circuit = stim.Circuit()
    for ancilla in eligible_boundary_stabilizers(code, basis):
        first = log.ancilla[(ancilla, 0)]
        circuit.append(
            "DETECTOR",
            [log.rel(first)],
            [ancilla[0], ancilla[1], 0 - log.coord_base],
        )
    return circuit


def final_boundary_detectors(
    code: CodeDefinition, log: MeasurementLog, basis: Pauli
) -> stim.Circuit:
    # Top time boundary: each check rebuilt from the data readout, vs the last round.
    circuit = stim.Circuit()
    last = log.round
    for ancilla in eligible_boundary_stabilizers(code, basis):
        targets = [log.rel(log.data[q]) for q in code.stabilizers[ancilla]]
        targets.append(log.rel(log.ancilla[(ancilla, last)]))
        circuit.append("DETECTOR", targets, [ancilla[0], ancilla[1], last + 1])
    return circuit


def repeat_rounds(
    log: MeasurementLog,
    ancilla_order: list[Coord],
    n: int,
    round_body: Callable[[], stim.Circuit],
) -> stim.Circuit:
    # Emit n identical rounds as a stim REPEAT block.
    if n <= 0:
        return stim.Circuit()

    start = log.snapshot()

    body = stim.Circuit()
    body.append("SHIFT_COORDS", [], [0, 0, 1])
    log.coord_base += 1
    log.round += 1
    body += round_body()
    body.append("TICK")

    log.advance_rounds(start, n, ancilla_order)
    return body * n
