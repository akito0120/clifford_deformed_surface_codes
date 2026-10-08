from cdsc.codes.builtin import build_rotated_surface
from cdsc.codes.definition import CodeDefinition, H, apply_deformation
from cdsc.codes.lattice import checkerboard_parity
from cdsc.codes.registry import register_code


@register_code("half_xzzx")
def build_half_xzzx(distance: int) -> CodeDefinition:
    # The XZZX deformation applied only to the data qubit columns left of the middle one
    css = build_rotated_surface(distance)
    deformation = {
        q: H for q in css.data_qubits
        if checkerboard_parity(q) == 1 and q[0] < distance
    }
    return apply_deformation(css, deformation, name=f"half_xzzx_d{distance}")
