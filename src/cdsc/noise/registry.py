from .noise import Noise
from typing import Callable, Any


NoiseBuilder = Callable[[float, dict[str, Any]], Noise]


_NOISE_REGISTRY: dict[str, NoiseBuilder] = {}
_REQUIRED_PARAMS: dict[str, tuple[str, ...]] = {}


def register_noise(
    name: str, required_params: tuple[str, ...] = ()
) -> Callable[[NoiseBuilder], NoiseBuilder]:
    # Register a builder under a name, for use as a decorator.
    # required_params: the noise.params keys the builder reads
    def decorator(builder: NoiseBuilder) -> NoiseBuilder:
        if name in _NOISE_REGISTRY:
            raise ValueError(f"noise {name!r} is already registered")
        _NOISE_REGISTRY[name] = builder
        _REQUIRED_PARAMS[name] = tuple(required_params)
        return builder
    return decorator


def required_params(name: str) -> tuple[str, ...]:
    # The noise.params keys a registered noise needs.
    return _REQUIRED_PARAMS.get(name, ())


def registered_noises() -> list[str]:
    # Names of all registered noises, sorted.
    return sorted(_NOISE_REGISTRY)


def build_noise(name: str, p: float, params: dict[str, Any]) -> Noise:
    try:
        builder = _NOISE_REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"unknown noise {name!r}; registered noises are {registered_noises()}"
        ) from None
    return builder(p, params)
