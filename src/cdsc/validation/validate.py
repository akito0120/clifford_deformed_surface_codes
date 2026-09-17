from dataclasses import dataclass
from .check_result import CheckResult
from .code_checks import CodeValidationError, CODE_CHECK_NAMES, check_code
from .circuit_checks import (
    CIRCUIT_CHECK_NAMES, DEFAULT_BASES, VALIDATION_NOISE,
    check_circuit
)
from ..codes.definition import CodeDefinition, Pauli
from typing import Optional, Sequence, Iterable
from ..noise.noise_model import NoiseModel


CHECK_NAMES: tuple[str, ...] = CODE_CHECK_NAMES + CIRCUIT_CHECK_NAMES


@dataclass(frozen=True)
class CodeValidation:
    # All six checks on one code, in one record.

    key: str
    results: tuple[CheckResult, ...]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    @property
    def failures(self) -> tuple[CheckResult, ...]:
        return tuple(result for result in self.results if not result.passed)

    def as_json(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "checks": {result.name: result.as_json() for result in self.results},
        }

    def raise_if_failed(self) -> None:
        # Stop a run rather than sweep a code the framework cannot trust.
        if self.passed:
            return
        raise CodeValidationError(
            f"code {self.key!r} failed {len(self.failures)} of {len(CHECK_NAMES)} "
            "checks:\n"
            + "\n".join(f"  {result.name}: {result.message}" for result in self.failures)
        )


def record_key(code: CodeDefinition, code_id: Optional[str] = None) -> str:
    # The validation.json key: the config's code id plus the distance.
    return code.name if code_id is None else f"{code_id}_d{code.distance}"


def validate_code(
    code: CodeDefinition,
    *,
    code_id: Optional[str] = None,
    bases: Sequence[Pauli] = DEFAULT_BASES,
    noise: NoiseModel = VALIDATION_NOISE,
    rounds: Optional[int] = None,
) -> CodeValidation:
    # Run all six checks on one code.
    code_results = check_code(code)
    circuit_results = check_circuit(code, list(bases), noise, rounds)
    results = (
        *code_results,
        *circuit_results
    )
    return CodeValidation(key=record_key(code, code_id), results=results)


def validate_codes(
    codes: Iterable[CodeDefinition],
    *,
    code_ids: Optional[Sequence[str]] = None,
    bases: Sequence[Pauli] = DEFAULT_BASES,
    noise: NoiseModel = VALIDATION_NOISE,
    rounds: Optional[int] = None,
    workers: int = 1,
) -> list[CodeValidation]:
    # Validate several codes, optionally in parallel.
    codes = list(codes)
    if code_ids is None:
        ids: list[Optional[str]] = [None] * len(codes)
    else:
        ids = list(code_ids)
        if len(ids) != len(codes):
            raise ValueError(
                f"code_ids has {len(ids)} entries for {len(codes)} codes; pass "
                "one id per code, in the same order"
            )

    if workers == 1 or len(codes) < 2:
        return [
            validate_code(code, code_id=code_id, bases=bases, noise=noise, rounds=rounds)
            for code, code_id in zip(codes, ids)
        ]

    from joblib import Parallel, delayed  # imported here: only this path needs it

    return list(
        Parallel(n_jobs=workers)(
            delayed(validate_code)(
                code, code_id=code_id, bases=bases, noise=noise, rounds=rounds
            )
            for code, code_id in zip(codes, ids)
        )
    )


def validation_report(validations: Iterable[CodeValidation]) -> dict[str, object]:
    # The validation.json content: one record per validated code.
    return {validation.key: validation.as_json() for validation in validations}
