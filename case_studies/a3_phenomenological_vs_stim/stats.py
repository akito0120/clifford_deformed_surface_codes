from pathlib import Path
import pandas as pd
from scipy.stats import chi2

RESULTS = Path(__file__).parent / "results"


def weighted_mean_and_chi2(x, err):
    w = err ** -2
    mean = (w * x).sum() / w.sum()
    chisq = (w * (x - mean) ** 2).sum()
    dof = len(x) - 1
    return pd.Series({"mean": mean, "err": w.sum() ** -0.5,
                      "chi2": chisq, "dof": dof, "p_value": chi2.sf(chisq, dof)})


def load(name):
    return pd.concat([pd.read_csv(RESULTS / s / name).assign(source=s) for s in ["framework", "stim"]])


def print_total(table):
    total, dof = table["chi2"].sum(), table["dof"].sum()
    print(f"total chi2/dof = {total:.2f}/{dof}, p-value = {chi2.sf(total, dof):.3f}")


def p_th_weighted_mean_and_chi2():
    df = load("threshold.csv")
    r = weighted_mean_and_chi2(df["p_th"], df["p_th_err"])
    print(f"p_th = {r['mean']:.6f} ± {r['err']:.6f}")
    print(f"chi2/dof = {r['chi2']:.2f}/{r['dof']:.0f}, p-value = {r['p_value']:.3f}")


def pl_weighted_mean_and_chi2():
    df = load("samples.csv")
    df = df[df["sweep_id"] == "threshold_sweep"]
    table = df.groupby(["basis", "d", "p"]).apply(
        lambda g: weighted_mean_and_chi2(g["pl"], g["sigma"]), include_groups=False
    ).astype({"dof": int})
    print(table.to_string())
    print_total(table)


def pl_ratio_weighted_mean_and_chi2():
    df = load("samples.csv")
    df = df[df["sweep_id"] == "threshold_sweep"]
    t = df.pivot(index=["basis", "d", "p"], columns="source", values=["pl", "sigma"])
    r = t["pl", "framework"] / t["pl", "stim"]
    err = r * ((t["sigma"] / t["pl"]) ** 2).sum(axis=1) ** 0.5
    s = weighted_mean_and_chi2(r, err)
    print(f"pl ratio (framework/stim) = {s['mean']:.4f} ± {s['err']:.4f}")


def main():
    p_th_weighted_mean_and_chi2()
    pl_weighted_mean_and_chi2()
    pl_ratio_weighted_mean_and_chi2()

if __name__ == "__main__":
    main()
