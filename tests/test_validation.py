from dataclasses import replace
from itertools import combinations
import pytest
from cdsc.codes.definition import H
from cdsc.codes.lattice import STEP_OF_OFFSET_ROW
from cdsc.codes.registry import build_code, registered_codes
from cdsc.validation.validate import CHECK_NAMES, validate_code


# Every built-in code passes all checks, reported in the documented order
@pytest.mark.parametrize("d", [3, 5])
@pytest.mark.parametrize("name", registered_codes())
def test_builtin_codes_pass_every_check(name, d):
    validation = validate_code(build_code(name, distance=d))
    assert validation.passed, [(r.name, r.message) for r in validation.failures]
    assert [r.name for r in validation.results] == list(CHECK_NAMES)


def _flip_one_leg(code):
    # One leg of a weight-4 check gets the other Pauli type
    ancilla, legs = next((a, legs) for a, legs in code.stabilizers.items() if len(legs) == 4)
    q = next(iter(legs))
    flipped = {**legs, q: "Z" if legs[q] == "X" else "X"}
    return replace(code, stabilizers={**code.stabilizers, ancilla: flipped})


def _single_qubit_logical_z(code):
    # A single Z anticommutes with the X checks on that qubit
    return replace(code, logical_z={(1, 1): "Z"})


def _duplicate_check(code):
    # A copy of an existing check on a new ancilla: m grows, the rank does not
    ancilla, legs = next(iter(code.stabilizers.items()))
    copy = (-2, -2)
    return replace(
        code,
        stabilizers={**code.stabilizers, copy: dict(legs)},
        ancilla_qubits={**code.ancilla_qubits, copy: max(code.ancilla_qubits.values()) + 1},
        schedule={**code.schedule, copy: list(code.schedule[ancilla])},
    )


def _deform_without_relabeling(code):
    # A deformation recorded on one qubit but not applied to the operators:
    # the algebra still checks out, but that qubit is prepared and measured in the wrong basis
    q = next(iter(code.data_qubits))
    return replace(code, deformation={q: H})


def _drop_one_check(code):
    # One generator fewer leaves two logical qubits
    ancilla = next(iter(code.stabilizers))
    return replace(
        code,
        stabilizers={a: legs for a, legs in code.stabilizers.items() if a != ancilla},
        ancilla_qubits={a: i for a, i in code.ancilla_qubits.items() if a != ancilla},
        schedule={a: steps for a, steps in code.schedule.items() if a != ancilla},
    )


def _colliding_schedule(code):
    # Two ancillas reach for the same data qubit in the same step
    schedule = {a: list(steps) for a, steps in code.schedule.items()}
    for a, b in combinations(schedule, 2):
        for step, leg in enumerate(schedule[a]):
            if leg is not None and leg in schedule[b] and schedule[b].index(leg) != step:
                other = schedule[b].index(leg)
                schedule[b][step], schedule[b][other] = schedule[b][other], schedule[b][step]
                return replace(code, schedule=schedule)
    raise AssertionError("no pair of checks shares a data qubit")


def _hook_error_schedule(code):
    # The same row-major CNOT order for every check lets hook errors shorten the circuit distance
    schedule = {}
    for (x, y), legs in code.stabilizers.items():
        steps = [None] * 4
        for leg_x, leg_y in legs:
            steps[STEP_OF_OFFSET_ROW[(leg_x - x, leg_y - y)]] = (leg_x, leg_y)
        schedule[(x, y)] = steps
    return replace(code, schedule=schedule)


# Each check catches the corruption it exists to catch
@pytest.mark.parametrize("d", [3, 5])
@pytest.mark.parametrize(
    "corrupt, check",
    [
        (_flip_one_leg, "stabilizer_commutation"),
        (_single_qubit_logical_z, "logical_operators"),
        (_duplicate_check, "generator_independence"),
        (_drop_one_check, "logical_qubit_count"),
        (_colliding_schedule, "schedule_consistency"),
        (_deform_without_relabeling, "detector_determinism"),
        (_hook_error_schedule, "distance_preservation"),
    ],
    ids=lambda value: getattr(value, "__name__", value),
)
def test_broken_code_fails_the_matching_check(corrupt, check, d):
    validation = validate_code(corrupt(build_code("rotated_surface", distance=d)))
    assert check in {r.name for r in validation.failures}
