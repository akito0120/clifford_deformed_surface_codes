from __future__ import annotations
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote
import pandas as pd
from tabulate import tabulate
from . import console
from .config import Config, DEFAULT_ROUNDS
from .console import fmt_compact, fmt_count, fmt_distances, fmt_duration, fmt_prob, fmt_ps, fmt_threshold, fmt_value
from .visualization.figures import make_figure_tag


# Config keys that decide what run samples: after a change to one of them, samples.csv no longer follows the config
SAMPLED_KEYS = ("experiment", "plugins", "codes", "noise", "sweeps", "sampling")

# Every output file: what it holds, and the command that writes it
FILES = (
    ("validation.json", "check results for each code and distance", "validate"),
    ("plans.json", "sweep plans", "compile-plans"),
    ("samples.csv", "shots, errors and p_L for each task", "run"),
    ("manifest.json", "config, environment, git commit, plugin hashes, run times", "run"),
    ("threshold.csv", "threshold fits", "analyze"),
    ("suppression.csv", "suppression fits and teraquop footprints", "analyze"),
    ("figures/", "threshold and suppression plots (PDF)", "visualize"),
    ("diagrams/", "circuit diagrams (SVG)", "visualize"),
)


def build_summary(config: Config, config_path: str) -> str:
    # The analysis results are required
    # manifest.json and validation.json may be missing
    out = config.output.path
    samples = pd.read_csv(out / "samples.csv")
    thresholds = pd.read_csv(out / "threshold.csv")
    suppressions = pd.read_csv(out / "suppression.csv")
    manifest = _read_json(out / "manifest.json")
    validation = _read_json(out / "validation.json")

    sections = [
        f"# Summary: {config.experiment.name}\n\nWritten by `cdsc summarize` on {datetime.now():%Y-%m-%d %H:%M}.",
        _setup(config, config_path, samples, manifest),
        _warnings(config, config_path, samples, thresholds, suppressions, manifest, validation),
        _threshold(config, thresholds),
        _footprint(config, suppressions),
        _sampling(config, samples),
        _validation(validation),
        _diagrams(config),
        _files(out),
    ]
    return "\n\n".join(sections) + "\n"


# --- Markdown ---

def _read_json(path: Path) -> Optional[dict[str, Any]]:
    return json.loads(path.read_text()) if path.exists() else None


def _link(text: str, target: str) -> str:
    # target is relative to summary.md
    return f"[{text}]({quote(target)})"


def _relative(path: str | Path, out: Path) -> str:
    # A path outside the output directory, as seen from summary.md
    return Path(os.path.relpath(Path(path).resolve(), out.resolve())).as_posix()


def _table(rows: list[dict[str, Any]]) -> str:
    cells = [{key: str(value).replace("|", "\\|") for key, value in row.items()} for row in rows]
    return tabulate(cells, headers="keys", tablefmt="github", disable_numparse=True)


def _section(title: str, *parts: str) -> str:
    return "\n\n".join([f"## {title}", *parts])


def _param_names(config: Config) -> list[str]:
    return list(config.noise.params or {})


def _figure_link(out: Path, kind: str, row: dict[str, Any], param_names: list[str]) -> str:
    # The name visualize gives the figure of this row's code, basis and noise parameters
    key = [row["code"], row["basis"], *(row[name] for name in param_names)]
    target = f"figures/{kind}{make_figure_tag(key)}.pdf"
    return _link("PDF", target) if (out / target).exists() else "—"


def _natural(path: Path) -> list[Any]:
    # d3 before d11
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.name)]


# --- Sections ---

def _setup(config: Config, config_path: str, samples: pd.DataFrame, manifest: Optional[dict[str, Any]]) -> str:
    out = config.output.path
    noise, sampling = config.noise, config.sampling
    params = "".join(f", {key} = {values}" for key, values in (noise.params or {}).items())
    lines = [
        f"- Config: {_link(str(config_path), _relative(config_path, out))}",
        f"- Codes: {', '.join(config.codes)}",
        f"- Noise: {noise.model} / {noise.definition}{params}, p_meas = {noise.p_meas}",
    ]
    if config.plugins:
        lines.append("- Plugins: " + ", ".join(_link(entry, _relative(entry, out)) for entry in config.plugins))

    # What was sampled, from samples.csv
    lines.append("- Sweeps:")
    for sweep in config.sweeps:
        rows = samples[samples["sweep_id"] == sweep.id]
        if rows.empty:
            lines.append(f"  - `{sweep.id}`: no samples")
            continue
        distances = sorted(int(d) for d in rows["d"].unique())
        ps = sorted(float(p) for p in rows["p"].unique())
        bases = ", ".join(sorted(rows["basis"].unique()))
        rounds = "" if noise.model == "code_capacity" else f", rounds = {sweep.rounds or DEFAULT_ROUNDS}"
        lines.append(f"  - `{sweep.id}`: d = {fmt_distances(distances)}{rounds}, basis {bases}, p = {fmt_ps(ps)}")

    lines.append(
        f"- Sampling: decoder {sampling.decoder}, each task until {fmt_count(sampling.max_errors)} errors "
        f"or {fmt_count(sampling.max_shots)} shots, {sampling.workers} workers"
    )
    lines.append(f"- Run: {_run(manifest)}")
    return _section("Setup", "\n".join(lines))


def _run(manifest: Optional[dict[str, Any]]) -> str:
    if manifest is None:
        return "manifest.json not found"
    started = datetime.fromisoformat(manifest["started_at"])
    text = f"{started:%Y-%m-%d %H:%M:%S}"
    # Manifests written before finished_at was added have no finish time
    if manifest.get("finished_at"):
        finished = datetime.fromisoformat(manifest["finished_at"])
        end = f"{finished:%H:%M:%S}" if finished.date() == started.date() else f"{finished:%Y-%m-%d %H:%M:%S}"
        text += f" → {end} ({fmt_duration((finished - started).total_seconds())})"
    software = manifest.get("software", {})
    if software.get("git_commit"):
        text += f", git {software['git_commit'][:7]}"
        if software.get("git_dirty"):
            text += " with uncommitted changes"
    return text


def _warnings(
    config: Config,
    config_path: str,
    samples: pd.DataFrame,
    thresholds: pd.DataFrame,
    suppressions: pd.DataFrame,
    manifest: Optional[dict[str, Any]],
    validation: Optional[dict[str, Any]],
) -> str:
    # The warnings of run and analyze, with the same wording as on the console
    messages = _validation_warnings(config, config_path, validation) + _config_warnings(config, manifest)
    messages += console.sample_warnings(samples, config)
    messages += console.threshold_warnings(thresholds, config)
    messages += console.suppression_warnings(suppressions, config)
    body = "\n".join(f"- {message}" for message in messages) if messages else "None."
    return _section("Warnings", body)


def _validation_warnings(config: Config, config_path: str, validation: Optional[dict[str, Any]]) -> list[str]:
    if validation is None:
        return [console.missing_input_message("validation.json", "validate", config_path)]
    messages = []
    failed = [key for key, record in validation.items() if not record["passed"]]
    if failed:
        messages.append(f"validation failed for {', '.join(failed)}; see Validation")
    # validation.json keys are "<code id>_d<distance>"
    validated = {key.rsplit("_d", 1)[0] for key in validation}
    missing = [code for code in config.codes if code not in validated]
    if missing:
        messages.append(f"no validation result for {', '.join(missing)}")
    return messages


def _config_warnings(config: Config, manifest: Optional[dict[str, Any]]) -> list[str]:
    if manifest is None or "config" not in manifest:
        return []
    # Through JSON, so that the current config compares like the recorded one
    current = json.loads(json.dumps(config.as_dict()))
    changed = [key for key in SAMPLED_KEYS if manifest["config"].get(key) != current.get(key)]
    if not changed:
        return []
    return [
        f"{', '.join(changed)} in the config changed after `cdsc run`; "
        "samples.csv was made with the config recorded in manifest.json"
    ]


def _threshold(config: Config, thresholds: pd.DataFrame) -> str:
    th, out = config.threshold, config.output.path
    param_names = _param_names(config)
    rows = [
        {
            "code": row["code"],
            "basis": row["basis"],
            **{name: fmt_value(row[name]) for name in param_names},
            "p_th": fmt_threshold(row["p_th"], row["p_th_err"]),
            "ν": f"{row['nu']:.2f}",
            "χ²_red": f"{row['chi2_red']:.2f}",
            "p-value": f"{row['p_value']:.3f}",
            "figure": _figure_link(out, "threshold", row, param_names),
        }
        for row in thresholds.to_dict("records")
    ]
    intro = (
        f"Sweep `{th.source_sweep}`, fit on d = {list(th.distances)}, x_window = {th.x_window}, "
        f"ν0 = {th.nu_0}. Data: {_link('threshold.csv', 'threshold.csv')}"
    )
    return _section("Threshold", intro, _table(rows) if rows else "No fits.")


def _footprint(config: Config, suppressions: pd.DataFrame) -> str:
    sup, out = config.suppression, config.output.path
    param_names = _param_names(config)
    rows = [
        {
            "code": row["code"],
            "basis": row["basis"],
            **{name: fmt_value(row[name]) for name in param_names},
            "p": fmt_prob(row["p"]),
            "d*": f"{row['d_star']:.1f}",
            "d_teraquop": int(row["d_teraquop"]),
            "qubits": fmt_count(row["qubits"]),
            "figure": _figure_link(out, "suppression", row, param_names),
        }
        for row in suppressions.to_dict("records")
        # A row with no fit carries the reason in "skipped" (listed under Warnings)
        if not isinstance(row.get("skipped"), str)
    ]
    intro = (
        f"Sweep `{sup.source_sweep}`, target p_L = {sup.target_pl:g} per d rounds. "
        f"Data: {_link('suppression.csv', 'suppression.csv')}"
    )
    return _section("Teraquop footprint", intro, _table(rows) if rows else "No fits; see Warnings.")


def _sampling(config: Config, samples: pd.DataFrame) -> str:
    param_names = _param_names(config)
    by_errors, by_shots = console.limited_by(samples, config.sampling)
    intro = (
        f"Data: {_link('samples.csv', 'samples.csv')}. {fmt_count(len(samples))} tasks, "
        f"{fmt_compact(samples['shots'].sum())} shots, {fmt_count(samples['errors'].sum())} errors. "
        f"Limited by max_errors: {fmt_count(by_errors)} tasks; by max_shots: {fmt_count(by_shots)} tasks."
    )

    # One row per plan, in the order they were sampled
    rows = []
    for key, group in samples.groupby(["sweep_id", "code", "basis", *param_names], sort=False):
        sweep_id, code, basis, *values = key
        rows.append({
            "sweep": sweep_id,
            "code": code,
            "basis": basis,
            **{name: fmt_value(value) for name, value in zip(param_names, values)},
            "d": fmt_distances(sorted(int(d) for d in group["d"].unique())),
            "p": fmt_ps(sorted(float(p) for p in group["p"].unique())),
            "tasks": fmt_count(len(group)),
            "shots": fmt_compact(group["shots"].sum()),
            "min errors": fmt_count(group["errors"].min()),
        })
    return _section("Sampling", intro, _table(rows))


def _validation(validation: Optional[dict[str, Any]]) -> str:
    if validation is None:
        return _section("Validation", "validation.json not found.")
    failed = {key: record for key, record in validation.items() if not record["passed"]}
    parts = [
        f"Data: {_link('validation.json', 'validation.json')}. "
        f"{len(validation) - len(failed)} of {len(validation)} passed."
    ]
    failures = [
        f"- `{key}` {name}: {' '.join(str(check.get('message', '')).split())}"
        for key, record in failed.items()
        for name, check in record["checks"].items()
        if not check["passed"]
    ]
    if failures:
        parts.append("\n".join(failures))
    return _section("Validation", *parts)


def _diagrams(config: Config) -> str:
    out = config.output.path
    lines = []
    for code in config.codes:
        paths = sorted((out / "diagrams" / code).glob("*.svg"), key=_natural)
        links = [
            _link(path.stem.removeprefix(f"{code}_").replace("_", " "), path.relative_to(out).as_posix())
            for path in paths
        ]
        lines.append(f"- {code}: {' · '.join(links) if links else 'not found'}")
    return _section("Circuit diagrams", "\n".join(lines))


def _files(out: Path) -> str:
    rows = [
        {
            "file": _link(name, name) if (out / name).exists() else f"{name} (not found)",
            "contents": contents,
            "written by": f"`cdsc {command}`",
        }
        for name, contents, command in FILES
    ]
    return _section("Files", _table(rows))
