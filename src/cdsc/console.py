"""Everything the cli prints: message formats, tables and warnings."""
from __future__ import annotations
import sys
import textwrap
from pathlib import Path
from typing import Any, Sequence
import numpy as np
import pandas as pd
from tabulate import tabulate
from .config import Config, SamplingConfig
from .sweep.run import SweepPlan
from .validation.validate import CHECK_NAMES, CodeValidation


# Warning limits
MIN_ERRORS = 100            # fewer errors than this: relative error > 10%
MAX_CHI2_RED = 2.0
MIN_P_VALUE = 0.01
MAX_EXTRAPOLATION = 2.0     # d_teraquop / largest sampled distance
MAX_LISTED = 3              # how many offending items a warning names


# --- Output ---

def info(text: str = "") -> None:
    print(text, file=sys.stdout, flush=True)


def warn(text: str) -> None:
    print(f"warning: {text}", file=sys.stderr, flush=True)


def warn_all(messages: list[str]) -> None:
    if not messages:
        return
    print(file=sys.stderr, flush=True)
    for message in messages:
        warn(message)


def error(text: str) -> None:
    print(f"error: {text}", file=sys.stderr, flush=True)


# --- Number formats ---

def fmt_prob(p: float) -> str:
    return f"{p:.2e}"


def fmt_threshold(p: float, err: float) -> str:
    return f"{p * 100:.4f}% ± {err * 100:.4f}%"


def fmt_count(n: int) -> str:
    return f"{int(n):,}"


def fmt_compact(n: float) -> str:
    for scale, suffix in ((1e9, "G"), (1e6, "M"), (1e3, "k")):
        if abs(n) >= scale:
            return f"{n / scale:.1f}{suffix}"
    return str(int(n))


def fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(int(round(seconds)), 60)
    if minutes < 60:
        return f"{minutes}m {secs:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}m"


def fmt_distances(distances: Sequence[int]) -> str:
    if len(distances) <= 4:
        return str(list(distances))
    return f"[{distances[0]} .. {distances[-1]}] ({len(distances)})"


def fmt_ps(ps: Sequence[float]) -> str:
    if len(ps) == 1:
        return fmt_prob(ps[0])
    return f"{len(ps)} pts [{fmt_prob(min(ps))} .. {fmt_prob(max(ps))}]"


def fmt_value(value: Any) -> str:
    # Noise parameter values read back from csv are floats: show 10.0 as 10
    return f"{value:g}" if isinstance(value, float) else str(value)


def fmt_params(params: dict[str, Any] | None) -> str:
    return "  ".join(f"{key}={fmt_value(value)}" for key, value in (params or {}).items())


# --- Tables ---

def table(rows: list[dict[str, Any]]) -> str:
    # Columns follow the key order of the row dicts
    return tabulate(rows, headers="keys", tablefmt="plain", disable_numparse=True)


def indent(text: str, prefix: str = "  ") -> str:
    return textwrap.indent(text, prefix)


def _param_names(config: Config) -> list[str]:
    return list(config.noise.params or {})


def _label(row: dict[str, Any], param_names: Sequence[str], extra: Sequence[str] = ()) -> str:
    parts = [str(row["code"]), str(row["basis"])]
    parts += [f"{name}={fmt_value(row[name])}" for name in param_names]
    parts += [f"{name}={fmt_prob(row[name]) if name == 'p' else fmt_value(row[name])}" for name in extra]
    return " ".join(parts)


def _listed(items: list[str]) -> str:
    shown = ", ".join(items[:MAX_LISTED])
    if len(items) > MAX_LISTED:
        shown += f", ... and {len(items) - MAX_LISTED} more"
    return shown


# --- Common ---

def header(command: str, config: Config, config_path: str | Path) -> None:
    info(f"cdsc {command}  experiment={config.experiment.name}  config={config_path}")
    info(f"  output:   {config.output.dir}")


def footer(ok: bool, elapsed: float) -> None:
    info()
    info(f"{'done' if ok else 'FAILED'} in {fmt_duration(elapsed)}")


def wrote(path: str | Path) -> None:
    info(f"wrote {path}")


def config_error_message(path: str | Path, exc: Exception) -> str:
    if isinstance(exc, FileNotFoundError):
        return f"config {path}: file not found"
    errors = getattr(exc, "errors", None)
    if callable(errors):
        details = "; ".join(
            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in errors()
        )
        return f"config {path}: {details}"
    return f"config {path}: {exc}"


def missing_input_message(path: str | Path, command: str, config_path: str | Path) -> str:
    return f"{path} not found; run `cdsc {command} {config_path}` first"


# --- run / compile-plans ---

def _plan_tasks(plan: SweepPlan) -> int:
    return len(plan.distances) * len(plan.ps)


def _plan_totals(plans: list[SweepPlan], sampling: SamplingConfig) -> str:
    tasks = sum(_plan_tasks(plan) for plan in plans)
    return (
        f"{len(plans)} plans, {fmt_count(tasks)} tasks, "
        f"≤ {fmt_compact(tasks * sampling.max_shots)} shots"
    )


def run_details(config: Config, commit: str, dirty: bool, plans: list[SweepPlan]) -> None:
    noise, sampling = config.noise, config.sampling
    params = "  ".join(f"{key}={values}" for key, values in (noise.params or {}).items())
    sweeps = len({plan.sweep_id for plan in plans})
    info(f"  git:      {commit[:7]}{' (dirty)' if dirty else ''}")
    info(f"  noise:    {noise.model} / {noise.definition}  params: {params or '-'}  p_meas={noise.p_meas}")
    info(
        f"  sampling: decoder={sampling.decoder}  max_shots={fmt_count(sampling.max_shots)}  "
        f"max_errors={fmt_count(sampling.max_errors)}  workers={sampling.workers}"
    )
    info(f"  plan:     {sweeps} sweeps, {_plan_totals(plans, sampling)}")


def plan_table(plans: list[SweepPlan], sampling: SamplingConfig) -> None:
    rows = [
        {
            "#": index,
            "sweep": plan.sweep_id,
            "code": plan.code,
            "basis": plan.basis,
            "params": fmt_params(plan.params) or "-",
            "d": fmt_distances(plan.distances),
            "p": fmt_ps(plan.ps),
            "tasks": fmt_count(_plan_tasks(plan)),
        }
        for index, plan in enumerate(plans, start=1)
    ]
    info()
    info(indent(table(rows)))
    info()
    info(f"total: {_plan_totals(plans, sampling)} (max_shots={fmt_count(sampling.max_shots)})")


def plan_started(index: int, total: int, plan: SweepPlan) -> None:
    width = len(str(total))
    info()
    info(
        f"[{index:>{width}}/{total}] {plan.sweep_id}  {plan.code}  basis={plan.basis}  "
        f"{fmt_params(plan.params)}  d={fmt_distances(plan.distances)}  "
        f"p={fmt_ps(plan.ps)}  ({fmt_count(_plan_tasks(plan))} tasks)"
    )


def plan_finished(index: int, total: int, plan: SweepPlan, shots: int, errors: int, elapsed: float) -> None:
    pad = " " * (2 * len(str(total)) + 3)
    info(f"{pad} done in {fmt_duration(elapsed)}  shots={fmt_compact(shots)}  errors={fmt_count(errors)}")


def samples_summary(samples: pd.DataFrame, config: Config) -> None:
    sampling = config.sampling
    info()
    info(f"samples: {fmt_count(len(samples))} rows")
    if samples.empty:
        return
    enough_errors = samples["errors"] >= sampling.max_errors
    out_of_shots = (samples["shots"] >= sampling.max_shots) & ~enough_errors
    info(f"  limited by max_errors: {fmt_count(enough_errors.sum())} tasks")
    info(f"  limited by max_shots:  {fmt_count(out_of_shots.sum())} tasks")

    param_names = _param_names(config)
    rows = samples.to_dict("records")
    zero = [
        f"{row['sweep_id']} {_label(row, param_names, ('d', 'p'))}"
        for row in rows if row["errors"] == 0
    ]
    messages = []
    if zero:
        messages.append(f"{len(zero)} tasks observed 0 errors ({_listed(zero)})")
    low = [row for row in rows if 0 < row["errors"] < MIN_ERRORS]
    if low:
        messages.append(f"{len(low)} tasks have < {MIN_ERRORS} errors; their error bars will be wide")
    warn_all(messages)


# --- validate ---

def validation_summary(entries: list[tuple[str, int, CodeValidation]], distances: Sequence[int]) -> None:
    code_ids = list(dict.fromkeys(code_id for code_id, _, _ in entries))
    info(f"  codes:    {', '.join(code_ids)}   distances: {list(distances)}   checks: {len(CHECK_NAMES)}")

    rows = [
        {
            "code": code_id,
            "d": distance,
            "result": "PASS" if validation.passed else "FAIL",
            "failed checks": ", ".join(result.name for result in validation.failures),
        }
        for code_id, distance, validation in entries
    ]
    info()
    info(indent(table(rows)))

    for _, _, validation in entries:
        if validation.passed:
            continue
        info()
        info(f"FAILED  {validation.key}")
        for result in validation.failures:
            info(f"  {result.name}: {result.message}")

    failed = sum(not validation.passed for _, _, validation in entries)
    info()
    info(f"summary: {len(entries) - failed}/{len(entries)} passed, {failed} failed")


# --- analyze ---

def _poor_fit(row: dict[str, Any]) -> bool:
    return row["p_value"] < MIN_P_VALUE or row["chi2_red"] > MAX_CHI2_RED


def _at_bounds(row: dict[str, Any]) -> list[str]:
    # Fit bounds in estimate_threshold: p_th in [0, 1], nu in [1, 2]
    hits = []
    if np.isclose(row["nu"], 1.0) or np.isclose(row["nu"], 2.0):
        hits.append(f"nu={row['nu']:.2f}")
    if np.isclose(row["p_th"], 0.0) or np.isclose(row["p_th"], 1.0):
        hits.append(f"p_th={row['p_th']:.3g}")
    return hits


def thresholds(df: pd.DataFrame, config: Config) -> None:
    th = config.threshold
    param_names = _param_names(config)
    records = df.to_dict("records")

    rows = [
        {
            "code": row["code"],
            "basis": row["basis"],
            **{name: fmt_value(row[name]) for name in param_names},
            "p_th": fmt_threshold(row["p_th"], row["p_th_err"]),
            "nu": f"{row['nu']:.2f}",
            "chi2_red": f"{row['chi2_red']:.2f}",
            "p-value": f"{row['p_value']:.3f}",
            "": "!" if _poor_fit(row) or _at_bounds(row) else "",
        }
        for row in records
    ]
    info()
    info(f"threshold  (sweep={th.source_sweep}, d={list(th.distances)}, x_window={th.x_window})")
    info(indent(table(rows)))

    messages = []
    for row in records:
        if _poor_fit(row):
            messages.append(
                f"{_label(row, param_names)}: poor fit "
                f"(chi2_red={row['chi2_red']:.2f}, p-value={row['p_value']:.3f})"
            )
        hits = _at_bounds(row)
        if hits:
            messages.append(f"{_label(row, param_names)}: fit parameter at its bound ({', '.join(hits)})")
    warn_all(messages)


def suppressions(df: pd.DataFrame, config: Config) -> None:
    sup = config.suppression
    param_names = _param_names(config)
    source = next((sweep for sweep in config.sweeps if sweep.id == sup.source_sweep), None)
    max_d = max(source.distances) if source is not None else None

    records = df.to_dict("records")
    skipped = [row for row in records if isinstance(row.get("skipped"), str)]
    fitted = [row for row in records if not isinstance(row.get("skipped"), str)]

    rows = [
        {
            "code": row["code"],
            "basis": row["basis"],
            **{name: fmt_value(row[name]) for name in param_names},
            "p": fmt_prob(row["p"]),
            "d_teraquop": int(row["d_teraquop"]),
            "qubits": fmt_count(row["qubits"]),
        }
        for row in fitted
    ]
    info()
    info(f"suppression  (sweep={sup.source_sweep}, target p_L={sup.target_pl:g})")
    info(indent(table(rows)))

    messages = []
    for row in fitted:
        if max_d is not None and row["d_teraquop"] > MAX_EXTRAPOLATION * max_d:
            messages.append(
                f"{_label(row, param_names, ('p',))}: d_teraquop={int(row['d_teraquop'])} "
                f"is extrapolated far beyond the largest sampled d={max_d}"
            )
    for row in skipped:
        messages.append(f"{_label(row, param_names, ('p',))}: skipped ({row['skipped']})")
    warn_all(messages)


# --- visualize ---

def rendered(items: list[tuple[str, str, list[Path]]]) -> None:
    # items: (kind, detail, paths) for each group of generated files
    rows = []
    for kind, detail, paths in items:
        folders = sorted({str(path.parent) for path in paths})
        rows.append({
            "kind": kind,
            "detail": detail,
            "files": len(paths),
            "output": f"{folders[0]}/" if len(folders) == 1 else ", ".join(folders) or "-",
        })
    info()
    info(indent(table(rows)))
