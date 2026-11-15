from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

RESULTS = Path(__file__).parent / "results"
OUT = RESULTS / "stim_zscore.csv"
STATS = RESULTS / "stats.txt"


def load(source):
    # round_trip keeps pl and sigma digit for digit as in the input CSVs
    df = pd.read_csv(RESULTS / source / "samples.csv", float_precision="round_trip")
    return df[df["sweep_id"] == "threshold_sweep"]


def pl_zscores():
    # deviation = (pl_framework - pl_stim) / combined sigma, on the (basis, p, d) points both CSVs share
    t = load("framework").merge(load("stim"), on=["basis", "d", "p"], suffixes=("_framework", "_stim"))
    t["deviation"] = (t["pl_framework"] - t["pl_stim"]) / np.hypot(t["sigma_framework"], t["sigma_stim"])
    columns = ["basis", "d", "p", "pl_framework", "sigma_framework", "pl_stim", "sigma_stim", "deviation"]
    return t[columns].sort_values(["basis", "d", "p"], ignore_index=True)


def print_normality(z):
    n = len(z)
    for k in (1, 2):
        inside = int((z.abs() <= k).sum())
        print(f"{k}σ: {inside}/{n} ({inside / n:.1%}), N(0,1): {norm.cdf(k) - norm.cdf(-k):.1%}")


def print_pl_ratio(table):
    # inverse-variance weighted mean of pl_framework / pl_stim
    r = table["pl_framework"] / table["pl_stim"]
    err = r * np.hypot(table["sigma_framework"] / table["pl_framework"], table["sigma_stim"] / table["pl_stim"])
    w = err ** -2
    print(f"pl ratio weighted mean (framework/stim) = {(w * r).sum() / w.sum():.4f} ± {w.sum() ** -0.5:.4f}")


def print_threshold_diff():
    # p_th(framework) - p_th(stim) per basis, in percentage points and in units of the combined sigma
    th = pd.read_csv(RESULTS / "framework" / "threshold.csv").merge(
        pd.read_csv(RESULTS / "stim" / "threshold.csv"), on="basis", suffixes=("_framework", "_stim"))
    diff = 100 * (th["p_th_framework"] - th["p_th_stim"])
    err = 100 * np.hypot(th["p_th_err_framework"], th["p_th_err_stim"])
    for basis, dp, e in zip(th["basis"], diff, err):
        print(f"p_th {basis} (framework - stim) = {dp:+.3f} ± {e:.3f} points ({dp / e:+.1f}σ)")


def print_threshold_pulls():
    # each p_th against the weighted mean of all four, as a z score (sigma_i^2 - sigma_mean^2 removes x_i's share of the mean)
    th = pd.concat([pd.read_csv(RESULTS / s / "threshold.csv").assign(source=s) for s in ("framework", "stim")])
    x, e = 100 * th["p_th"], 100 * th["p_th_err"]
    w = e ** -2
    mean, mean_err = (w * x).sum() / w.sum(), w.sum() ** -0.5
    print(f"p_th weighted mean = {mean:.3f} ± {mean_err:.3f}%")
    for source, basis, xi, ei in zip(th["source"], th["basis"], x, e):
        print(f"p_th {basis} {source} - mean = {(xi - mean) / (ei ** 2 - mean_err ** 2) ** 0.5:+.1f}σ")


def main():
    table = pl_zscores()
    table.assign(deviation=table["deviation"].map("{:.6f}".format)).to_csv(OUT, index=False)
    with STATS.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print_normality(table["deviation"])
        print()
        print_pl_ratio(table)
        print()
        print_threshold_diff()
        print()
        print_threshold_pulls()
    print(f"wrote {OUT.relative_to(RESULTS.parent)} and {STATS.relative_to(RESULTS.parent)}")


if __name__ == "__main__":
    main()
