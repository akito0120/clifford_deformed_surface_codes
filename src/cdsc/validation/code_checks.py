from __future__ import annotations
from typing import Mapping, Optional
from ..codes.definition import CodeDefinition, Coord, Pauli
from .check_result import CheckResult


CODE_CHECK_NAMES: tuple[str, ...] = (
    "stabilizer_commutation",
    "logical_operators",
    "generator_independence",
    "logical_qubit_count",
    "schedule_consistency",
)

# How many offending items a failure message names before saying "and N more".
_MAX_REPORTED = 5


class CodeValidationError(ValueError):
    pass


# --- shared machinery --------------------------------------------------------


def _anticommute(a: Mapping[Coord, Pauli], b: Mapping[Coord, Pauli]) -> bool:
    # Whether two Pauli operators anticommute.
    disagreements = sum(1 for q, pauli in a.items() if q in b and b[q] != pauli)
    return disagreements % 2 == 1


def _unknown_coordinates(
    operator: Mapping[Coord, Pauli], code: CodeDefinition
) -> list[Coord]:
    # Qubits that appear in the operand, but not in the data qubits
    return sorted(set(operator) - set(code.data_qubits))


def _require_data_qubits(code: CodeDefinition) -> None:
    # Reject operators acting on coordinates that are not data qubits.
    for label, operator in (
        *((f"stabilizer {a}", legs) for a, legs in code.stabilizers.items()),
        ("logical_x", code.logical_x),
        ("logical_z", code.logical_z),
    ):
        unknown = _unknown_coordinates(operator, code)
        if unknown:
            raise ValueError(
                f"{label} refers to coordinates that are not data qubits: {unknown}"
            )


def _symplectic_row(
    operator: Mapping[Coord, Pauli], index: Mapping[Coord, int], n: int
) -> int:
    # Encode one Pauli operator as a 2n-bit row [X part | Z part].
    # Bit i is set when the operator has an X component on data qubit i, bit n + i when it has a Z component.
    # Y sets both, which is what makes this work for a deformed code where one generator mixes bases.
    row = 0
    for q, pauli in operator.items():
        i = index[q]
        if pauli in ("X", "Y"):
            row |= 1 << i
        if pauli in ("Z", "Y"):
            row |= 1 << (n + i)
    return row


def _gf2_rank(rows: list[int]) -> int:
    # Rank over GF(2) of rows given as bitsets.
    # Gaussian elimination where each row is a Python int:
    # reduce a row against the stored basis vector sharing its leading bit
    # until it either finds a free leading bit, and joins the basis, or vanishes, and was dependent.
    basis: dict[int, int] = {}
    for row in rows:
        while row:
            leading = row.bit_length() - 1
            if leading not in basis:
                basis[leading] = row
                break
            row ^= basis[leading]
    return len(basis)


def check_matrix_rank(code: CodeDefinition) -> int:
    # GF(2) rank of the symplectic check matrix. Shared by checks 3a and 3b.
    _require_data_qubits(code)
    n = len(code.data_qubits)
    index = {q: i for i, q in enumerate(code.data_qubits)}
    return _gf2_rank(
        [_symplectic_row(legs, index, n) for legs in code.stabilizers.values()]
    )


def _summarise(items: list[str]) -> str:
    shown = ", ".join(items[:_MAX_REPORTED])
    remaining = len(items) - _MAX_REPORTED
    return f"{shown} and {remaining} more" if remaining > 0 else shown


# --- check 1 -----------------------------------------------------------------


def check_stabilizer_commutation(code: CodeDefinition) -> CheckResult:
    # Check 1: every pair of generators commutes.
    _require_data_qubits(code)
    ancillas = list(code.stabilizers)
    offenders: list[tuple[Coord, Coord]] = [
        (ancillas[i], ancillas[j])
        for i in range(len(ancillas))
        for j in range(i + 1, len(ancillas))
        if _anticommute(code.stabilizers[ancillas[i]], code.stabilizers[ancillas[j]])
    ]

    detail: dict[str, object] = {"generators": len(ancillas)}
    if not offenders:
        return CheckResult(CODE_CHECK_NAMES[0], True, detail=detail)

    detail["anticommuting_pairs"] = len(offenders)
    detail["examples"] = [[list(a), list(b)] for a, b in offenders[:_MAX_REPORTED]]
    return CheckResult(
        CODE_CHECK_NAMES[0],
        False,
        f"{len(offenders)} generator pair(s) anticommute: "
        + _summarise([f"{a} with {b}" for a, b in offenders]),
        detail,
    )


# --- check 2 -----------------------------------------------------------------


def check_logical_operators(code: CodeDefinition) -> CheckResult:
    # Check 2: the logical operators are logical, and are a conjugate pair.
    _require_data_qubits(code)
    problems: list[str] = []
    detail: dict[str, object] = {}

    for label, logical in (("logical_x", code.logical_x), ("logical_z", code.logical_z)):
        clashes = [
            ancilla
            for ancilla, legs in code.stabilizers.items()
            if _anticommute(logical, legs)
        ]
        if clashes:
            detail[f"{label}_anticommuting_stabilizers"] = len(clashes)
            problems.append(
                f"{label} anticommutes with {len(clashes)} stabilizer(s): "
                + _summarise([str(a) for a in clashes])
            )

    if not _anticommute(code.logical_x, code.logical_z):
        detail["logicals_anticommute"] = False
        problems.append(
            "logical_x and logical_z commute; a conjugate pair must anticommute"
        )

    if problems:
        return CheckResult(CODE_CHECK_NAMES[1], False, "; ".join(problems), detail)
    return CheckResult(CODE_CHECK_NAMES[1], True, detail=detail)


# --- checks 3a and 3b --------------------------------------------------------


def check_generator_independence(
    code: CodeDefinition, *, rank: Optional[int] = None
) -> CheckResult:
    # Check 3a: the m generators are independent, i.e. the rank is m.
    n = len(code.data_qubits)
    m = len(code.stabilizers)
    rank = check_matrix_rank(code) if rank is None else rank

    detail = {"n": n, "m": m, "rank": rank}
    if rank == m:
        return CheckResult(CODE_CHECK_NAMES[2], True, detail=detail)
    return CheckResult(
        CODE_CHECK_NAMES[2],
        False,
        f"check matrix rank {rank} is below the generator count {m}: "
        f"{m - rank} generator(s) are dependent on the others (duplicated, or a "
        "product of others)",
        detail,
    )


def check_logical_qubit_count(
    code: CodeDefinition, *, rank: Optional[int] = None
) -> CheckResult:
    # Check 3b: the code encodes exactly one logical qubit.
    n = len(code.data_qubits)
    rank = check_matrix_rank(code) if rank is None else rank
    expected = n - 1

    detail = {"rank": rank, "expected": expected, "k": n - rank}
    if rank == expected:
        return CheckResult(CODE_CHECK_NAMES[3], True, detail=detail)
    return CheckResult(
        CODE_CHECK_NAMES[3],
        False,
        f"check matrix rank {rank} implies k = {n - rank} logical qubit(s), "
        f"but the framework tracks exactly one (rank must be n - 1 = {expected})",
        detail,
    )


# --- check 4 -----------------------------------------------------------------


def check_schedule_consistency(code: CodeDefinition) -> CheckResult:
    # Check 4: the schedule is a runnable ordering of the two-qubit gates.
    # Four ways it can fail:
    # - It does not cover exactly the generators,
    # - Its generators disagree on how many steps a round takes,
    # - Two ancillas reach for the same data qubit in one step,
    # - A generator's legs are not covered exactly once.

    if not code.schedule:
        return CheckResult(
            CODE_CHECK_NAMES[4],
            True,
            detail={"steps": 0, "scheduled": False},
        )

    missing = sorted(set(code.stabilizers) - set(code.schedule))
    extra = sorted(set(code.schedule) - set(code.stabilizers))
    if missing or extra:
        return CheckResult(
            CODE_CHECK_NAMES[4],
            False,
            f"schedule does not cover the generators: missing {missing}, "
            f"unexpected {extra}",
            {"scheduled": True, "missing": len(missing), "unexpected": len(extra)},
        )

    step_counts = {len(steps) for steps in code.schedule.values()}
    if len(step_counts) != 1:
        return CheckResult(
            CODE_CHECK_NAMES[4],
            False,
            f"generators disagree on the number of time steps: "
            f"{sorted(step_counts)}; a round takes one fixed number of steps",
            {"scheduled": True, "step_counts": sorted(step_counts)},
        )
    steps = step_counts.pop()

    problems: list[str] = []
    detail: dict[str, object] = {"steps": steps, "scheduled": True}

    # One data qubit cannot be the target of two gates in the same time step.
    for step in range(steps):
        seen: dict[Coord, Coord] = {}
        collisions: list[str] = []
        for ancilla, legs in code.schedule.items():
            leg = legs[step]
            if leg is None:
                continue
            if leg in seen:
                collisions.append(f"{leg} by {seen[leg]} and {ancilla}")
            else:
                seen[leg] = ancilla
        if collisions:
            problems.append(f"step {step}: " + _summarise(collisions))
    if problems:
        detail["colliding_steps"] = len(problems)

    # Every leg coupled exactly once, and nothing that is not a leg.
    coverage: list[str] = []
    for ancilla, legs in code.stabilizers.items():
        scheduled = [leg for leg in code.schedule[ancilla] if leg is not None]
        if sorted(scheduled) != sorted(legs):
            coverage.append(
                f"{ancilla} couples {sorted(scheduled)} but its legs are {sorted(legs)}"
            )
    if coverage:
        detail["miscovered_generators"] = len(coverage)
        problems.append("leg coverage: " + _summarise(coverage))

    if problems:
        return CheckResult(CODE_CHECK_NAMES[4], False, "; ".join(problems), detail)
    return CheckResult(CODE_CHECK_NAMES[4], True, detail=detail)


# --- orchestration -----------------------------------------------------------


def check_code(code: CodeDefinition) -> list[CheckResult]:
    # Run checks 1-4, in CODE_CHECK_NAMES order.
    rank = check_matrix_rank(code)
    return [
        check_stabilizer_commutation(code),
        check_logical_operators(code),
        check_generator_independence(code, rank=rank),
        check_logical_qubit_count(code, rank=rank),
        check_schedule_consistency(code),
    ]


def require_valid(code: CodeDefinition) -> None:
    # Raise CodeValidationError if any of checks 1-4 fails.
    failures = [result for result in check_code(code) if not result.passed]
    if failures:
        raise CodeValidationError(
            f"code {code.name!r} failed {len(failures)} of {len(CODE_CHECK_NAMES)} "
            "checks:\n"
            + "\n".join(f"  {result.name}: {result.message}" for result in failures)
        )
