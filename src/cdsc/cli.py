from .codes.registry import build_code
from .codes.builtin import *
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


# Exit codes for the cli
EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE_ERROR = 2


def _run(args: argparse.Namespace) -> int:
    return EXIT_FAILED


def _validate(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    distances = [3, 5, 7, 9]

    codes: list[CodeDefinition] = []
    code_ids: list[str] = []
    for entry in config.codes:
        for distance in distances:
                codes.append(build_code(entry.builder, distance=distance))
                code_ids.append(entry.id)

    result = validate_codes(codes, code_ids=code_ids)
    report = validation_report(result)

    output_dir = Path(config.output.dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "validation.json"
    output_file.write_text(json.dumps(report, indent=2) + "\n")

    return EXIT_OK


def _analyze(args: argparse.Namespace) -> int:
    return EXIT_FAILED


def _visualize(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    distances = [3, 5, 7]

    for entry in config.codes:
        codes: list[CodeDefinition] = []
        code_ids: list[str] = []
        output_dir = Path(config.output.dir) / "diagrams" / f"{entry.id}"
        for distance in distances:
            codes.append(build_code(entry.builder, distance=distance))
            code_ids.append(entry.id)
        render_diagrams(output_dir, codes, code_ids)
        
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

    return parser


def commit_hash() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def _write_manifest(args: argparse.Namespace):
    config = load_config(args.config)
    now = datetime.now()
    manifest = {
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "git_commit": commit_hash(),
        "started_at": str(now),
        "config_path": str(args.config),
        "config": config.as_dict(),
    }

    output_dir = Path(config.output.dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "manifest.json"
    output_file.write_text(json.dumps(manifest, indent=2) + "\n")


HANDLERS = {
    "run": _run,
    "validate": _validate,
    "analyze": _analyze,
    "visualize": _visualize,
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    _write_manifest(args)

    handler = HANDLERS.get(args.command)
    if handler is None:
        return EXIT_USAGE_ERROR
    return handler(args)
