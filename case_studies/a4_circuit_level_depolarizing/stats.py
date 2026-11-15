from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

RESULTS = Path(__file__).parent / "results"
OUT = RESULTS / "orourke2025_zscore.csv"


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


def print_pl_ratio(table):
    # inverse-variance weighted mean of pl_framework / pl_orourke
    r = table["pl_framework"] / table["pl_orourke"]
    err = r * np.hypot(table["sigma_framework"] / table["pl_framework"], table["sigma_orourke"] / table["pl_orourke"])
    w = err ** -2
    print(f"pl ratio weighted mean (framework/orourke) = {(w * r).sum() / w.sum():.4f} ± {w.sum() ** -0.5:.4f}")


def main():
    table = pl_zscores()
    table.assign(deviation=table["deviation"].map("{:.6f}".format)).to_csv(OUT, index=False)
    print_normality(table["deviation"])
    print_pl_ratio(table)


if __name__ == "__main__":
    main()
