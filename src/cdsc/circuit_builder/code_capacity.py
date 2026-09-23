from __future__ import annotations
from dataclasses import dataclass
import stim
from ..codes.definition import CodeDefinition, Pauli
from ..noise.noise import Noise
from . import fragments
from .record import MeasurementLog


@dataclass(frozen=True)
class CodeCapacityBuilder:
    code: CodeDefinition
    noise: Noise
    basis: Pauli = "X"

    def build(self) -> stim.Circuit:
        code, noise, basis = self.code, self.noise, self.basis
        ancilla_order = fragments.default_ancilla_order(code)
        log = MeasurementLog()

        circuit = stim.Circuit()

        circuit += fragments.init_qubit_coords(code)
        circuit += fragments.prep_data(code, basis)

        # The reference round, projecting into the code space.
        circuit += fragments.syndrome_round(code, log, ancilla_order)
        circuit.append("TICK")

        # There is no REPEAT block to advance the round counter, so do it here.
        log.round += 1

        circuit += fragments.data_round_noise(code, noise)
        circuit += fragments.syndrome_round(code, log, ancilla_order)
        circuit += fragments.consecutive_round_detectors(code, log, ancilla_order)

        # Perfect data readout and the observable. No time-boundary detectors.
        circuit += fragments.data_readout(code, log, basis)
        circuit += fragments.define_observable(code, log, basis)

        return circuit
