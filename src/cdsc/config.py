from pydantic import AfterValidator, BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator
from typing import Annotated, Any, Literal
from pathlib import Path
from math import prod
import yaml


WINDOW_MODE = "window"
LINSPACE_MODE = "linspace"
LIST_MODE = "list"

SAME_AS_P = "same_as_p"


class ConfigError(Exception):
    # A config that cannot be used, with every problem found in it
    def __init__(self, path: Path, problems: list[tuple[str, str]], readable: bool = True):
        super().__init__(f"invalid config {path}")
        self.path = path
        self.problems = problems    # (location, reason)
        self.readable = readable    # False when the file itself could not be read


class _Model(BaseModel):
    # Unknown keys are errors, so a typo in the config is not silently ignored
    model_config = ConfigDict(extra="forbid")


def _check_distances(distances: list[int]) -> list[int]:
    bad = [d for d in distances if d < 3 or d % 2 == 0]
    if bad:
        raise ValueError(f"distances must be odd and at least 3, got {bad}")
    return distances


Distances = Annotated[list[int], Field(min_length=1), AfterValidator(_check_distances)]


def _check_probabilities(name: str, values: list[float]) -> list[str]:
    bad = [v for v in values if not 0 < v < 1]
    if not bad:
        return []
    return [f"{name} must be between 0 and 1 (exclusive), got [{', '.join(f'{v:g}' for v in bad)}]"]


class ExperimentConfig(_Model):
    # Identity of the run
    name: str = Field(min_length=1)
    seed: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "seed": self.seed}


class NoiseConfig(_Model):
    model: Literal["code_capacity", "phenomenological", "circuit_level"]
    definition: str
    params: dict[str, list[Any]] | None = None
    p_meas: str | float

    @field_validator("definition")
    @classmethod
    def _registered(cls, name: str) -> str:
        from .noise import builtin  # Register built-in noises
        from .noise.registry import registered_noises
        if name not in registered_noises():
            raise ValueError(f"unknown noise definition {name!r}; registered: {registered_noises()}")
        return name

    @field_validator("params")
    @classmethod
    def _non_empty_values(cls, params: dict[str, list[Any]] | None) -> dict[str, list[Any]] | None:
        empty = [key for key, values in (params or {}).items() if not values]
        if empty:
            raise ValueError(f"each parameter needs at least one value; empty: {empty}")
        return params

    @field_validator("p_meas")
    @classmethod
    def _p_meas(cls, p_meas: str | float) -> str | float:
        if p_meas == SAME_AS_P or (not isinstance(p_meas, str) and 0 <= p_meas <= 1):
            return p_meas
        raise ValueError(f"p_meas must be {SAME_AS_P!r} or a number between 0 and 1, got {p_meas!r}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "definition": self.definition,
            "params": self.params,
            "p_meas": self.p_meas
        }


class PointsConfig(_Model):
    mode: Literal["window", "linspace", "list"]

    # For window mode
    centers: list[float] | None = None
    half_width: float | None = None
    step: float | None = None

    # For linspace mode
    start: float | None = None
    stop: float | None = None
    num: int | None = None

    # For list mode
    values: list[float] | None = None

    @model_validator(mode="after")
    def _keys_for_mode(self) -> "PointsConfig":
        keys_by_mode = {
            WINDOW_MODE: ("centers", "half_width", "step"),
            LINSPACE_MODE: ("start", "stop", "num"),
            LIST_MODE: ("values",),
        }
        problems = []
        for mode, keys in keys_by_mode.items():
            for key in keys:
                given = getattr(self, key) is not None
                if mode == self.mode and not given:
                    problems.append(f"{self.mode} mode requires {key!r}")
                elif mode != self.mode and given:
                    problems.append(f"{key!r} is not used in {self.mode} mode")
        if not problems:
            problems = self._range_problems()
        if problems:
            raise ValueError("; ".join(problems))
        return self

    def _range_problems(self) -> list[str]:
        if self.mode == WINDOW_MODE:
            problems = []
            if not self.centers:
                problems.append("centers must not be empty")
            if self.half_width < 0:
                problems.append(f"half_width must be >= 0, got {self.half_width}")
            if self.step <= 0:
                problems.append(f"step must be > 0, got {self.step}")
            edges = [c - self.half_width for c in self.centers] + [c + self.half_width for c in self.centers]
            return problems + _check_probabilities("window points (center ± half_width)", edges)
        if self.mode == LINSPACE_MODE:
            problems = [] if self.num >= 1 else [f"num must be >= 1, got {self.num}"]
            return problems + _check_probabilities("start and stop", [self.start, self.stop])
        if not self.values:
            return ["values must not be empty"]
        return _check_probabilities("values", self.values)

    def as_dict(self) -> dict[str, Any]:
        if self.mode == WINDOW_MODE:
            return {
                "mode": self.mode,
                "centers": self.centers,
                "half_width": self.half_width,
                "step": self.step
            }
        elif self.mode == LINSPACE_MODE:
            return {
                "mode": self.mode,
                "start": self.start,
                "stop": self.stop,
                "num": self.num
            }
        elif self.mode == LIST_MODE:
            return {
                "mode": self.mode,
                "values": self.values
            }
        return None


class SweepConfig(_Model):
    id: str = Field(min_length=1)
    distances: Distances
    basis: list[Literal["X", "Z"]] = Field(min_length=1)
    p: PointsConfig

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "distances": self.distances,
            "basis": self.basis,
            "p": self.p.as_dict()
        }


class SamplingConfig(_Model):
    decoder: Literal["mwpm", "uf", "bp"]
    max_shots: int = Field(gt=0)
    max_errors: int = Field(gt=0)
    max_batch_size: int = Field(gt=0)
    workers: int = Field(gt=0)

    def as_dict(self) -> dict[str, Any]:
        return {
            "decoder": self.decoder,
            "max_shots": self.max_shots,
            "max_errors": self.max_errors,
            "max_batch_size": self.max_batch_size,
            "workers": self.workers
        }


class ThresholdConfig(_Model):
    source_sweep: str
    distances: Distances
    x_window: float = Field(gt=0)
    nu_0: float = Field(ge=1, le=2)    # the fit bounds nu to [1, 2]

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_sweep": self.source_sweep,
            "distances": self.distances,
            "x_window": self.x_window,
            "nu_0": self.nu_0
        }


class SuppressionConfig(_Model):
    source_sweep: str
    target_pl: float = Field(gt=0, lt=1)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_sweep": self.source_sweep,
            "target_pl": self.target_pl
        }


class OutputConfig(_Model):
    dir: str = Field(min_length=1)

    @property
    def path(self) -> Path:
        return Path(self.dir)

    def as_dict(self) -> dict[str, Any]:
        return {"dir": self.dir}


class Config(_Model):
    # One experiment configuration
    experiment: ExperimentConfig
    codes: list[str] = Field(min_length=1)
    noise: NoiseConfig
    sweeps: list[SweepConfig] = Field(min_length=1)
    sampling: SamplingConfig
    threshold: ThresholdConfig
    suppression: SuppressionConfig
    output: OutputConfig

    @field_validator("codes")
    @classmethod
    def _registered(cls, codes: list[str]) -> list[str]:
        from .codes import builtin  # Register built-in codes
        from .codes.registry import registered_codes
        unknown = [code for code in codes if code not in registered_codes()]
        if unknown:
            raise ValueError(f"unknown codes {unknown}; registered: {registered_codes()}")
        duplicated = sorted({code for code in codes if codes.count(code) > 1})
        if duplicated:
            raise ValueError(f"codes are listed more than once: {duplicated}")
        return codes

    def as_dict(self) -> dict[str, Any]:
        return {
            "experiment": self.experiment.as_dict(),
            "codes": list(self.codes),
            "noise": self.noise.as_dict(),
            "sweeps": [sweep.as_dict() for sweep in self.sweeps],
            "sampling": self.sampling.as_dict(),
            "threshold": self.threshold.as_dict(),
            "suppression": self.suppression.as_dict(),
            "output": self.output.as_dict(),
        }


def check_references(config: Config) -> list[tuple[str, str]]:
    # Checks across sections; empty when the config is consistent
    from .noise.registry import required_params

    problems = []
    sweeps = {sweep.id: sweep for sweep in config.sweeps}

    # Sweep ids duplicated
    ids = [sweep.id for sweep in config.sweeps]
    duplicated = sorted({sweep_id for sweep_id in ids if ids.count(sweep_id) > 1})
    if duplicated:
        problems.append(("sweeps", f"sweep ids are used more than once: {duplicated}"))

    # Sweep source does not exist
    for section in ("threshold", "suppression"):
        source = getattr(config, section).source_sweep
        if source not in sweeps:
            problems.append((f"{section}.source_sweep", f"no sweep has id {source!r}; sweep ids: {ids}"))

    # Threshold distances not sampled
    source = sweeps.get(config.threshold.source_sweep)
    if source is not None:
        missing = [d for d in config.threshold.distances if d not in source.distances]
        if missing:
            problems.append((
                "threshold.distances",
                f"{missing} are not sampled by sweep {source.id!r} (distances: {source.distances})"
            ))

    # One center for one parameter combination
    params = config.noise.params or {}
    combinations = len(config.codes) * prod(len(values) for values in params.values())
    for index, sweep in enumerate(config.sweeps):
        if sweep.p.mode != WINDOW_MODE:
            continue
        expected = combinations * len(sweep.basis)
        if len(sweep.p.centers) != expected:
            problems.append((
                f"sweeps[{index}].p.centers",
                f"got {len(sweep.p.centers)} centers, but there are {expected} combinations "
                "of codes x basis x noise params; give one center per combination"
            ))

    # Missing noise params
    missing = [key for key in required_params(config.noise.definition) if key not in params]
    if missing:
        problems.append((
            "noise.params",
            f"noise {config.noise.definition!r} requires parameters {missing}"
        ))

    return problems


class _UniqueKeyLoader(yaml.SafeLoader):
    # SafeLoader that rejects duplicate keys instead of keeping the last one
    def construct_mapping(self, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in seen
            except TypeError:
                continue # unhashable key: SafeLoader reports it
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found duplicate key {key!r}", key_node.start_mark,
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _location(loc: tuple) -> str:
    # Format the validation error location
    # e.g. ("sweeps", 0, "p", "mode") -> "sweeps[0].p.mode"
    text = ""
    for item in loc:
        if isinstance(item, int):
            text += f"[{item}]"
        else:
            text += f".{item}" if text else str(item)
    return text or "(root)"


def _problem(error: dict[str, Any]) -> tuple[str, str]:
    kind = error["type"]
    if kind == "extra_forbidden":
        reason = "unknown key"
    elif kind == "missing":
        reason = "required key is missing"
    elif kind == "value_error":
        reason = str(error["ctx"]["error"])
    else:
        reason = error["msg"]
        value = error.get("input")
        if isinstance(value, (str, int, float, bool)):
            reason += f" (got {value!r})"
    return _location(error["loc"]), reason


def load_config(path: Path) -> Config:
    # Read file
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ConfigError(path, [("", e.strerror or str(e))], readable=False) from e
    except UnicodeDecodeError as e:
        raise ConfigError(path, [("", "not a UTF-8 text file")], readable=False) from e

    # Load and validate YAML syntax
    try:
        document = yaml.load(text, Loader=_UniqueKeyLoader)
    except yaml.MarkedYAMLError as e:
        mark = e.problem_mark or e.context_mark
        location = f"line {mark.line + 1}, column {mark.column + 1}" if mark else "(yaml)"
        reason = e.problem or "invalid YAML"
        if e.context:
            reason += f" ({e.context})"
        raise ConfigError(path, [(location, reason)]) from e
    except yaml.YAMLError as e:
        raise ConfigError(path, [("(yaml)", str(e))]) from e

    if document is None:
        raise ConfigError(path, [("(root)", "file is empty")])
    if not isinstance(document, dict):
        raise ConfigError(path, [(
            "(root)",
            f"top level must be a mapping of sections (experiment, codes, ...), got {type(document).__name__}"
        )])

    # Config schema validation
    try:
        config = Config.model_validate(document)
    except ValidationError as e:
        raise ConfigError(path, [_problem(error) for error in e.errors()]) from e

    problems = check_references(config)
    if problems:
        raise ConfigError(path, problems)
    return config
