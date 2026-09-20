from pydantic import BaseModel
from typing import Any, Literal
from pathlib import Path
import yaml


WINDOW_MODE = "window"
LINSPACE_MODE = "linspace"
LIST_MODE = "list"


class ExperimentConfig(BaseModel):
    # Identity of the run
    name: str
    seed: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "seed": self.seed}


class CodeConfig(BaseModel):
    # One code to simulate
    id: str
    builder: str

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "builder": self.builder}


class NoiseConfig(BaseModel):
    model: Literal["code_capacity", "phenomenological", "circuit_level"]
    definition: str
    params: dict[str, list[Any]] | None = None
    p_meas: str | float

    def as_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "definition": self.definition,
            "params": self.params,
            "p_meas": self.p_meas
        }


class PointsConfig(BaseModel):
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


class SweepConfig(BaseModel):
    id: str
    distances: list[int]
    basis: list[Literal["X", "Z"]]
    p: PointsConfig

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "distances": self.distances,
            "basis": self.basis,
            "p": self.p.as_dict()
        }


class SamplingConfig(BaseModel):
    decoder: Literal["mwpm", "uf", "bp"]
    max_shots: int
    max_errors: int
    max_batch_size: int
    workers: str | int

    def as_dict(self) -> dict[str, Any]:
        return {
            "decoder": self.decoder,
            "max_shots": self.max_shots,
            "max_errors": self.max_errors,
            "max_batch_size": self.max_batch_size,
            "workers": self.workers
        }


class OutputConfig(BaseModel):
    dir: str
    figures: bool = False
    diagrams: bool = False

    @property
    def path(self) -> Path:
        return Path(self.dir)

    def as_dict(self) -> dict[str, Any]:
        return {"dir": self.dir, "figures": self.figures, "diagrams": self.diagrams}


class Config(BaseModel):
    # One experiment configuration
    experiment: ExperimentConfig
    codes: list[CodeConfig]
    noise: NoiseConfig
    sweeps: list[SweepConfig]
    sampling: SamplingConfig
    output: OutputConfig

    def as_dict(self) -> dict[str, Any]:
        return {
            "experiment": self.experiment.as_dict(),
            "codes": [code.as_dict() for code in self.codes],
            "noise": self.noise.as_dict(),
            "sweeps": [sweep.as_dict() for sweep in self.sweeps],
            "sampling": self.sampling.as_dict(),
            "output": self.output.as_dict(),
        }


def load_config(path: Path) -> Config:
    text = path.read_text()
    document = yaml.safe_load(text)
    return Config.model_validate(document)
