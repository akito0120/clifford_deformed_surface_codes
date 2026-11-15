from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2, kstest, norm, ttest_1samp

from cdsc.config import load_config

RESULTS = Path(__file__).parent / "results"
STATS = RESULTS / "stats.txt"
CRIGER2018_P_TH = 14.95, 0.02  # %, Fig. 7 (top): 9.97 ± 0.01% at q, converted to p = 1.5q


def pl_pulls():
    # each series' pl against the weighted mean of the six at the same (p, d), as a z score,
    # and chi^2 = sum of ((pl - mean) / sigma)^2, with 6 - 1 degrees of freedom per (p, d)
    df = pd.read_csv(RESULTS / "samples.csv")
    df = df[df["sweep_id"] == "threshold_sweep"]
    w = df["sigma"] ** -2
    g = df.assign(w=w, wx=w * df["pl"]).groupby(["p", "d"])
    w_sum = g["w"].transform("sum")
    mean, mean_err = g["wx"].transform("sum") / w_sum, w_sum ** -0.5
    residual = df["pl"] - mean
    table = df.assign(pull=residual / (df["sigma"] ** 2 - mean_err ** 2) ** 0.5)
    return table, ((residual / df["sigma"]) ** 2).sum(), len(df) - g.ngroups


def print_normality(z, c, dof):
    n = len(z)
    for k in (1, 2):
        inside = int((z.abs() <= k).sum())
        print(f"{k}σ: {inside}/{n} ({inside / n:.1%}), N(0,1): {norm.cdf(k) - norm.cdf(-k):.1%}")
    # the largest |z|, next to the median of the largest |z| among n draws from N(0,1)
    print(f"max |z|: {z.abs().max():.1f}σ, N(0,1) median: {norm.ppf((1 + 0.5 ** (1 / n)) / 2):.1f}σ")
    # chi^2 from the residuals, not the sum of pulls^2: the six pulls at a (p, d) are correlated through their mean
    print(f"chi2/dof: {c:.1f}/{dof} = {c / dof:.2f}, chi2-test p-value = {chi2.sf(c, dof):.2f}")


def print_series_means(table):
    # one-sample t-test of each series' mean pull against 0: the pooled mean is ~0 by construction,
    # but a series sitting above or below the other five shows up in its own mean
    for (code, basis), z in table.groupby(["code", "basis"])["pull"]:
        print(f"mean z {code} {basis}: {z.mean():+.2f} ± {z.sem():.2f}, t-test p-value = {ttest_1samp(z, 0).pvalue:.2f}")


def print_series_ks(table):
    # Kolmogorov-Smirnov test of each series' pulls against N(0,1), per series only: the six pulls at a (p, d)
    # are correlated through their mean, which makes a test on all pulls together far too conservative
    for (code, basis), z in table.groupby(["code", "basis"])["pull"]:
        ks = kstest(z, "norm")
        print(f"KS D {code} {basis}: {ks.statistic:.2f}, ks-test p-value = {ks.pvalue:#.2g}")


def print_threshold_pulls():
    # each p_th against the weighted mean of all six, as a z score (sigma_i^2 - sigma_mean^2 removes x_i's share of the mean)
    th = pd.read_csv(RESULTS / "threshold.csv")
    x, e = 100 * th["p_th"], 100 * th["p_th_err"]
    w = e ** -2
    mean, mean_err = (w * x).sum() / w.sum(), w.sum() ** -0.5
    print(f"p_th weighted mean = {mean:.3f} ± {mean_err:.3f}%")
    for code, basis, xi, ei in zip(th["code"], th["basis"], x, e):
        print(f"p_th {code} {basis} - mean = {(xi - mean) / (ei ** 2 - mean_err ** 2) ** 0.5:+.1f}σ")
    return mean, mean_err


def print_criger2018_diff(mean, mean_err):
    # weighted mean of the six p_th - Criger2018 Fig. 7, in percentage points and in units of the combined sigma
    paper, paper_err = CRIGER2018_P_TH
    dp, e = mean - paper, np.hypot(mean_err, paper_err)
    print(f"p_th weighted mean - criger2018 = {dp:+.3f} ± {e:.3f} points ({dp / e:+.1f}σ)")


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
    with STATS.open("w", encoding="utf-8") as f, redirect_stdout(f):
        table, c, dof = pl_pulls()
        print_normality(table["pull"], c, dof)
        print()
        print_series_means(table)
        print()
        print_series_ks(table)
        print()
        mean, mean_err = print_threshold_pulls()
        print()
        print_criger2018_diff(mean, mean_err)
        print()
        print_shot_budget()
    print(f"wrote {STATS.relative_to(RESULTS.parent)}")


if __name__ == "__main__":
    main()
