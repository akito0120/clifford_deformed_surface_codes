from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import stim
from ..codes.definition import CodeDefinition, Coord, Pauli
from ..noise.noise import Noise
from . import fragments, rounds
from .gates import ANCILLA_BASIS, CGATE, MEAS_GATE, PREP_ERROR, PREP_GATE
from .record import MeasurementLog


def schedule_step_count(code: CodeDefinition) -> int:
    # Number of time steps in the code's extraction schedule.
    if not code.schedule:
        raise ValueError(
            f"code {code.name!r} has no extraction schedule; the circuit-level "
            "model needs one to order the two-qubit gates"
        )
    if set(code.schedule) != set(code.stabilizers):
        missing = sorted(set(code.stabilizers) - set(code.schedule))
        extra = sorted(set(code.schedule) - set(code.stabilizers))
        raise ValueError(
            f"code {code.name!r} schedule does not match its generators: "
            f"missing {missing}, unexpected {extra}"
        )
    step_counts = {len(steps) for steps in code.schedule.values()}
    if len(step_counts) != 1:
        raise ValueError(
            f"code {code.name!r} schedule has generators of differing step "
            f"counts {sorted(step_counts)}; a round takes one fixed number of steps"
        )
    return step_counts.pop()


def noisy_syndrome_round(
    code: CodeDefinition,
    noise: Noise,
    log: MeasurementLog,
    ancilla_order: list[Coord],
    steps: int,
) -> stim.Circuit:
    # One full noisy round of syndrome extraction, in three phases.

    px, py, pz = noise.one_qubit_rates
    two_qubit_rates = noise.two_qubit_rates

    ancilla_indices = [code.ancilla_qubits[a] for a in ancilla_order]
    data_indices = list(code.data_qubits.values())
    all_indices = data_indices + ancilla_indices

    circuit = stim.Circuit()

    # Phase 1: ancilla reset, with its preparation error, and data idling.
    circuit.append(PREP_GATE[ANCILLA_BASIS], ancilla_indices)
    circuit.append(PREP_ERROR[ANCILLA_BASIS], ancilla_indices, noise.p)
    circuit.append("PAULI_CHANNEL_1", data_indices, [px, py, pz])

    # Phase 2: the scheduled two-qubit gates.
    for step in range(steps):
        busy: set[int] = set()
        for ancilla in ancilla_order:
            leg = code.schedule[ancilla][step]
            if leg is None:
                continue
            ancilla_index = code.ancilla_qubits[ancilla]
            data_index = code.data_qubits[leg]
            pauli = code.stabilizers[ancilla][leg]
            circuit.append(CGATE[pauli], [ancilla_index, data_index])
            circuit.append(
                "PAULI_CHANNEL_2", [ancilla_index, data_index], two_qubit_rates
            )
            busy.add(ancilla_index)
            busy.add(data_index)
        idle = [q for q in all_indices if q not in busy]
        if idle:
            circuit.append("PAULI_CHANNEL_1", idle, [px, py, pz])
        circuit.append("TICK")

    # Phase 3: data idling through the measurement window, then readout.
    circuit.append("PAULI_CHANNEL_1", data_indices, [px, py, pz])
    flip = noise.meas_flip
    for ancilla in ancilla_order:
        ancilla_index = code.ancilla_qubits[ancilla]
        if flip > 0.0:
            circuit.append(MEAS_GATE[ANCILLA_BASIS], [ancilla_index], flip)
        else:
            circuit.append(MEAS_GATE[ANCILLA_BASIS], [ancilla_index])
        log.record_ancilla(ancilla)
    return circuit


@dataclass(frozen=True)
class CircuitLevelBuilder:
    code: CodeDefinition
    noise: Noise
    rounds: Optional[int] = None
    basis: Pauli = "X"

    @property
    def n_rounds(self) -> int:
        return self.code.distance if self.rounds is None else self.rounds

    def build(self) -> stim.Circuit:
        code, noise, basis = self.code, self.noise, self.basis
        ancilla_order = fragments.default_ancilla_order(code)
        steps = schedule_step_count(code)
        log = MeasurementLog()

        def syndrome_round() -> stim.Circuit:
            return noisy_syndrome_round(code, noise, log, ancilla_order, steps)

        circuit = stim.Circuit()

        # Prepare the data in its memory basis, noisily.
        circuit += fragments.init_qubit_coords(code)
        circuit += fragments.prep_data(code, basis)
        circuit += fragments.prep_error(code, basis, noise.p)

        # Round 0 is already noisy, so the bottom boundary carries detectors.
        circuit += syndrome_round()
        circuit += rounds.initial_boundary_detectors(code, log, basis)
        circuit.append("TICK")

        # The remaining rounds. Unlike the phenomenological model there is no separate data-noise step:
        # gate and idle errors inside the round are the data noise.
        def round_body() -> stim.Circuit:
            body = syndrome_round()
            body += fragments.consecutive_round_detectors(code, log, ancilla_order)
            return body

        circuit += rounds.repeat_rounds(
            log, ancilla_order, self.n_rounds - 1, round_body
        )

        # Final readout, the top time boundary, and the logical observable.
        circuit += fragments.data_readout(
            code, log, basis, flip=noise.meas_flip
        )
        circuit += rounds.final_boundary_detectors(code, log, basis)
        circuit += fragments.define_observable(code, log, basis)

        return circuit
