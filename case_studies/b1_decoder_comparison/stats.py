from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd

from cdsc.config import load_config

HERE = Path(__file__).parent
RESULTS = HERE / "results"
STATS = RESULTS / "stats.txt"
DECODERS = ("bp", "uf")
# the MWPM threshold under the same noise; for depolarizing noise it is A1's run
MWPM = {
    "depolarizing": HERE.parent / "a1_code_capacity_depolarizing" / "results" / "threshold.csv",
    "dephasing": RESULTS / "dephasing_mwpm" / "threshold.csv",
}


def print_mwpm_ratios(noise):
    # p_th(decoder) / p_th(MWPM) under the same noise, code and basis, with the relative errors added in quadrature
    mwpm = pd.read_csv(MWPM[noise])
    for decoder in DECODERS:
        t = pd.read_csv(RESULTS / f"{noise}_{decoder}" / "threshold.csv").merge(
            mwpm, on=["code", "basis"], suffixes=("", "_mwpm"))
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
