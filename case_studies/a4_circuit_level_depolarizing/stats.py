from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm, pearsonr

from cdsc.config import load_config

RESULTS = Path(__file__).parent / "results"
OUT = RESULTS / "orourke2025_zscore.csv"
STATS = RESULTS / "stats.txt"
OROURKE2025_P_TH = 0.5637, 0.0004  # %, Table III (SD noise, rotated code, memory Z)


def pl_zscores():
    # deviation = (pl_framework - pl_orourke) / combined sigma, on the (p, d) points both CSVs share
    # round_trip keeps pl and sigma digit for digit as in the input CSVs
    ours = pd.read_csv(RESULTS / "samples.csv", float_precision="round_trip")
    ours = ours[ours["sweep_id"] == "threshold_sweep"]
    paper = pd.read_csv(RESULTS / "orourke2025_samples.csv", float_precision="round_trip")
    t = ours.merge(paper, on=["d", "rounds", "p", "basis"], suffixes=("_framework", "_orourke"))
    t["deviation"] = (t["pl_framework"] - t["pl_orourke"]) / np.hypot(t["sigma_framework"], t["sigma_orourke"])
    columns = ["d", "p", "pl_framework", "sigma_framework", "pl_orourke", "sigma_orourke", "deviation"]
    return t[columns].sort_values(["d", "p"], ignore_index=True)


def print_normality(z):
    n = len(z)
    for k in (1, 2):
        inside = int((z.abs() <= k).sum())
        print(f"{k}σ: {inside}/{n} ({inside / n:.1%}), N(0,1): {norm.cdf(k) - norm.cdf(-k):.1%}")
    # the largest |z|, next to the median of the largest |z| among n draws from N(0,1)
    print(f"max |z|: {z.abs().max():.1f}σ, N(0,1) median: {norm.ppf((1 + 0.5 ** (1 / n)) / 2):.1f}σ")


def print_trend(table):
    # Pearson correlation of the deviation with p and with d: a trend, unlike the mean offset,
    # would point to a p- or d-dependent　difference between the two circuits
    for var in ("p", "d"):
        r = pearsonr(table[var], table["deviation"])
        print(f"deviation vs {var}: r = {r.statistic:+.2f}, p-value = {r.pvalue:.2f}")


def print_pl_ratio(table):
    # inverse-variance weighted mean of pl_framework / pl_orourke
    r = table["pl_framework"] / table["pl_orourke"]
    err = r * np.hypot(table["sigma_framework"] / table["pl_framework"], table["sigma_orourke"] / table["pl_orourke"])
    w = err ** -2
    print(f"pl ratio weighted mean (framework/orourke) = {(w * r).sum() / w.sum():.4f} ± {w.sum() ** -0.5:.4f}")


def print_threshold_diff():
    # p_th(framework) - p_th(ORourke2025 Table III), in percentage points and in units of the combined sigma
    th = pd.read_csv(RESULTS / "threshold.csv")
    paper, paper_err = OROURKE2025_P_TH
    for basis, p_th, p_th_err in zip(th["basis"], 100 * th["p_th"], 100 * th["p_th_err"]):
        dp, e = p_th - paper, np.hypot(p_th_err, paper_err)
        print(f"p_th {basis} (framework - orourke) = {dp:+.4f} ± {e:.4f} points ({dp / e:+.1f}σ)")


def print_shot_budget():
    # total shots per sweep, and the points that stopped at max_shots, with their fewest errors
    max_shots = load_config(RESULTS.parent / "config.yaml").sampling.max_shots
    df = pd.read_csv(RESULTS / "samples.csv")
    for sweep, g in df.groupby("sweep_id", sort=False):
        capped = g[g["shots"] >= max_shots]
        line = f"{sweep}: {g['shots'].sum():,} shots, {len(capped)}/{len(g)} points stopped at max_shots = {max_shots:,}"
        if len(capped):
            line += f", fewest errors among them = {capped['errors'].min():,}"
        print(line)


def main():
    table = pl_zscores()
    table.assign(deviation=table["deviation"].map("{:.6f}".format)).to_csv(OUT, index=False)
    with STATS.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print_normality(table["deviation"])
        print()
        print_trend(table)
        print()
        print_pl_ratio(table)
        print()
        print_threshold_diff()
        print()
        print_shot_budget()
    print(f"wrote {OUT.relative_to(RESULTS.parent)} and {STATS.relative_to(RESULTS.parent)}")


if __name__ == "__main__":
    main()
