import pandas as pd
from pathlib import Path
from ..config import Config
from typing import Hashable
from ..sweep.run import wilson_interval
import numpy as np
import matplotlib.pyplot as plt


def render_one_sweep(samples: pd.DataFrame, file: Path, config: Config):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=600, sharey=True)

    code = samples.iloc[0]["code"]
    basis = samples.iloc[0]["basis"]
    title = f"Logical Error Rate vs Physical Error Rate for {code} with {basis} Memory"

    if len(config.noise.params.keys()) > 0:
        param_names = config.noise.params.keys()
        params = dict()
        for param_name in param_names:
            param_value = samples.iloc[0][param_name]
            params[param_name] = param_value
        title += "\n(" + ", ".join(f"{key} = {value}" for key, value in params.items()) + ")"

    for d, d_samples in samples.groupby("d"):
        sorted_samples = d_samples.sort_values("p")

        ps = sorted_samples["p"].to_numpy()
        pls = sorted_samples["pl"].to_numpy()
        errs = sorted_samples["errors"].to_numpy()
        shots = sorted_samples["shots"].to_numpy()
        bounds = np.array([wilson_interval(e, s, z=1.0) for e, s in zip(errs, shots)]).reshape(-1, 2)
        lows, highs = bounds[:, 0], bounds[:, 1]

        measured = errs > 0
        zero = ~measured

        # Measured points: connect with a line and show Wilson error bars
        if np.any(measured):
            ax.errorbar(
                ps[measured], pls[measured],
                yerr=[pls[measured] - lows[measured], highs[measured] - pls[measured]],
                marker="o", linestyle="-", capsize=3,
                label=f"d = {d}",
            )

        # Zero-failure points: plot the Wilson upper bound as a downward arrow
        if np.any(zero):
            ax.errorbar(
                ps[zero], highs[zero],
                yerr=highs[zero] * 0.5, uplims=True,
                marker='', linestyle='none',
                label=f"d = {d}"
            )

    fig.suptitle(title)
    ax.set_xscale('linear')
    ax.set_yscale('log')
    ax.set_xlabel('Physical Error Rate')
    ax.set_ylabel('Logical Error Rate (error bars: 1σ Wilson)')
    ax.grid(True, which="both", alpha=0.5)
    ax.legend()

    fig.savefig(str(file))
    plt.close(fig)


def make_figure_tag(key: list[Hashable]) -> str:
    tag = ""
    for value in key:
        tag += f"_{str(value)}"
    return tag


def render_all_sweeps(config: Config):
    sample_path = config.output.path / "samples.csv"
    samples = pd.read_csv(sample_path)

    figures_dir = config.output.path / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    group_columns = ["code", "basis", *config.noise.params.keys()]
    for key, group_samples in samples.groupby(group_columns):
        tag = make_figure_tag(key)
        path = figures_dir / f"result{tag}.pdf"
        render_one_sweep(group_samples, path, config)
