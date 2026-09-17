from dataclasses import dataclass


@dataclass(frozen=True)
class NoiseModel:
    p :float
    meas_flip: float
    one_qubit_rates: tuple[float, float, float]
    two_qubit_rates: list[float]
