from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2, kstest, norm, pearsonr, ttest_1samp

from cdsc.config import load_config

HERE = Path(__file__).parent
RESULTS = HERE / "results"
OUT = RESULTS / "stim_zscore.csv"
STATS = RESULTS / "stats.txt"
CONFIGS = {"framework": HERE / "config_framework.yaml", "stim": HERE / "config_stim.yaml"}


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
    # the largest |z|, next to the median of the largest |z| among n draws from N(0,1)
    print(f"max |z|: {z.abs().max():.1f}σ, N(0,1) median: {norm.ppf((1 + 0.5 ** (1 / n)) / 2):.1f}σ")
    # one-sample t-test of the mean of the signed z against 0, with the standard error s/sqrt(n) from the sample
    print(f"mean z: {z.mean():+.2f} ± {z.sem():.2f}, t-test p-value = {ttest_1samp(z, 0).pvalue:.2f}")
    # sum of z^2 against chi^2 with n degrees of freedom: nothing is fitted to the deviations
    c = (z ** 2).sum()
    print(f"chi2/dof: {c:.1f}/{n} = {c / n:.2f}, chi2-test p-value = {chi2.sf(c, n):.2f}")
    # Kolmogorov-Smirnov test against N(0,1): D is the largest gap between the empirical CDF of z and Φ
    ks = kstest(z, "norm")
    print(f"KS D: {ks.statistic:.2f}, ks-test p-value = {ks.pvalue:#.2g}")


def print_trend(table):
    # Pearson correlation of the deviation with p and with d: a trend, unlike the mean offset,
    # would point to a p- or d-dependent difference between the two circuits
    for var in ("p", "d"):
        r = pearsonr(table[var], table["deviation"])
        print(f"deviation vs {var}: r = {r.statistic:+.2f}, pearson-test p-value = {r.pvalue:.2f}")


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


def print_shot_budget():
    # total shots per config and sweep, and the points that stopped at max_shots, with their fewest errors
    for name, path in CONFIGS.items():
        config = load_config(path)
        max_shots = config.sampling.max_shots
        df = pd.read_csv(config.output.path / "samples.csv")
        for sweep, g in df.groupby("sweep_id", sort=False):
            capped = g[g["shots"] >= max_shots]
            line = f"{name} {sweep}: {g['shots'].sum():,} shots, {len(capped)}/{len(g)} points stopped at max_shots = {max_shots:,}"
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
        print_threshold_pulls()
        print()
        print_shot_budget()
    print(f"wrote {OUT.relative_to(RESULTS.parent)} and {STATS.relative_to(RESULTS.parent)}")


if __name__ == "__main__":
    main()
