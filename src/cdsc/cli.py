from .codes.registry import build_code
from .codes.builtin import *
from .noise.builtin import *
from .validation.validate import validate_codes, validation_report
import json
from .config import load_config
import argparse
from pathlib import Path
from typing import Optional, Sequence
from .visualization.diagrams import render_diagrams
from datetime import datetime
import platform
import subprocess
from .sweep.run import build_sweep_plans, sweep
from .visualization.figures import render_all_sweeps, render_all_suppressions
from .analysis.threshold import estimate_all_thresholds
from .analysis.suppression import estimate_all_suppressions

# Exit codes for the cli
EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE_ERROR = 2


def _write_manifest(args: argparse.Namespace):
    config = load_config(Path(args.config))
    now = datetime.now()
    manifest = {
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "software": {
            "git_commit": commit_hash(),
            "git_dirty": git_dirty(),
        },
        "started_at": str(now),
        "config_path": str(args.config),
        "config": config.as_dict(),
    }

    output_dir = config.output.path
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "manifest.json"
    output_file.write_text(json.dumps(manifest, indent=2) + "\n")


def _run(args: argparse.Namespace) -> int:
    _write_manifest(args)

    config = load_config(Path(args.config))
    result = sweep(config)
    result.to_csv(f"{config.output.dir}/samples.csv", index=False)

    return EXIT_OK


def _validate(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    distances = [3, 5, 7, 9]

    codes: list[CodeDefinition] = []
    code_ids: list[str] = []
    for entry in config.codes:
        for distance in distances:
                codes.append(build_code(entry, distance=distance))
                code_ids.append(entry)

    result = validate_codes(codes, code_ids=code_ids)
    report = validation_report(result)

    output_dir = config.output.path
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "validation.json"
    output_file.write_text(json.dumps(report, indent=2) + "\n")

    return EXIT_OK


def _analyze(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))

    thresholds = estimate_all_thresholds(config)
    thresholds.to_csv(f"{config.output.dir}/threshold.csv", index=False)

    suppressions = estimate_all_suppressions(config)
    suppressions.to_csv(f"{config.output.dir}/suppression.csv", index=False)

    return EXIT_OK


def _visualize(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    distances = [3, 5, 7]

    for entry in config.codes:
        codes: list[CodeDefinition] = []
        code_ids: list[str] = []
        output_dir = config.output.path / "diagrams" / f"{entry}"
        for distance in distances:
            codes.append(build_code(entry, distance=distance))
            code_ids.append(entry)
        render_diagrams(output_dir, codes, code_ids)

    render_all_sweeps(config)
    render_all_suppressions(config)
        
    return EXIT_OK


def _see_plans(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    output_dir = config.output.path

    plans = build_sweep_plans(config)
    plan_file = output_dir / "plans.json"
    plan_file.write_text(json.dumps([plan.as_dict() for plan in plans], indent=2))

    return EXIT_OK
    

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cdsc",
        description=("Clifford-deformed surface code simulations"),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    run = subparsers.add_parser("run", help="Build circuits, sample, and decode")
    run.add_argument("config", help="path to the YAML config")

    validate = subparsers.add_parser("validate", help="Run checks on codes and circuits")
    validate.add_argument("config", help="path to the YAML config")

    analyze = subparsers.add_parser("analyze", help="Estimate the theshold, suppression factor and teraquop footpring")
    analyze.add_argument("config", help="path to the YAML config")

    visualize = subparsers.add_parser("visualize", help="Visualize the analysis result and circuit diagrams")
    visualize.add_argument("config", help="path to the YAML config")

    see_plans = subparsers.add_parser("see-plans", help="Generate sweep plans from the configuration file")
    see_plans.add_argument("config", help="path to the YAML config")

    return parser


def commit_hash() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def git_dirty() -> bool:
    return subprocess.run(
        ["git", "diff", "--quiet"],
    ).returncode != 0


HANDLERS = {
    "run": _run,
    "validate": _validate,
    "analyze": _analyze,
    "visualize": _visualize,
    "see-plans": _see_plans
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    handler = HANDLERS.get(args.command)
    if handler is None:
        return EXIT_USAGE_ERROR
    return handler(args)
