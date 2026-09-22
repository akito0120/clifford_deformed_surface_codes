from __future__ import annotations
from dataclasses import dataclass, replace


SAME_AS_P = "same_as_p"


@dataclass(frozen=True)
class Noise:
    p :float
    meas_flip: float
    one_qubit_rates: tuple[float, float, float]
    two_qubit_rates: list[float]

    def with_p_meas(self, p_meas: str | float) -> Noise:
        # Return a copy whose measurement flip rate is the configured p_meas
        if p_meas == SAME_AS_P:
            return self
        if isinstance(p_meas, str):
            raise ValueError(
                f"invalid p_meas specified: {p_meas!r}; use {SAME_AS_P!r} or a number"
            )
        return replace(self, meas_flip=float(p_meas))
