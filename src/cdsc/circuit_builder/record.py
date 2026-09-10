# Measurement record bookkeeping.

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence
import stim
from ..codes.definition import Coord

# (count, round, coord_base) as of some point in the build.
Snapshot = tuple[int, int, int]


@dataclass
class MeasurementLog:
    # Absolute measurement indices, and the round counters that name them.

    count: int = 0
    round: int = 0
    coord_base: int = 0

    ancilla: dict[tuple[Coord, int], int] = field(default_factory=dict)
    data: dict[Coord, int] = field(default_factory=dict)

    def rel(self, absolute_index: int) -> stim.GateTarget:
        # Turn an absolute measurement index into a Stim rec[] target.
        return stim.target_rec(absolute_index - self.count)

    def record_ancilla(self, ancilla: Coord) -> None:
        # Claim the next measurement index for this ancilla in this round.
        self.ancilla[(ancilla, self.round)] = self.count
        self.count += 1

    def record_data(self, coord: Coord) -> None:
        # Claim the next measurement index for this data qubit's readout.
        self.data[coord] = self.count
        self.count += 1

    def snapshot(self) -> Snapshot:
        # The counters as they stand, for a later advance_rounds().
        return self.count, self.round, self.coord_base

    def advance_rounds(
        self, start: Snapshot, n: int, ancilla_order: Sequence[Coord]
    ) -> None:
        # Jump the counters as if n rounds had been unrolled from `start`.
        count0, round0, coord_base0 = start
        n_ancilla = len(ancilla_order)

        self.round = round0 + n
        self.count = count0 + n * n_ancilla
        self.coord_base = coord_base0 + n
        for i, ancilla in enumerate(ancilla_order):
            self.ancilla[(ancilla, self.round)] = self.count - n_ancilla + i
