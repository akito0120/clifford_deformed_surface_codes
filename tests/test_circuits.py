import pytest
from pytest import approx
from cdsc.circuit_builder import build_circuit
from cdsc.codes.registry import build_code, registered_codes
from cdsc.noise.builtin import (
    biased_pauli_rates,
    biased_two_qubit_rates,
    depolarizing_noise,
    depolarizing_pauli_rates,
    depolarizing_two_qubit_rates,
)


MODELS = ["code_capacity", "phenomenological", "circuit_level"]


def _circuit(model, code, basis, d):
    return build_circuit(model, build_code(code, distance=d), depolarizing_noise(0.001, None), basis)


every_circuit = pytest.mark.parametrize(
    "model, code, basis, d",
    [
        (model, code, basis, d)
        for model in MODELS
        for code in registered_codes()
        for basis in ("X", "Z")
        for d in (3, 5)
    ],
)


# Every detector and the observable are deterministic in the noiseless circuit
@every_circuit
def test_circuit_is_deterministic(model, code, basis, d):
    # Stim refuses to build a detector error model if a detector or the observable is not deterministic
    circuit = _circuit(model, code, basis, d)
    dem = circuit.detector_error_model(decompose_errors=True, approximate_disjoint_errors=True)
    assert dem.num_observables == 1


# The shortest graphlike error in the circuit has exactly the code distance
@every_circuit
def test_circuit_distance_equals_code_distance(model, code, basis, d):
    circuit = _circuit(model, code, basis, d)
    assert len(circuit.shortest_graphlike_error()) == d


# Depolarizing noise is invariant under single-qubit Cliffords, so a deformed code has the CSS code's error model
@pytest.mark.parametrize(
    "model, code, basis, d",
    [
        (model, code, basis, d)
        for model in MODELS
        for code in ("xzzx", "xy")
        for basis in ("X", "Z")
        for d in (3, 5)
    ],
)
def test_deformed_code_matches_css_under_depolarizing_noise(model, code, basis, d):
    assert build_code(code, distance=d).stabilizers != build_code("rotated_surface", distance=d).stabilizers
    # Compared undecomposed: Stim's decomposition into graphlike edges is not Clifford-invariant
    deformed = _circuit(model, code, basis, d).detector_error_model(approximate_disjoint_errors=True)
    css = _circuit(model, "rotated_surface", basis, d).detector_error_model(approximate_disjoint_errors=True)
    assert deformed.approx_equals(css, atol=1e-12)


# Biased rates sum to p and split Z against X + Y in the ratio eta
@pytest.mark.parametrize("eta", [0.5, 1.0, 10.0])
def test_biased_rates_sum_to_p_with_the_given_bias(eta):
    p = 0.01
    px, py, pz = biased_pauli_rates(p, eta)
    assert px + py + pz == approx(p)
    assert pz / (px + py) == approx(eta)
    assert sum(biased_two_qubit_rates(p, eta)) == approx(p)


# Infinite bias leaves only Z errors
def test_infinite_bias_is_pure_z():
    p = 0.01
    assert biased_pauli_rates(p, float("inf")) == (0.0, 0.0, p)
    assert sum(biased_two_qubit_rates(p, float("inf"))) == approx(p)


# Depolarizing noise spreads p evenly over the 3 one-qubit and 15 two-qubit Paulis
def test_depolarizing_rates_are_uniform():
    p = 0.01
    assert depolarizing_pauli_rates(p) == approx((p / 3,) * 3)
    two_qubit = depolarizing_two_qubit_rates(p)
    assert len(two_qubit) == 15
    assert two_qubit == approx([p / 15] * 15)
