# Sample stim's generated rotated surface code circuits under phenomenological depolarizing noise.

# Usage:
# python case_study/a3_phenomenological_vs_stim/sample_stim.py <config_stim.yaml> [--reference <config_framework.yaml>]

import argparse
import json
import platform
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import sinter
import stim

from cdsc import console
from cdsc.cli import commit_hash, git_dirty, installed_packages
from cdsc.config import SAME_AS_P, Config, ConfigError, load_config
from cdsc.decoder import resolve_decoder
from cdsc.sweep.run import SweepPlan, build_sweep_plans, sample_row


# The only settings stim.Circuit.generated can reproduce exactly
SUPPORTED = {
    "noise.model": "phenomenological",
    "noise.definition": "depolarizing",
    "codes": ["rotated_surface"],
}

# How the framework's phenomenological model maps onto stim.Circuit.generated
CIRCUIT_SOURCE = {
    "generator": "stim.Circuit.generated",
    "code_task": "surface_code:rotated_memory_x / surface_code:rotated_memory_z (by basis)",
    "rounds": "d",
    "before_round_data_depolarization": "p",
    "before_measure_flip_probability": "p_meas",
    "after_clifford_depolarization": 0.0,
    "after_reset_flip_probability": 0.0,
}

# Sections that may differ between the stim config and the framework config
IGNORED_SECTIONS = ("experiment", "output")


def unsupported(config: Config) -> list[str]:
    # Settings the stim generator cannot match; empty when the config is supported
    actual = {
        "noise.model": config.noise.model,
        "noise.definition": config.noise.definition,
        "codes": list(config.codes),
    }
    problems = [
        f"{key} must be {expected!r}, got {actual[key]!r}"
        for key, expected in SUPPORTED.items()
        if actual[key] != expected
    ]
    if config.noise.params:
        problems.append(f"noise.params must be empty, got {config.noise.params!r}")
    return problems


def mismatches(config: Config, reference: Config) -> list[str]:
    # Sections that differ from the reference config, apart from IGNORED_SECTIONS
    ours, theirs = config.as_dict(), reference.as_dict()
    return [
        section for section in ours
        if section not in IGNORED_SECTIONS and ours[section] != theirs[section]
    ]


def measurement_flip(p: float, p_meas: str | float) -> float:
    return p if p_meas == SAME_AS_P else float(p_meas)


def stim_circuit(distance: int, basis: str, p: float, p_meas: float) -> stim.Circuit:
    # The framework's phenomenological model, as stim generates it:
    # depolarizing data noise at the start of each round, flips before every measurement,
    # ideal gates and resets, d rounds
    return stim.Circuit.generated(
        f"surface_code:rotated_memory_{basis.lower()}",
        distance=distance,
        rounds=distance,
        after_clifford_depolarization=0.0,
        after_reset_flip_probability=0.0,
        before_round_data_depolarization=p,
        before_measure_flip_probability=p_meas,
    )


def plan_to_stim_tasks(plan: SweepPlan) -> list[sinter.Task]:
    # Same tasks and metadata as cdsc.sweep.run.plan_to_tasks, with stim's circuits
    tasks = list()

    for distance in plan.distances:
        for p in plan.ps:
            circuit = stim_circuit(distance, plan.basis, p, measurement_flip(p, plan.p_meas))

            dem = circuit.detector_error_model(
                decompose_errors=True,
                approximate_disjoint_errors=True
            )

            tasks.append(sinter.Task(
                circuit=circuit,
                detector_error_model=dem,
                json_metadata={
                    "d": distance,
                    "p": p,
                    "sweep_id": plan.sweep_id,
                    "code": plan.code,
                    "basis": plan.basis,
                    "noise_model": plan.noise_model,
                    "noise_definition": plan.noise_definition,
                    **plan.params,
                },
            ))

    return tasks


def write_manifest(config: Config, config_path: str, reference_path: str | None) -> Path:
    # The framework's manifest, plus where the circuits came from
    manifest: dict[str, Any] = {
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "packages": installed_packages(),
        },
        "software": {
            "git_commit": commit_hash(),
            "git_dirty": git_dirty(),
            "plugins": {},
        },
        "circuit_source": CIRCUIT_SOURCE,
        "started_at": str(datetime.now()),
        "config_path": str(config_path),
        "reference_config_path": reference_path,
        "config": config.as_dict(),
    }

    output_dir = config.output.path
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "manifest.json"
    output_file.write_text(json.dumps(manifest, indent=2) + "\n")
    return output_file


def load(path: str) -> Config:
    try:
        return load_config(Path(path))
    except ConfigError as e:
        console.error(console.config_error_message(e))
        sys.exit(2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sample stim's generated circuits for A3")
    parser.add_argument("config", help="path to the stim-side YAML config")
    parser.add_argument("--reference", help="framework-side config that must match, apart from experiment and output")
    args = parser.parse_args()

    config = load(args.config)
    problems = unsupported(config)
    if problems:
        console.error("stim.Circuit.generated cannot reproduce this config:\n" + "\n".join(f"  {p}" for p in problems))
        return 2

    if args.reference is not None:
        differing = mismatches(config, load(args.reference))
        if differing:
            console.error(f"{args.config} differs from {args.reference} in: {', '.join(differing)}")
            return 2

    plans = build_sweep_plans(config)
    manifest_file = write_manifest(config, args.config, args.reference)
    decoder, custom_decoders = resolve_decoder(config.sampling.decoder)

    rows: list[dict] = list()
    for index, plan in enumerate(plans, start=1):
        console.plan_started(index, len(plans), plan)
        start = time.monotonic()

        stats = sinter.collect(
            num_workers=config.sampling.workers,
            tasks=plan_to_stim_tasks(plan),
            decoders=[decoder],
            custom_decoders=custom_decoders,
            max_shots=config.sampling.max_shots,
            max_errors=config.sampling.max_errors,
            max_batch_size=config.sampling.max_batch_size,
            print_progress=True
        )
        rows.extend(sample_row(stat) for stat in stats)

        shots = sum(stat.shots for stat in stats)
        errors = sum(stat.errors for stat in stats)
        console.plan_finished(index, len(plans), plan, shots, errors, time.monotonic() - start)

    samples_file = config.output.path / "samples.csv"
    pd.DataFrame(rows).to_csv(samples_file, index=False)

    console.info()
    console.wrote(manifest_file)
    console.wrote(samples_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
