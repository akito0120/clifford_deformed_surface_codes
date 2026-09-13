from pydantic import BaseModel
from typing import Any
from pathlib import Path
import yaml


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
