# Usage:
# python case_studies/r1_regular_deformations/summarize_screen.py case_studies/r1_regular_deformations/config_screen_eta100.yaml

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from cdsc.config import ConfigError, load_config

REFERENCE = "xzzx"
# Listed whatever their rank
BUILTIN_CODES = ("rotated_surface", "xzzx", "xy")


def load_screen(config_path: str) -> tuple[pd.DataFrame, Path]:
    # One row per code, distance and basis, from the config's samples.csv, and the config's output dir
    config = load_config(Path(config_path))
    samples = pd.read_csv(config.output.path / "samples.csv")
    if samples["eta"].nunique() != 1 or samples["p"].nunique() != 1:
        raise ValueError(f"{config_path}: a screen config has one eta and one p")
    if REFERENCE not in set(samples["code"]):
        raise ValueError(f"{config_path}: no {REFERENCE} in the screen to compare against")
    return samples, config.output.path


def per_distance(samples: pd.DataFrame) -> pd.DataFrame:
    # Both bases side by side, the worse basis, and the ratio to XZZX at the same distance
    wide = samples.pivot_table(index=["eta", "p", "code", "d"], columns="basis", values="pl")
    wide.columns = [f"pl_{basis}" for basis in wide.columns]
    wide = wide.reset_index()
    x_worse = wide["pl_X"] >= wide["pl_Z"]
    wide["worse_basis"] = np.where(x_worse, "X", "Z")
    wide["pl_worse"] = np.where(x_worse, wide["pl_X"], wide["pl_Z"])

    reference = wide[wide["code"] == REFERENCE].set_index("d")["pl_worse"]
    wide["xzzx_pl_worse"] = wide["d"].map(reference)
    wide["ratio_vs_xzzx"] = wide["xzzx_pl_worse"] / wide["pl_worse"].replace(0.0, np.nan)
    # The smallest ratio over the distances; a code with no errors at some d has no finite ratio there, so that d is left out
    wide["ratio_min"] = wide.groupby("code")["ratio_vs_xzzx"].transform(lambda r: r.fillna(np.inf).min())
    return wide


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank an R1 screen against XZZX.")
    parser.add_argument("config", help="a screen config whose `cdsc run` has finished")
    parser.add_argument("--out", help="summary CSV (default: screen_summary.csv in the config's output dir)")
    parser.add_argument("--top", type=int, default=10, help="codes listed (default: 10)")
    args = parser.parse_args()

    try:
        samples, output_dir = load_screen(args.config)
    except (ConfigError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    # Highest ratio_min first; ties by name, so the order is reproducible
    table = per_distance(samples).sort_values(["ratio_min", "code", "d"], ascending=[False, True, True],
                                              ignore_index=True)
    out = Path(args.out) if args.out else output_dir / "screen_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False)

    distances = sorted(int(d) for d in table["d"].unique())
    ranking = table.drop_duplicates("code").reset_index(drop=True)
    reference = table[table["code"] == REFERENCE].set_index("d")["pl_worse"].sort_index()
    print(f"eta = {table['eta'].iloc[0]}, p = {table['p'].iloc[0]}: {len(ranking)} codes; "
          f"xzzx p_L (worse basis) " + ", ".join(f"d={d}: {pl:.2e}" for d, pl in reference.items()))
    print(f"  {'rank':>4}  {'code':16}" + "  ".join(f"ratio d={d:<3}" for d in distances) + f"  {'ratio_min':>11}")
    shown = list(ranking.index[:args.top]) + [i for i in ranking.index[args.top:]
                                              if ranking.loc[i, "code"] in BUILTIN_CODES]
    for i in shown:
        code = ranking.loc[i, "code"]
        rows = table[table["code"] == code].set_index("d")
        # A code with no errors at some d has no finite ratio there
        ratios = "  ".join(f"{rows.loc[d, 'ratio_vs_xzzx']:>11.2f}" if pd.notna(rows.loc[d, "ratio_vs_xzzx"])
                           else f"{'no errors':>11}" for d in distances)
        print(f"  {i + 1:>4}  {code:16}{ratios}  {ranking.loc[i, 'ratio_min']:>11.2f}")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
