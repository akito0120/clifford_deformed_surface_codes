# Circuit fragments shared by the three noise models

from __future__ import annotations
import stim
from ..codes.definition import CodeDefinition, Coord, Pauli
from ..noise.noise_model import NoiseModel
from .gates import ANCILLA_BASIS, BASES, CGATE, MEAS_GATE, PREP_ERROR, PREP_GATE
from .record import MeasurementLog

MEMORY_BASES: tuple[Pauli, ...] = ("X", "Z")


def default_ancilla_order(code: CodeDefinition) -> list[Coord]:
    # The order ancillas are measured in, and so the measurement record order.
    return list(code.stabilizers.keys())


def prep_basis_of(code: CodeDefinition, q: Coord, basis: Pauli) -> Pauli:
    # The basis data qubit q is prepared and measured in, for a memory basis.
    return code.deformation_of(q)[basis]


def data_basis_partition(
    code: CodeDefinition, basis: Pauli
) -> dict[Pauli, list[tuple[Coord, int]]]:
    # Split the data qubits by the basis each is prepared and measured in.
    # Keyed in BASES order, so that iterating the result fixes the order groups are emitted in.
    groups: dict[Pauli, list[tuple[Coord, int]]] = {b: [] for b in BASES}
    for coord, index in code.data_qubits.items():
        groups[prep_basis_of(code, coord, basis)].append((coord, index))
    return groups


def init_qubit_coords(code: CodeDefinition) -> stim.Circuit:
    # QUBIT_COORDS for every qubit: data first, then ancillas.
    circuit = stim.Circuit()
    for coord, index in code.data_qubits.items():
        circuit.append("QUBIT_COORDS", [index], [coord[0], coord[1]])
    for coord, index in code.ancilla_qubits.items():
        circuit.append("QUBIT_COORDS", [index], [coord[0], coord[1]])
    return circuit


def prep_data(code: CodeDefinition, basis: Pauli) -> stim.Circuit:
    # Prepare each data qubit in the basis its deformation assigns it.
    circuit = stim.Circuit()
    for prep, group in data_basis_partition(code, basis).items():
        if group:
            circuit.append(PREP_GATE[prep], [index for _, index in group])
    return circuit


def prep_error(code: CodeDefinition, basis: Pauli, p: float) -> stim.Circuit:
    # Preparation error: flip each data qubit against its own prep basis.
    circuit = stim.Circuit()
    for prep, group in data_basis_partition(code, basis).items():
        if group:
            circuit.append(PREP_ERROR[prep], [index for _, index in group], p)
    return circuit


def data_round_noise(code: CodeDefinition, noise: NoiseModel) -> stim.Circuit:
    # A bulk Pauli channel over every data qubit, once.
    # It stands in for everything that happens to an idle data qubit while a round of syndrome extraction runs.
    # The phenomenological model applies it once per round.
    # The code-capacity model exactly once.
    circuit = stim.Circuit()
    circuit.append(
        "PAULI_CHANNEL_1",
        list(code.data_qubits.values()),
        list(noise.one_qubit_rates),
    )
    return circuit


def syndrome_round(
    code: CodeDefinition,
    log: MeasurementLog,
    ancilla_order: list[Coord],
    flip: float = 0.0,
) -> stim.Circuit:
    # One round of ideal syndrome extraction. flip > 0 adds readout error.
    circuit = stim.Circuit()

    # Reset every ancilla
    for ancilla in ancilla_order:
        circuit.append(PREP_GATE[ANCILLA_BASIS], [code.ancilla_qubits[ancilla]])

    # Apply controlled gates
    for ancilla in ancilla_order:
        ancilla_index = code.ancilla_qubits[ancilla]
        for leg, pauli in code.stabilizers[ancilla].items():
            circuit.append(CGATE[pauli], [ancilla_index, code.data_qubits[leg]])

    # Measure every ancilla
    for ancilla in ancilla_order:
        ancilla_index = code.ancilla_qubits[ancilla]
        if flip > 0.0:
            circuit.append(MEAS_GATE[ANCILLA_BASIS], [ancilla_index], flip)
        else:
            circuit.append(MEAS_GATE[ANCILLA_BASIS], [ancilla_index])
        log.record_ancilla(ancilla)
    return circuit


def consecutive_round_detectors(
    code: CodeDefinition, log: MeasurementLog, ancilla_order: list[Coord]
) -> stim.Circuit:
    # Compare every ancilla against its own measurement in the previous round.
    # A change between consecutive rounds flags an error that occurred in between.
    circuit = stim.Circuit()
    for ancilla in ancilla_order:
        now = log.ancilla[(ancilla, log.round)]
        previous = log.ancilla[(ancilla, log.round - 1)]
        circuit.append(
            "DETECTOR",
            [log.rel(now), log.rel(previous)],
            [ancilla[0], ancilla[1], log.round - log.coord_base],
        )
    return circuit


def data_readout(
    code: CodeDefinition, log: MeasurementLog, basis: Pauli, flip: float = 0.0
) -> stim.Circuit:
    # Measure every data qubit in its own basis, recording indices in log.data.
    # flip > 0 injects a readout error with that probability.
    circuit = stim.Circuit()
    for meas, group in data_basis_partition(code, basis).items():
        if not group:
            continue
        indices = [index for _, index in group]
        if flip > 0.0:
            circuit.append(MEAS_GATE[meas], indices, flip)
        else:
            circuit.append(MEAS_GATE[meas], indices)
        for coord, _ in group:
            log.record_data(coord)
    return circuit


def define_observable(
    code: CodeDefinition, log: MeasurementLog, basis: Pauli
) -> stim.Circuit:
    # Declare the logical observable, reconstructed from the data readout.
    if basis not in MEMORY_BASES:
        raise ValueError(
            f"memory basis must be one of {MEMORY_BASES}, got {basis!r}; a "
            "CodeDefinition declares logical_x and logical_z only"
        )
    logical = code.logical_x if basis == "X" else code.logical_z
    circuit = stim.Circuit()
    circuit.append(
        "OBSERVABLE_INCLUDE", [log.rel(log.data[q]) for q in logical], 0
    )
    return circuit
