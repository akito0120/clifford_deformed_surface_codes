from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

Channel = Literal["biased", "depolarizing"]

# Two-qubit Pauli labels in the order Stim's PAULI_CHANNEL_2 expects its arguments.
TWO_QUBIT_PAULIS: tuple[str, ...] = (
    "IX", "IY", "IZ",
    "XI", "XX", "XY", "XZ",
    "YI", "YX", "YY", "YZ",
    "ZI", "ZX", "ZY", "ZZ",
)

# The three two-qubit terms that carry the bias: those made only of I and Z.
BIASED_TWO_QUBIT_PAULIS = frozenset({"IZ", "ZI", "ZZ"})


def biased_pauli_rates(p: float, eta: float) -> tuple[float, float, float]:
    # Single-qubit (p_X, p_Y, p_Z) at total rate p and bias eta = p_Z/(p_X+p_Y).
    if eta == float("inf"):
        return 0.0, 0.0, p
    px = py = p / (2.0 * (1.0 + eta))
    pz = p * eta / (1.0 + eta)
    return px, py, pz


def biased_two_qubit_rates(p: float, eta: float) -> list[float]:
    # The 15 two-qubit rates, biased towards the I/Z-only terms.
    # Returned in TWO_QUBIT_PAULIS order for direct use as PAULI_CHANNEL_2 args.
    if eta == float("inf"):
        return [
            p / 3.0 if ab in BIASED_TWO_QUBIT_PAULIS else 0.0
            for ab in TWO_QUBIT_PAULIS
        ]
    p_high = p * eta / (3.0 * (1.0 + eta))
    p_low = p / (12.0 * (1.0 + eta))
    return [
        p_high if ab in BIASED_TWO_QUBIT_PAULIS else p_low
        for ab in TWO_QUBIT_PAULIS
    ]


def depolarizing_pauli_rates(p: float) -> tuple[float, float, float]:
    # Single-qubit depolarizing: every non-identity Pauli equally likely.
    return p / 3.0, p / 3.0, p / 3.0


def depolarizing_two_qubit_rates(p: float) -> list[float]:
    # Two-qubit depolarizing: all 15 non-identity pairs equally likely.
    return [p / 15.0] * len(TWO_QUBIT_PAULIS)


@dataclass(frozen=True)
class NoiseModel:
    # A physical error rate together with the channel that shapes it.

    p: float
    channel: Channel = "biased"
    eta: float = 0.5
    p_meas: Optional[float] = None

    def __post_init__(self) -> None:
        if self.channel not in ("biased", "depolarizing"):
            raise ValueError(
                f"channel must be 'biased' or 'depolarizing', got {self.channel!r}"
            )

    @property
    def measurement_flip(self) -> float:
        # Readout flip probability.
        return self.p if self.p_meas is None else self.p_meas

    def one_qubit_rates(self) -> tuple[float, float, float]:
        # (p_X, p_Y, p_Z) for PAULI_CHANNEL_1.
        if self.channel == "depolarizing":
            return depolarizing_pauli_rates(self.p)
        return biased_pauli_rates(self.p, self.eta)

    def two_qubit_rates(self) -> list[float]:
        # The 15 rates for PAULI_CHANNEL_2, in TWO_QUBIT_PAULIS order.
        if self.channel == "depolarizing":
            return depolarizing_two_qubit_rates(self.p)
        return biased_two_qubit_rates(self.p, self.eta)
