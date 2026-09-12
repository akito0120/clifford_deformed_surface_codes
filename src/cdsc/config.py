from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Any, Mapping
import yaml
from pathlib import Path
from .codes.registry import registered_codes


class ConfigError(ValueError):
    pass


# Config data records

@dataclass(frozen=True)
class ExperimentConfig:
    # Identity of the run
    name: str
    seed: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "seed": self.seed}

@dataclass(frozen=True)
class CodeConfig:
    # One code to simulate
    id: str
    builder: str

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "builder": self.builder}

@dataclass(frozen=True)
class OutputConfig:
    dir: str
    figures: bool = False
    diagrams: bool = False

    @property
    def path(self) -> Path:
        return Path(self.dir)

    def as_dict(self) -> dict[str, Any]:
        return {"dir": self.dir, "figures": self.figures, "diagrams": self.diagrams}


@dataclass(frozen=True)
class Config:
    # One experiment configuration
    experiment: ExperimentConfig
    codes: list[CodeConfig]
    output: OutputConfig

    def as_dict(self) -> dict[str, Any]:
        return {
            "experiment": self.experiment.as_dict(),
            "codes": [code.as_dict() for code in self.codes],
            "output": self.output.as_dict(),
        }


# Parsers

def _parse_experiment(document: Mapping[str, Any]) -> ExperimentConfig:
    section = document.get("experiment")
    if not isinstance(section, Mapping):
        raise ConfigError("experiment: expected a mapping")
    return ExperimentConfig(
        name=str(section.get("name", "experiment")),
        seed=int(section.get("seed", 0)),
    )


def _parse_codes(document: Mapping[str, Any]) -> list[CodeConfig]:
    entries = list(document.get("codes"))
    if not entries:
        raise ConfigError("codes: at least one code is required")

    known = registered_codes()
    codes: list[CodeConfig] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            raise ConfigError(f"codes[{index}]: expected a mapping, got {entry!r}")
        code_id = str(entry.get("id"))
        builder = str(entry.get("builder"))
        if builder not in known:
            raise ConfigError(
                f"codes[{code_id}].builder: {builder!r} is not a registered code; "
                f"known: {known}"
            )
        codes.append(CodeConfig(id=code_id, builder=builder))

    duplicates = {c.id for c in codes if [x.id for x in codes].count(c.id) > 1}
    if duplicates:
        raise ConfigError(f"codes: duplicate ids {sorted(duplicates)}")
    return tuple(codes)


def _parse_output(document: Mapping[str, Any]) -> OutputConfig:
    section = document.get("output", {})
    if not isinstance(section, Mapping):
        raise ConfigError("output: expected a mapping")
    return OutputConfig(
        dir=str(section.get("dir", "results")),
        figures=bool(section.get("figures", True)),
        diagrams=bool(section.get("diagrams", False)),
    )


def parse_config(document: Mapping[str, Any]) -> Config:
    return Config(
        experiment=_parse_experiment(document),
        codes=_parse_codes(document),
        output=_parse_output(document),
    )


# Config loader

def load_config(path: str) -> Config:
    path = Path(path)

    try:
        text = path.read_text()
    except OSError as error:
            raise ConfigError(f"cannot read config {str(path)!r}: {error}") from None
    
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise ConfigError(f"{path}: invalid YAML: {error}") from None

    if not isinstance(document, Mapping):
        raise ConfigError(f"{path}: expected a mapping at the top level")

    return parse_config(document)
