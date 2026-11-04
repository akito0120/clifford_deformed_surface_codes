from .codes.registry import build_code
from .codes.builtin import *
from .noise.builtin import *
from .validation.validate import validate_codes, validation_report
import json
from .config import Config, ConfigError, load_config
from . import console
import time
import argparse
import hashlib
from pathlib import Path
from typing import Any, Optional, Sequence
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
    except ConfigError as e:
        raise CliError(console.config_error_message(e), EXIT_USAGE_ERROR) from e


def _require(path: Path, command: str, config_path: str) -> None:
    # Fail early when an earlier command's output is missing
    if not path.exists():
        raise CliError(console.missing_input_message(path, command, config_path), EXIT_FAILED)


def _manifest(config: Config, config_path: str) -> dict[str, Any]:
    # The environment, software and config as they are when sampling starts
    # finished_at is set when it ends
    return {
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "packages": installed_packages(),
        },
        "software": {
            "git_commit": commit_hash(),
            "git_dirty": git_dirty(),
            "plugins": {
                entry: hashlib.sha256(Path(entry).read_bytes()).hexdigest()
                for entry in config.plugins
            },
        },
        "started_at": str(datetime.now()),
        "finished_at": None,
        "config_path": str(config_path),
        "config": config.as_dict(),
    }


def _write_manifest(config: Config, manifest: dict[str, Any]) -> Path:
    output_file = config.output.path / "manifest.json"
    output_file.write_text(json.dumps(manifest, indent=2) + "\n")
    return output_file


def _run(config: Config, args: argparse.Namespace) -> int:
    plans = build_sweep_plans(config)
    console.header("run", config, args.config)
    console.run_details(config, commit_hash(), git_dirty(), plans)

    # Create the output directory before sampling, so that a bad path fails before the sweep
    config.output.path.mkdir(parents=True, exist_ok=True)

    manifest = _manifest(config, args.config)
    result = sweep(
        config,
        on_plan_start=console.plan_started,
        on_plan_done=console.plan_finished,
    )
    manifest["finished_at"] = str(datetime.now())

    samples_file = config.output.path / "samples.csv"
    result.to_csv(samples_file, index=False)
    manifest_file = _write_manifest(config, manifest)

    console.samples_summary(result, config)
    console.info()
    console.wrote(manifest_file)
    console.wrote(samples_file)

    return EXIT_OK


def _validate(config: Config, args: argparse.Namespace) -> int:
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


def _analyze(config: Config, args: argparse.Namespace) -> int:
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


def _visualize(config: Config, args: argparse.Namespace) -> int:
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


def _compile_plans(config: Config, args: argparse.Namespace) -> int:
    output_dir = config.output.path
    console.header("compile-plans", config, args.config)

    plans = build_sweep_plans(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_file = output_dir / "plans.json"
    plan_file.write_text(json.dumps([plan.as_dict() for plan in plans], indent=2))

    console.plan_table(plans, config.sampling)
    console.wrote(plan_file)

    return EXIT_OK


# The steps of run-all, in order: each one reads what the ones before it wrote
RUN_ALL_STEPS: tuple[str, ...] = ("validate", "compile-plans", "run", "analyze", "visualize")


def _run_all(config: Config, args: argparse.Namespace) -> int:
    # Every step gets the same loaded config
    # Stop at the first step that fails
    for index, step in enumerate(RUN_ALL_STEPS):
        if index > 0:
            console.info()
        exit_code = HANDLERS[step](config, args)
        if exit_code != EXIT_OK:
            console.error(console.run_all_stopped_message(step, RUN_ALL_STEPS[index + 1:]))
            return exit_code
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

    analyze = subparsers.add_parser("analyze", help="Estimate the threshold and teraquop footprint")
    analyze.add_argument("config", help="path to the YAML config")

    visualize = subparsers.add_parser("visualize", help="Visualize the analysis result and circuit diagrams")
    visualize.add_argument("config", help="path to the YAML config")

    compile_plans = subparsers.add_parser("compile-plans", help="Generate sweep plans from the configuration file")
    compile_plans.add_argument("config", help="path to the YAML config")

    run_all = subparsers.add_parser("run-all", help="Run the entire simulation pipeline, stopping at the first failure")
    run_all.add_argument("config", help="path to the YAML config")

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
    "compile-plans": _compile_plans,
    "run-all": _run_all,
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    handler = HANDLERS.get(args.command)

    start = time.monotonic()
    try:
        config = _load_config(args.config)
        exit_code = handler(config, args)
    except CliError as e:
        console.error(str(e))
        return e.exit_code
    console.footer(exit_code == EXIT_OK, time.monotonic() - start)
    return exit_code
