from __future__ import annotations
from .definition import CodeDefinition, H, apply_deformation
from .lattice import (
    checkerboard_parity,
    checkerboard_stabilizers,
    default_rotated_schedule,
    rotated_lattice,
)
from .registry import register_code


@register_code("rotated_surface")
def build_rotated_surface(distance: int) -> CodeDefinition:
    # The CSS rotated surface code.
    lattice = rotated_lattice(distance)
    code = checkerboard_stabilizers(lattice)
    schedule = default_rotated_schedule(code)
    return code.with_schedule(schedule)


@register_code("xzzx")
def build_xzzx(distance: int) -> CodeDefinition:
    # The XZZX code: a Hadamard deformation on half the data qubits of the CSS code.
    css = build_rotated_surface(distance)
    deformation = {q: H for q in css.data_qubits if checkerboard_parity(q) == 1}
    return apply_deformation(css, deformation, name=f"xzzx_d{distance}")
