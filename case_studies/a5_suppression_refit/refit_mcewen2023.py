# Refit McEwen2023's released memory-experiment counts with McEwen2023's own footprint fit and with cdsc's suppression fit.
# McEwen2023: M. McEwen, D. Bacon, C. Gidney, "Relaxing hardware requirements for surface code circuits using
# time-dynamics", Quantum 7, 1172 (2023), arXiv:2302.02192. Data: Zenodo 7587578, fused_stats.csv (CC-BY 4.0).
# Code: github.com/Strilanc/midout (Apache-2.0); its fit is re-implemented below, with the source of each part.
#
# The counts: X and Z memory experiments fused into one "XZ" row per (style, noise, d, p): the smaller shot count,
# and errors for "X or Z fails", 1 - (1 - p_X)(1 - p_Z). r = 4d rounds, q = 2d^2 - 1 qubits for the standard circuits.
# - McEwen2023 (tools/plot_footprint): p_L per d rounds with xz_piece_error_rate(pieces = r/d, combo = True),
#   then sqrt(q) against ln(p_L per d rounds), unweighted, with sinter.fit_line_y_at_x(max_extra_squared_error=1)
#   at 1e-12, squared: the teraquop footprint and its band
# - cdsc: cdsc.analysis.suppression.estimate_suppression on the same tasks: p_L per round (pieces = r), log10 against d,
#   weighted by the binomial sigma (Wilson, cdsc.sweep.run.sample_row), d* for 1e-12 per d rounds, n* = 2 d*^2 - 1
# - cdsc with McEwen2023's unit: estimate_suppression on p_L per d rounds (rounds = r/d, so pieces = r/d), its weighted
#   line, then d* where that line meets 1e-12 directly (estimate_suppression's own d* assumes a per-round line)
# All use the tasks McEwen2023 keeps: 0 < p_shot < 0.3.

# Usage:
# python case_studies/a5_suppression_refit/refit_mcewen2023.py [--stats CSV] [--out-dir DIR]
# Writes mcewen2023_footprint.csv next to this script unless --out-dir is given.

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import sinter

import cdsc.codes.builtin  # noqa: F401  registers rotated_surface (q = 2d^2 - 1) for estimate_suppression
from cdsc.analysis.suppression import estimate_suppression
from cdsc.sweep.run import sample_row

HERE = Path(__file__).resolve().parent
STYLES = {"4-CZ": "SI1000", "4-CX": "UniformDepolarizing"}  # the standard circuits, with CZ and with CX
TARGET = 1e-12
MAX_P_SHOT = 0.3


def xz_piece_error_rate(p_combo: float, *, pieces: float, combo: bool) -> float:
    # Verbatim from midout, src/midout/all_circuits.py
    if not combo:
        return sinter.shot_error_rate_to_piece_error_rate(p_combo, pieces=pieces)
    p_solo = 1 - (1 - p_combo)**0.5
    unit_solo = sinter.shot_error_rate_to_piece_error_rate(p_solo, pieces=pieces)
    unit_combo = unit_solo*(2 - unit_solo)
    return unit_combo


def mcewen2023_footprint(tasks: list[sinter.TaskStats]) -> sinter.Fit | None:
    # The fit of midout's tools/plot_footprint, for one (style, p)
    log_ps, sqrt_qs = [], []
    for stat in tasks:
        meta = stat.json_metadata
        p_shot = stat.errors / stat.shots
        p_unit = xz_piece_error_rate(p_shot, pieces=meta["r"] / meta["d"], combo=meta["b"] == "XZ")
        log_ps.append(math.log(p_unit))
        sqrt_qs.append(math.sqrt(meta["q"]))
    if len(log_ps) < 2:
        return None
    slope_fit = sinter.fit_line_slope(xs=log_ps, ys=sqrt_qs, max_extra_squared_error=1)
    if slope_fit.best >= 0:
        return None
    fit = sinter.fit_line_y_at_x(xs=log_ps, ys=sqrt_qs, target_x=math.log(TARGET), max_extra_squared_error=1)
    return sinter.Fit(low=fit.low**2, best=fit.best**2, high=fit.high**2)


def cdsc_footprint(tasks: list[sinter.TaskStats]) -> dict:
    samples = pd.DataFrame([sample_row(stat) for stat in tasks]).rename(columns={"r": "rounds"})
    fit = estimate_suppression(samples, "rotated_surface", TARGET)

    # McEwen2023's unit: one piece per d rounds, and a line in log10(p_L per d rounds) that meets the target directly
    per_d = samples.assign(rounds=samples["rounds"] / samples["d"])
    fit_d = estimate_suppression(per_d, "rotated_surface", TARGET)
    d_star_d = (np.log10(TARGET) - fit_d.intercept) / fit_d.slope
    return {"cdsc_d_star": fit.d_star, "cdsc_n_star": 2 * fit.d_star**2 - 1,
            "cdsc_d_teraquop": fit.d_teraquop, "cdsc_qubits": fit.qubits,
            "cdsc_per_d_d_star": d_star_d, "cdsc_per_d_n_star": 2 * d_star_d**2 - 1}


def compare(stats: list[sinter.TaskStats]) -> tuple[pd.DataFrame, list[str]]:
    groups: dict[tuple[str, float], list[sinter.TaskStats]] = {}
    for stat in stats:
        meta = stat.json_metadata
        if meta.get("b") != "XZ" or STYLES.get(meta.get("style")) != meta.get("noise"):
            continue
        if stat.shots and 0 < stat.errors / stat.shots < MAX_P_SHOT:
            groups.setdefault((meta["style"], meta["p"]), []).append(stat)

    rows, skipped = [], []
    for (style, p), tasks in sorted(groups.items()):
        tasks.sort(key=lambda s: s.json_metadata["d"])
        key = {"style": style, "noise": STYLES[style], "p": p,
               "distances": " ".join(str(s.json_metadata["d"]) for s in tasks), "points": len(tasks)}
        mcewen = mcewen2023_footprint(tasks)
        try:
            cdsc = cdsc_footprint(tasks)
        except ValueError as e:
            cdsc = None
            skipped.append(f"{style} p = {p}: cdsc skipped ({e})")
        if mcewen is None:
            skipped.append(f"{style} p = {p}: McEwen2023's fit has no suppression")
        if mcewen is None or cdsc is None:
            continue
        rows.append({
            **key,
            "mcewen_low": mcewen.low, "mcewen_best": mcewen.best, "mcewen_high": mcewen.high,
            **cdsc,
            "ratio": cdsc["cdsc_n_star"] / mcewen.best,
            "in_band": mcewen.low <= cdsc["cdsc_n_star"] <= mcewen.high,
            "per_d_ratio": cdsc["cdsc_per_d_n_star"] / mcewen.best,
            "per_d_in_band": mcewen.low <= cdsc["cdsc_per_d_n_star"] <= mcewen.high,
        })
    return pd.DataFrame(rows), skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Refit McEwen2023's counts with its own footprint fit and with cdsc's.")
    parser.add_argument("--stats", default=str(HERE / "fused_stats.csv"),
                        help="McEwen2023's fused_stats.csv (default: next to this script)")
    parser.add_argument("--out-dir", default=str(HERE), help="output directory (default: next to this script)")
    args = parser.parse_args()

    try:
        stats = sinter.stats_from_csv_files(args.stats)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    result, skipped = compare(stats)
    if result.empty:
        print("error: no (style, p) has both fits", file=sys.stderr)
        return 2

    print("Teraquop footprint (qubits): McEwen2023's fit [band], cdsc's n* = 2d*^2 - 1 per round and per d rounds:")
    for _, row in result.iterrows():
        print(f"  {row['style']:5s} p = {row['p']:<7g} d = {row['distances']:<20s} "
              f"McEwen2023 {row['mcewen_best']:8.0f} [{row['mcewen_low']:.0f}, {row['mcewen_high']:.0f}]  "
              f"cdsc {row['cdsc_n_star']:7.0f} ({row['ratio']:.3f}, {'in' if row['in_band'] else 'OUT'})  "
              f"per d rounds {row['cdsc_per_d_n_star']:7.0f} ({row['per_d_ratio']:.3f}, {'in' if row['per_d_in_band'] else 'OUT'})")
    for style, group in result.groupby("style"):
        print(f"  {style}: cdsc {int(group['in_band'].sum())} of {len(group)} in band "
              f"(ratio {group['ratio'].min():.3f}-{group['ratio'].max():.3f}); per d rounds "
              f"{int(group['per_d_in_band'].sum())} of {len(group)} "
              f"(ratio {group['per_d_ratio'].min():.3f}-{group['per_d_ratio'].max():.3f})")
    for line in skipped:
        print(f"  {line}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_dir / "mcewen2023_footprint.csv", index=False)
    print(f"wrote {out_dir / 'mcewen2023_footprint.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
