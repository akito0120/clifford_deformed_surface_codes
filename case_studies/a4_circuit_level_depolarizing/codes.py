from dataclasses import replace

from cdsc.codes.builtin import build_rotated_surface
from cdsc.codes.definition import CodeDefinition
from cdsc.codes.registry import register_code


@register_code("rotated_surface_sd")
def build_rotated_surface_sd(distance: int) -> CodeDefinition:
    # The rotated surface code with one gate-free step before its four CNOT steps.
    # Every qubit idles in that step, which stands in for the first Hadamard layer of the SD circuits in
    # O'Rourke & Devitt (2025). Their second Hadamard layer is folded into the measurement flip (noises.py).
    css = build_rotated_surface(distance)
    schedule = {ancilla: [None, *steps] for ancilla, steps in css.schedule.items()}
    return replace(css.with_schedule(schedule), name=f"rotated_surface_sd_d{distance}")
