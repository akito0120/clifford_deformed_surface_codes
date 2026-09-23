from __future__ import annotations
import numpy as np


def build_p_window(
    center: float,
    half_width: float,
    step: float
) -> list[float]:
    return np.arange(center - half_width, center + half_width + step * 1e-9, step).tolist()


def build_p_linspace(
    start: float,
    stop: float,
    num: int
) -> list[float]:
    return np.linspace(start, stop, num).tolist()
