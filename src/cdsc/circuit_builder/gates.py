# Stim gates

from __future__ import annotations
from ..codes.definition import Pauli

# Emission order for anything that groups data qubits by basis.
BASES: tuple[Pauli, ...] = ("X", "Y", "Z")

# A stabilizer leg's Pauli -> the controlled gate that couples it to the ancilla.
CGATE: dict[Pauli, str] = {"X": "CX", "Y": "CY", "Z": "CZ"}

# Preparation and measurement in a given basis.
PREP_GATE: dict[Pauli, str] = {"X": "RX", "Y": "RY", "Z": "R"}
MEAS_GATE: dict[Pauli, str] = {"X": "MX", "Y": "MY", "Z": "M"}

# The error channel that flips a qubit prepared in a given basis
# i.e. a Pauli that anticommutes with it
PREP_ERROR: dict[Pauli, str] = {"X": "Z_ERROR", "Y": "Z_ERROR", "Z": "X_ERROR"}

# Ancillas are always prepared and measured in X basis
ANCILLA_BASIS: Pauli = "X"
