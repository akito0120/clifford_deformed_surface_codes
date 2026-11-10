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


def p_th_weighted_mean_and_chi2():
    df = pd.read_csv(RESULTS / "threshold.csv")
    r = weighted_mean_and_chi2(df["p_th"], df["p_th_err"])
    print(f"p_th = {r['mean']:.6f} ± {r['err']:.6f}")
    print(f"chi2/dof = {r['chi2']:.2f}/{r['dof']:.0f}, p-value = {r['p_value']:.3f}")


def pl_weighted_mean_and_chi2():
    df = pd.read_csv(RESULTS / "samples.csv")
    df = df[df["sweep_id"] == "threshold_sweep"]
    table = df.groupby(["d", "p"]).apply(
        lambda g: weighted_mean_and_chi2(g["pl"], g["sigma"]), include_groups=False
    ).astype({"dof": int})
    print(table.to_string())
    total, dof = table["chi2"].sum(), table["dof"].sum()
    print(f"total chi2/dof = {total:.2f}/{dof}, p-value = {chi2.sf(total, dof):.3f}")


def main():
    p_th_weighted_mean_and_chi2()
    pl_weighted_mean_and_chi2()

if __name__ == "__main__":
    main()
