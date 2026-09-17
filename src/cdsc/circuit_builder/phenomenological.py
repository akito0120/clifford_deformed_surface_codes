from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import stim
from ..codes.definition import CodeDefinition, Pauli
from ..noise.noise_model import NoiseModel
from . import fragments, rounds
from .record import MeasurementLog


@dataclass(frozen=True)
class PhenomenologicalBuilder:
    code: CodeDefinition
    noise: NoiseModel
    rounds: Optional[int] = None
    basis: Pauli = "X"

    @property
    def n_rounds(self) -> int:
        return self.code.distance if self.rounds is None else self.rounds

    def build(self) -> stim.Circuit:
        code, noise, basis = self.code, self.noise, self.basis
        ancilla_order = fragments.default_ancilla_order(code)
        flip = noise.meas_flip
        log = MeasurementLog()

        def noisy_round() -> stim.Circuit:
            circuit = fragments.data_round_noise(code, noise)
            circuit += fragments.syndrome_round(code, log, ancilla_order, flip=flip)
            return circuit

        circuit = stim.Circuit()

        # Prepare the data in its memory basis.
        circuit += fragments.init_qubit_coords(code)
        circuit += fragments.prep_data(code, basis)

        # Round 0 is noisy, so the bottom boundary carries detectors.
        circuit += noisy_round()
        circuit += rounds.initial_boundary_detectors(code, log, basis)
        circuit.append("TICK")

        def round_body() -> stim.Circuit:
            body = noisy_round()
            body += fragments.consecutive_round_detectors(code, log, ancilla_order)
            return body

        circuit += rounds.repeat_rounds(
            log, ancilla_order, self.n_rounds - 1, round_body
        )

        # Final readout, the top time boundary, and the logical observable.
        circuit += fragments.data_readout(code, log, basis, flip=flip)
        circuit += rounds.final_boundary_detectors(code, log, basis)
        circuit += fragments.define_observable(code, log, basis)

        return circuit
