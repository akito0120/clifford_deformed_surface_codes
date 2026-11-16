from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd

from cdsc.analysis.threshold import estimate_all_thresholds
from cdsc.config import load_config

HERE = Path(__file__).parent
RESULTS = HERE / "results"
STATS = RESULTS / "stats.txt"
DECODERS = ("bp", "uf")
A1_CONFIG = HERE.parent / "a1_code_capacity_depolarizing" / "config.yaml"


def mwpm_thresholds(noise):
    # the MWPM threshold under the same noise, fit on the same distances as B1
    if noise == "dephasing":
        return pd.read_csv(RESULTS / "dephasing_mwpm" / "threshold.csv")
    # for depolarizing noise it is A1's run, whose threshold.csv fits d = 7-23:
    # refit its samples on B1's distances here, without writing to A1's results
    config = load_config(A1_CONFIG)
    config.threshold.distances = load_config(HERE / "config_depolarizing_bp.yaml").threshold.distances
    return estimate_all_thresholds(config)


def print_mwpm_ratios(noise):
    # p_th(decoder) / p_th(MWPM) under the same noise, code and basis, with the relative errors added in quadrature
    mwpm = mwpm_thresholds(noise)
    for decoder in DECODERS:
        t = pd.read_csv(RESULTS / f"{noise}_{decoder}" / "threshold.csv").merge(
            mwpm, on=["code", "basis"], suffixes=("", "_mwpm"))
        if decoder == DECODERS[0]:
            for row in t.itertuples():
                print(f"p_th {noise} mwpm {row.code} {row.basis} = {row.p_th_mwpm:.5f} ± {row.p_th_err_mwpm:.5f}, "
                      f"nu = {row.nu_mwpm:.2f}, chi2_red = {row.chi2_red_mwpm:.2f}")
        r = t["p_th"] / t["p_th_mwpm"]
        err = r * np.hypot(t["p_th_err"] / t["p_th"], t["p_th_err_mwpm"] / t["p_th_mwpm"])
        for ri, ei in zip(r, err):
            print(f"p_th {noise} {decoder} / mwpm = {ri:.3f} ± {ei:.3f}")


def print_shot_budget():
    # total shots per config and sweep, and the points that stopped at max_shots, with their fewest errors
    for path in sorted(HERE.glob("config_*.yaml")):
        name = path.stem.removeprefix("config_")
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
    with STATS.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print_mwpm_ratios("depolarizing")
        print()
        print_mwpm_ratios("dephasing")
        print()
        print_shot_budget()
    print(f"wrote {STATS.relative_to(HERE)}")


if __name__ == "__main__":
    main()
