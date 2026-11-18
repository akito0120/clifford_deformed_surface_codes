from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd

from cdsc.config import load_config
from cdsc.noise.builtin import biased_pauli_rates

HERE = Path(__file__).parent
RESULTS = HERE / "results"
STATS = RESULTS / "stats.txt"
CONFIGS = {"css": HERE / "config_css.yaml", "xzzx": HERE / "config_xzzx.yaml"}
WANG2003_Q_TH = 2.93, 0.02 # %, as q = p_Y + p_Z; Wang2003 abstract: p_c0 = .0293 ± .0002
DEPOLARIZING_ETA = 0.5  # p_X = p_Y = p_Z, where the XZZX code is a Clifford deformation of the CSS code


def q_per_p(th):
    # q = p_Y + p_Z per unit p at each eta: the measurement flip rate of biased_meas_yz, and the X memory's data error rate
    return th["eta"].map(lambda eta: sum(biased_pauli_rates(1.0, eta)[1:]))


def print_wang2003_diff(th):
    # p_th - Wang2003's q_th converted to p, in percentage points and in units of the combined sigma
    paper, paper_err = WANG2003_Q_TH
    to_p = 1 / q_per_p(th)
    dp, e = 100 * th["p_th"] - paper * to_p, np.hypot(100 * th["p_th_err"], paper_err * to_p)
    for eta, d, ei in zip(th["eta"], dp, e):
        print(f"p_th eta={eta:g} css - wang2003 = {d:+.3f} ± {ei:.3f} points ({d / ei:+.1f}σ)")


def campos2026_diff(th):
    # p_th - Campos2026 Fig. 6 (CSS (a), XZZX (b)), in percentage points and the combined sigma, at the eta both have
    t = th.merge(pd.read_csv(HERE / "Campos2026_fig6_l2.csv"), on=["code", "eta"])
    return t, 100 * (t["p_th"] - t["pth"]), 100 * np.hypot(t["p_th_err"], t["err_approx"])


def print_campos2026_diff(th):
    t, dp, e = campos2026_diff(th)
    for eta, d, ei in zip(t["eta"], dp, e):
        print(f"p_th eta={eta:g} css - campos2026 = {d:+.3f} ± {ei:.3f} points ({d / ei:+.1f}σ)")


def print_q_threshold_pulls(th):
    # each p_th as q = p_Y + p_Z, against the weighted mean of the six, in percentage points and as a z score
    # (sigma_i^2 - sigma_mean^2 removes q_i's share of the mean)
    to_q = q_per_p(th)
    x, e = 100 * th["p_th"] * to_q, 100 * th["p_th_err"] * to_q
    w = e ** -2
    mean, mean_err = (w * x).sum() / w.sum(), w.sum() ** -0.5
    print(f"q_th weighted mean = {mean:.4f} ± {mean_err:.4f}%")
    for eta, xi, ei in zip(th["eta"], x, e):
        d = xi - mean
        print(f"q_th eta={eta:g} css - mean = {d:+.4f} points ({d / (ei ** 2 - mean_err ** 2) ** 0.5:+.1f}σ)")


def print_depolarizing_pulls(css):
    # at eta = 0.5, the CSS threshold and the two XZZX ones against their weighted mean, in percentage points and as a z score
    th = pd.concat([css, pd.read_csv(RESULTS / "xzzx" / "threshold.csv")])
    th = th[th["eta"] == DEPOLARIZING_ETA]
    x, e = 100 * th["p_th"], 100 * th["p_th_err"]
    w = e ** -2
    mean, mean_err = (w * x).sum() / w.sum(), w.sum() ** -0.5
    print(f"p_th eta={DEPOLARIZING_ETA:g} weighted mean = {mean:.3f} ± {mean_err:.3f}%")
    for code, basis, xi, ei in zip(th["code"], th["basis"], x, e):
        d = xi - mean
        print(f"p_th eta={DEPOLARIZING_ETA:g} {code} {basis} - mean = {d:+.3f} points ({d / (ei ** 2 - mean_err ** 2) ** 0.5:+.1f}σ)")


def print_xzzx_basis_diff():
    # XZZX p_th(X memory) - p_th(Z memory) per eta, in percentage points and in units of the combined sigma
    th = pd.read_csv(RESULTS / "xzzx" / "threshold.csv")
    t = th[th["basis"] == "X"].merge(th[th["basis"] == "Z"], on=["code", "eta"], suffixes=("_x", "_z"))
    dp, e = 100 * (t["p_th_x"] - t["p_th_z"]), 100 * np.hypot(t["p_th_err_x"], t["p_th_err_z"])
    for eta, d, ei in zip(t["eta"], dp, e):
        print(f"p_th eta={eta:g} xzzx X - xzzx Z = {d:+.3f} ± {ei:.3f} points ({d / ei:+.1f}σ)")


def print_xzzx_campos2026_diff(side):
    # one of the two XZZX bases per eta against Campos2026: "lower", as Campos2026 counts a failure of either logical, or "higher"
    th = pd.read_csv(RESULTS / "xzzx" / "threshold.csv")
    th = th.loc[th.groupby("eta")["p_th"].agg({"lower": "idxmin", "higher": "idxmax"}[side])]
    t, dp, e = campos2026_diff(th)
    for eta, d, ei in zip(t["eta"], dp, e):
        print(f"p_th eta={eta:g} xzzx {side} - campos2026 = {d:+.3f} ± {ei:.3f} points ({d / ei:+.1f}σ)")


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
    th = pd.read_csv(RESULTS / "css" / "threshold.csv")
    with STATS.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print_wang2003_diff(th)
        print()
        print_campos2026_diff(th)
        print()
        print_q_threshold_pulls(th)
        print()
        print_depolarizing_pulls(th)
        print()
        print_xzzx_basis_diff()
        print()
        print_xzzx_campos2026_diff("lower")
        print()
        print_xzzx_campos2026_diff("higher")
        print()
        print_shot_budget()
    print(f"wrote {STATS.relative_to(HERE)}")


if __name__ == "__main__":
    main()
