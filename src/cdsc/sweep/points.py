from __future__ import annotations
from ..config import PointsConfig, WINDOW_MODE, LINSPACE_MODE, LIST_MODE
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
    num: float
) -> list[float]:
    np.linspace(start, stop, num)


def physical_error_rates(config: PointsConfig) -> list[float]:
    if config.mode == WINDOW_MODE:
        return build_p_window(config.center, config.half_width, config.step)
    elif config.mode == LINSPACE_MODE:
        return build_p_linspace(config.start, config.stop, config.num)
    elif config.mode == LIST_MODE:
        return config.values
    raise ValueError("invalida mode is specified")
