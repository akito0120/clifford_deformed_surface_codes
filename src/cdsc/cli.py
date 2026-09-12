from .codes.registry import build_code
from .codes.builtin import *
from .validation.validate import validate_codes, validation_report
import json
from .config import load_config
import argparse
from pathlib import Path
from typing import Optional, Sequence


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


def _diagrams(args: argparse.Namespace) -> int:
    return EXIT_FAILED


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cdsc",
        description=("Clifford-deformed surface code simulations"),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    validate = subparsers.add_parser(
        "validate",
        help="run the six code health checks",
    )
    validate.add_argument("config", help="path to the YAML config")

    return parser


HANDLERS = {
    "run": _run,
    "validate": _validate,
    "analyze": _analyze,
    "diagrams": _diagrams,
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    handler = HANDLERS.get(args.command)
    if handler is None:
        return EXIT_USAGE_ERROR
    return handler(args)
