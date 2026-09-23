from .noise import Noise
from typing import Callable, Any


NoiseBuilder = Callable[[float, dict[str, Any]], Noise]


_NOISE_REGISTRY: dict[str, NoiseBuilder] = {}


def register_noise(name: str) -> Callable[[NoiseBuilder], NoiseBuilder]:
    # Register a builder under a name, for use as a decorator.
    def decorator(builder: NoiseBuilder) -> NoiseBuilder:
        if name in _NOISE_REGISTRY:
            raise ValueError(f"noise {name!r} is already registered")
        _NOISE_REGISTRY[name] = builder
        return builder
    return decorator


def registered_noises() -> list[str]:
    # Names of all registered codes, sorted.
    return sorted(_NOISE_REGISTRY)


def build_noise(name: str, p: float, params: dict[str, Any]) -> Noise:
    try:
        builder = _NOISE_REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"unknown noise {name!r}; registered noises are {registered_noises()}"
        ) from None
    return builder(p, params)
