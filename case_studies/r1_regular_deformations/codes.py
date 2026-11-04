from itertools import product

from cdsc.codes.builtin import build_rotated_surface
from cdsc.codes.definition import H, SQRT_X, CodeDefinition, apply_deformation
from cdsc.codes.registry import register_code

# Regular Clifford deformations of the rotated surface code (case study R1).
# Each data qubit, at column c and row r, gets I, H or V (SQRT_X) from a periodic pattern.
# Under Z-biased noise with p_X = p_Y these three labels give every distinct deformation:
# they turn a Z error into a Z, X or Y error on the CSS code.
CLIFFORDS = {"I": None, "H": H, "V": SQRT_X}

# Pattern families: name prefix, number of labels, and the label index of data qubit (c, r)
FAMILIES = [
    ("cell", 4, lambda c, r: 2 * (r % 2) + c % 2),  # 2x2 unit cell, named by its rows: cell_ab_cd
    ("row3", 3, lambda c, r: c % 3),  # period 3 along each row
    ("col3", 3, lambda c, r: r % 3),  # period 3 along each column
    ("diag3", 3, lambda c, r: (r + c) % 3),
    ("anti3", 3, lambda c, r: (r - c) % 3),
    ("diag4", 4, lambda c, r: (r + c) % 4),
]

# Patterns equal to a built-in code are left to the built-in: all I (rotated_surface),
# the checkerboard of xzzx (H where c + r is odd) and all V (xy)
BUILTIN_PATTERNS = [lambda c, r: "I", lambda c, r: "IH"[(c + r) % 2], lambda c, r: "V"]

# Every period divides 12, so two patterns agree everywhere if they agree on a 12x12 patch
PATCH = 12


def _patch(label_of) -> tuple[str, ...]:
    return tuple(label_of(c, r) for r in range(PATCH) for c in range(PATCH))


def _register(name: str, label_of) -> None:
    @register_code(name)
    def build(distance: int) -> CodeDefinition:
        css = build_rotated_surface(distance)
        deformation = {}
        for q in css.data_qubits:
            clifford = CLIFFORDS[label_of((q[0] - 1) // 2, (q[1] - 1) // 2)]
            if clifford is not None:
                deformation[q] = clifford
        return apply_deformation(css, deformation, name=f"{name}_d{distance}")


def _register_all() -> None:
    # Register every pattern of every family once, in a fixed order; the first name of a pattern wins
    seen = {_patch(label_of) for label_of in BUILTIN_PATTERNS}
    for prefix, size, index_of in FAMILIES:
        for labels in product("IHV", repeat=size):
            label_of = lambda c, r, labels=labels, index_of=index_of: labels[index_of(c, r)]
            patch = _patch(label_of)
            if patch in seen:
                continue
            seen.add(patch)
            text = "".join(labels)
            _register(f"cell_{text[:2]}_{text[2:]}" if prefix == "cell" else f"{prefix}_{text}", label_of)


_register_all()
