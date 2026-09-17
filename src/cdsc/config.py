from pydantic import BaseModel
from typing import Any
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


class PointsConfig(BaseModel):
    mode: str

    # For window mode
    center: float
    half_width: float
    step: float

    # For linspace mode
    start: float
    stop: float
    num: float

    # For list mode
    values: list[float]

    def as_dict(self) -> dict[str, Any]:
        if self.mode == WINDOW_MODE:
            return {
                "mode": self.mode,
                "center": self.center,
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
    output: OutputConfig

    def as_dict(self) -> dict[str, Any]:
        return {
            "experiment": self.experiment.as_dict(),
            "codes": [code.as_dict() for code in self.codes],
            "output": self.output.as_dict(),
        }


def load_config(path: Path) -> Config:
    text = path.read_text()
    document = yaml.safe_load(text)
    return Config.model_validate(document)
