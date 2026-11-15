from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

RESULTS = Path(__file__).parent / "results"
STATS = RESULTS / "stats.txt"
CRIGER2018_P_TH = 14.95, 0.02  # %, Fig. 7 (top): 9.97 ± 0.01% at q, converted to p = 1.5q


def pl_pulls():
    # each series' pl against the weighted mean of the six at the same (p, d), as a z score
    df = pd.read_csv(RESULTS / "samples.csv")
    df = df[df["sweep_id"] == "threshold_sweep"]
    w = df["sigma"] ** -2
    g = df.assign(w=w, wx=w * df["pl"]).groupby(["p", "d"])
    w_sum = g["w"].transform("sum")
    mean, mean_err = g["wx"].transform("sum") / w_sum, w_sum ** -0.5
    return (df["pl"] - mean) / (df["sigma"] ** 2 - mean_err ** 2) ** 0.5


def print_normality(z):
    n = len(z)
    for k in (1, 2):
        inside = int((z.abs() <= k).sum())
        print(f"{k}σ: {inside}/{n} ({inside / n:.1%}), N(0,1): {norm.cdf(k) - norm.cdf(-k):.1%}")
    # the largest |z|, next to the median of the largest |z| among n draws from N(0,1)
    print(f"max |z|: {z.abs().max():.1f}σ, N(0,1) median: {norm.ppf((1 + 0.5 ** (1 / n)) / 2):.1f}σ")


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


def main():
    with STATS.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print_normality(pl_pulls())
        print()
        mean, mean_err = print_threshold_pulls()
        print()
        print_criger2018_diff(mean, mean_err)
    print(f"wrote {STATS.relative_to(RESULTS.parent)}")


if __name__ == "__main__":
    main()
