from __future__ import annotations
from typing import Callable
from .definition import CodeDefinition

CodeBuilder = Callable[..., CodeDefinition]

_REGISTRY: dict[str, CodeBuilder] = {}


def register_code(name: str) -> Callable[[CodeBuilder], CodeBuilder]:
    # Register a builder under a name, for use as a decorator.
    def decorator(builder: CodeBuilder) -> CodeBuilder:
        if name in _REGISTRY:
            raise ValueError(f"code {name!r} is already registered")
        _REGISTRY[name] = builder
        return builder
    return decorator


def registered_codes() -> list[str]:
    # Names of all registered codes, sorted.
    return sorted(_REGISTRY)


def build_code(name: str, **params) -> CodeDefinition:
    # Build a registered code.
    try:
        builder = _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"unknown code {name!r}; registered codes are {registered_codes()}"
        ) from None
    return builder(**params)
