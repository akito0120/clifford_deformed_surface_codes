# Convert ORourke2025's released statistics (SD_stats.pickle of wamud/compare_the_pair, a list of sinter.TaskStats)　to the framework's samples.csv format.

# Usage:
# python case_studies/a4_circuit_level_depolarizing/convert_orourke2025.py [config.yaml] [--pickle SD_stats.pickle] [--out-dir DIR]
# Writes orourke2025_samples.csv to <output.dir> unless --out-dir is given.

import argparse
import collections
import pickle
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import sinter

from cdsc.config import Config, ConfigError, load_config
from cdsc.sweep.run import sample_row

HERE = Path(__file__).resolve().parent

# ORourke2025's tasks for the rotated code under SD noise, with their CNOT order and idling errors
PAPER_TASKS = {"ro": "ro", "noise": "SD", "o": 10231203, "idl": "y"}
PAPER_SWEEP_ID = "orourke2025"
SAMPLE_COLUMNS = ["d", "rounds", "p", "sweep_id", "code", "basis", "noise_model", "noise_definition", "pl", "sigma", "errors", "shots"]


class _TaskStatsRecord:
    # Stands in for sinter.TaskStats while unpickling: it only receives the pickled fields
    def __setstate__(self, state: Any) -> None:
        if isinstance(state, tuple):  # (dict, slots)
            state = {**(state[0] or {}), **(state[1] or {})}
        self.__dict__.update(state)


class _RestrictedUnpickler(pickle.Unpickler):
    # Unpickling can run any code the file names: allow only the two classes a sinter stats pickle needs
    ALLOWED = {
        ("sinter._task_stats", "TaskStats"): _TaskStatsRecord,
        ("collections", "Counter"): collections.Counter,
    }

    def find_class(self, module: str, name: str) -> Any:
        try:
            return self.ALLOWED[(module, name)]
        except KeyError:
            raise pickle.UnpicklingError(f"refusing to load {module}.{name}") from None


def load_paper_stats(path: Path) -> list[dict[str, Any]]:
    with path.open("rb") as f:
        try:
            records = _RestrictedUnpickler(f).load()
        except (pickle.UnpicklingError, EOFError, TypeError, AttributeError) as e:
            raise ValueError(f"{path}: not a pickle of sinter.TaskStats ({type(e).__name__}: {e})") from e
    if not isinstance(records, list) or not all(isinstance(r, _TaskStatsRecord) for r in records):
        raise ValueError(f"{path}: expected a list of sinter.TaskStats")
    return [r.__dict__ for r in records]


def rounds_multiple(rounds: str) -> int:
    # The paper's "r" metadata: "3d" -> 3, "d" -> 1
    head = rounds.removesuffix("d")
    return int(head) if head else 1


def paper_samples(stats: list[dict[str, Any]], config: Config, bases: list[str]) -> pd.DataFrame:
    # ORourke2025's tasks as rows of the framework's samples.csv, labelled with the config's code and noise
    rows = []
    for s in stats:
        meta = s["json_metadata"]
        if any(meta.get(key) != value for key, value in PAPER_TASKS.items()):
            continue
        basis = meta["b"].upper()
        if basis not in bases:
            continue
        d = meta["d"]
        stat = sinter.TaskStats(
            strong_id=s["strong_id"],
            decoder=s["decoder"],
            json_metadata={
                "d": d,
                "rounds": rounds_multiple(meta["r"]) * d,
                "p": meta["p"],
                "sweep_id": PAPER_SWEEP_ID,
                "code": config.codes[0],
                "basis": basis,
                "noise_model": config.noise.model,
                "noise_definition": config.noise.definition,
            },
            shots=s["shots"],
            errors=s["errors"],
            discards=s["discards"],
            seconds=s["seconds"],
        )
        rows.append(sample_row(stat))
    if not rows:
        raise ValueError(f"no tasks in the pickle match {PAPER_TASKS} and bases {bases}")
    return pd.DataFrame(rows, columns=SAMPLE_COLUMNS).sort_values(["basis", "p", "d"], ignore_index=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert ORourke2025's SD_stats.pickle to the framework's samples.csv format.")
    parser.add_argument("config", nargs="?", default=str(HERE / "config.yaml"), help="A4's config (default: config.yaml)")
    parser.add_argument("--pickle", default=str(HERE / "SD_stats.pickle"),
                        help="ORourke2025's SD_stats.pickle (default: next to this script)")
    parser.add_argument("--out-dir", help="output directory (default: the config's output dir)")
    args = parser.parse_args()

    try:
        config = load_config(Path(args.config))
        if len(config.codes) != 1:
            raise ValueError("the config must have one code, the label for ORourke2025's rotated code")
        sweep = next(s for s in config.sweeps if s.id == config.threshold.source_sweep)
        paper = paper_samples(load_paper_stats(Path(args.pickle)), config, list(sweep.basis))
    except (ConfigError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir) if args.out_dir else config.output.path
    out_dir.mkdir(parents=True, exist_ok=True)
    paper.to_csv(out_dir / "orourke2025_samples.csv", index=False)
    print(f"wrote {out_dir / 'orourke2025_samples.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
