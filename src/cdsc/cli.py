from .codes.registry import build_code
from .codes.builtin import *
from .noise.builtin import *
from .validation.validate import validate_codes, validation_report
import json
from .config import Config, load_config
from pydantic import ValidationError
from . import console
import time
import argparse
from pathlib import Path
from typing import Optional, Sequence
from .visualization.diagrams import render_diagrams
from datetime import datetime
import platform
import subprocess
from importlib import metadata
from .sweep.run import build_sweep_plans, sweep
from .visualization.figures import render_all_sweeps, render_all_suppressions
from .analysis.threshold import estimate_all_thresholds
from .analysis.suppression import estimate_all_suppressions

# Exit codes for the cli
EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE_ERROR = 2


class CliError(Exception):
    # A failure reported as one line, without a traceback
    def __init__(self, message: str, exit_code: int):
        super().__init__(message)
        self.exit_code = exit_code


def _load_config(config_path: str) -> Config:
    try:
        return load_config(Path(config_path))
    except (FileNotFoundError, ValidationError) as e:
        raise CliError(console.config_error_message(config_path, e), EXIT_USAGE_ERROR) from e


def _require(path: Path, command: str, config_path: str) -> None:
    # Fail early when an earlier command's output is missing
    if not path.exists():
        raise CliError(console.missing_input_message(path, command, config_path), EXIT_FAILED)


def _write_manifest(config: Config, config_path: str) -> Path:
    now = datetime.now()
    manifest = {
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "packages": installed_packages(),
        },
        "software": {
            "git_commit": commit_hash(),
            "git_dirty": git_dirty(),
        },
        "started_at": str(now),
        "config_path": str(config_path),
        "config": config.as_dict(),
    }

    output_dir = config.output.path
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "manifest.json"
    output_file.write_text(json.dumps(manifest, indent=2) + "\n")
    return output_file


def _run(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    plans = build_sweep_plans(config)
    console.header("run", config, args.config)
    console.run_details(config, commit_hash(), git_dirty(), plans)

    manifest_file = _write_manifest(config, args.config)
    result = sweep(
        config,
        on_plan_start=console.plan_started,
        on_plan_done=console.plan_finished,
    )
    samples_file = config.output.path / "samples.csv"
    result.to_csv(samples_file, index=False)

    console.samples_summary(result, config)
    console.info()
    console.wrote(manifest_file)
    console.wrote(samples_file)

    return EXIT_OK


def _validate(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    distances = [3, 5, 7, 9]
    console.header("validate", config, args.config)

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

    entries = [
        (code_id, code.distance, validation)
        for code, code_id, validation in zip(codes, code_ids, result)
    ]
    console.validation_summary(entries, distances)
    console.wrote(output_file)

    return EXIT_OK if all(validation.passed for validation in result) else EXIT_FAILED


def _analyze(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _require(config.output.path / "samples.csv", "run", args.config)
    console.header("analyze", config, args.config)

    thresholds = estimate_all_thresholds(config)
    threshold_file = config.output.path / "threshold.csv"
    thresholds.to_csv(threshold_file, index=False)

    suppressions = estimate_all_suppressions(config)
    suppression_file = config.output.path / "suppression.csv"
    suppressions.to_csv(suppression_file, index=False)

    console.thresholds(thresholds, config)
    console.suppressions(suppressions, config)
    console.info()
    console.wrote(threshold_file)
    console.wrote(suppression_file)

    return EXIT_OK


def _visualize(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _require(config.output.path / "samples.csv", "run", args.config)
    _require(config.output.path / "threshold.csv", "analyze", args.config)
    _require(config.output.path / "suppression.csv", "analyze", args.config)
    distances = [3, 5, 7]
    console.header("visualize", config, args.config)

    rendered = list()
    for entry in config.codes:
        codes: list[CodeDefinition] = []
        code_ids: list[str] = []
        output_dir = config.output.path / "diagrams" / f"{entry}"
        for distance in distances:
            codes.append(build_code(entry, distance=distance))
            code_ids.append(entry)
        paths = render_diagrams(output_dir, codes, code_ids)
        rendered.append(("diagrams", f"{entry} d={distances}", paths))

    rendered.append(("figures", "threshold", render_all_sweeps(config)))
    rendered.append(("figures", "suppression", render_all_suppressions(config)))
    console.rendered(rendered)

    return EXIT_OK


def _compile_plans(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    output_dir = config.output.path
    console.header("compile-plans", config, args.config)

    plans = build_sweep_plans(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_file = output_dir / "plans.json"
    plan_file.write_text(json.dumps([plan.as_dict() for plan in plans], indent=2))

    console.plan_table(plans, config.sampling)
    console.wrote(plan_file)

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

    compile_plans = subparsers.add_parser("compile-plans", help="Generate sweep plans from the configuration file")
    compile_plans.add_argument("config", help="path to the YAML config")

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


def installed_packages() -> dict[str, str]:
    packages = {}
    for dist in metadata.distributions():
        name = dist.metadata["Name"]
        packages[name] = dist.version
    return dict(sorted(packages.items(), key=lambda item: item[0].lower()))


HANDLERS = {
    "run": _run,
    "validate": _validate,
    "analyze": _analyze,
    "visualize": _visualize,
    "compile-plans": _compile_plans
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    handler = HANDLERS.get(args.command)

    start = time.monotonic()
    try:
        exit_code = handler(args)
    except CliError as e:
        console.error(str(e))
        return e.exit_code
    console.footer(exit_code == EXIT_OK, time.monotonic() - start)
    return exit_code
