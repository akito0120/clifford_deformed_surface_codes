from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence
from ..circuit_builder.circuit_level import CircuitLevelBuilder
from .check_result import CheckResult
from ..codes.definition import CodeDefinition, Pauli
from ..noise import NoiseModel

CIRCUIT_CHECK_NAMES: tuple[str, ...] = (
    "detector_determinism",
    "distance_preservation",
)
DEFAULT_BASES: tuple[Pauli, ...] = ("X", "Z")
VALIDATION_NOISE = NoiseModel(p=0.1, eta=0.5)


@dataclass(frozen=True)
class _BasisOutcome:
    # What one memory basis produced, before the two checks are separated.
    basis: Pauli
    deterministic: bool
    determinism_error: str = ""
    measured_distance: Optional[int] = None
    distance_error: str = ""


def _evaluate(
    code: CodeDefinition,
    bases: Sequence[Pauli],
    noise: NoiseModel,
    rounds: Optional[int],
) -> list[_BasisOutcome]:
    # Build each basis's circuit once and run both checks
    if not bases:
        raise ValueError(
            "no memory bases to validate; checks 5 and 6 have nothing to "
            f"measure. Pass at least one of {DEFAULT_BASES}"
        )

    outcomes: list[_BasisOutcome] = []
    for basis in bases:
        try:
            circuit = CircuitLevelBuilder(
                code=code, noise=noise, rounds=rounds, basis=basis
            ).build()
            circuit.detector_error_model(approximate_disjoint_errors=True)
        except Exception as error:
            outcomes.append(
                _BasisOutcome(
                    basis=basis,
                    deterministic=False,
                    determinism_error=f"{type(error).__name__}: {error}",
                    distance_error="not evaluated: the circuit is not valid",
                )
            )
            continue

        try:
            measured = len(circuit.shortest_graphlike_error())
            outcomes.append(
                _BasisOutcome(basis=basis, deterministic=True, measured_distance=measured)
            )
        except Exception as error:
            outcomes.append(
                _BasisOutcome(
                    basis=basis,
                    deterministic=True,
                    distance_error=f"{type(error).__name__}: {error}",
                )
            )
    return outcomes


def _determinism_result(outcomes: Sequence[_BasisOutcome]) -> CheckResult:
    bases = [outcome.basis for outcome in outcomes]
    failures = [outcome for outcome in outcomes if not outcome.deterministic]

    detail: dict[str, object] = {"bases": list(bases)}
    if not failures:
        return CheckResult(CIRCUIT_CHECK_NAMES[0], True, detail=detail)

    detail["failed_bases"] = [outcome.basis for outcome in failures]
    return CheckResult(
        CIRCUIT_CHECK_NAMES[0],
        False,
        "; ".join(
            f"memory basis {outcome.basis}: {outcome.determinism_error}"
            for outcome in failures
        ),
        detail,
    )


def _distance_result(
    code: CodeDefinition, outcomes: Sequence[_BasisOutcome]
) -> CheckResult:
    bases = [outcome.basis for outcome in outcomes]
    measured = {
        outcome.basis: outcome.measured_distance
        for outcome in outcomes
        if outcome.measured_distance is not None
    }

    detail: dict[str, object] = {"declared": code.distance, "bases": list(bases)}

    unmeasured = [outcome for outcome in outcomes if outcome.measured_distance is None]
    wrong = {b: d for b, d in measured.items() if d != code.distance}

    if not unmeasured and not wrong:
        # Every basis agreed, so the scalar in validation.json is unambiguous.
        detail["measured"] = code.distance
        return CheckResult(CIRCUIT_CHECK_NAMES[1], True, detail=detail)

    if not unmeasured:
        detail["measured"] = min(measured.values())
    detail["by_basis"] = dict(measured)

    problems = [
        f"memory basis {outcome.basis}: {outcome.distance_error}"
        for outcome in unmeasured
    ]
    problems += [
        f"memory basis {basis}: graphlike distance {found} != declared "
        f"{code.distance}"
        for basis, found in wrong.items()
    ]
    return CheckResult(CIRCUIT_CHECK_NAMES[1], False, "; ".join(problems), detail)


def check_circuit(
    code: CodeDefinition, 
    bases: Sequence[Pauli], 
    noise: NoiseModel,
    rounds: Optional[int]
) -> list[CheckResult]:
    # Run all circuit checks in CIRCUIT_CHECK_NAMES order
    outcomes = _evaluate(code, list(bases), noise, rounds)
    return [
        _determinism_result(outcomes),
        _distance_result(code, outcomes)
    ]
