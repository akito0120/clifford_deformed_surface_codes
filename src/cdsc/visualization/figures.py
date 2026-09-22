import pandas as pd
from pathlib import Path
from ..config import Config
from typing import Hashable
from ..sweep.run import wilson_interval
import numpy as np
import matplotlib.pyplot as plt


def render_one_sweep(
    samples: pd.DataFrame, 
    file: Path, 
    config: Config, 
    p_th: float,
    p_th_err: float
):

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

    n_dist = samples["d"].nunique()
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, n_dist + 1)).tolist()

    for (d, d_samples), color in zip(samples.groupby("d"), colors):
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
                color=color
            )

        # Zero-failure points: plot the Wilson upper bound as a downward arrow
        if np.any(zero):
            ax.errorbar(
                ps[zero], highs[zero],
                yerr=highs[zero] * 0.5, uplims=True,
                marker='', linestyle='none',
                label=None if np.any(measured) else f"d = {d}",
                color=color
            )

    ax.axvline(
        x=p_th, linestyle="--", 
        label=f"{code} p_th = {p_th:.6f} ± {p_th_err:.6f}", color=colors[n_dist]
    )
    # ax.axvspan(p_th - p_th_err, p_th + p_th_err, alpha=0.1, color=colors[n_dist])

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
    samples = samples[samples["sweep_id"] == config.threshold.source_sweep]

    threshold_path = config.output.path / "threshold.csv"
    thresholds = pd.read_csv(threshold_path)

    figures_dir = config.output.path / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    group_columns = ["code", "basis", *config.noise.params.keys()]
    for key, group_samples in samples.groupby(group_columns):
        tag = make_figure_tag(key)
        path = figures_dir / f"threshold{tag}.pdf"

        key_dict = dict(zip(group_columns, key))
        threshold = thresholds.loc[thresholds[list(key_dict)].eq(pd.Series(key_dict)).all(axis=1)].iloc[0]

        render_one_sweep(group_samples, path, config, threshold["p_th"], threshold["p_th_err"])


def render_one_suppression(
    samples: pd.DataFrame,
    suppressions: pd.DataFrame,
    target_pl: float,
    file: Path
):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=600, sharey=True)

    code = samples.iloc[0]["code"]
    basis = samples.iloc[0]["basis"]
    title = f"Distance vs Per-Round Logical Error Rate for {code} with {basis} Memory"

    for p, p_samples in samples.groupby("p"):
        sorted_samples = p_samples.sort_values("d")

        pls = sorted_samples["pl"].to_numpy()
        ds = sorted_samples["d"].to_numpy()
        errs = sorted_samples["errors"].to_numpy()
        shots = sorted_samples["shots"].to_numpy()
        bounds = np.array([wilson_interval(e, s, z=1.0) for e, s in zip(errs, shots)]).reshape(-1, 2)
        lows, highs = bounds[:, 0], bounds[:, 1]

        fits = suppressions[np.isclose(suppressions["p"], p)]
        fit = fits.iloc[0]
        label = f"p = {p}: d* = {fit['d_star']:.1f} -> d = {fit['d_teraquop']} ({fit['qubits']} qubits)"

        container = ax.errorbar(
            ds, pls / ds,
            yerr=[(pls - lows) / ds, (highs - pls) / ds],
            marker="o", linestyle="none", capsize=3,
            label=label,
        )

        color = container[0].get_color()
        observed = ds[errs > 0]
        d_fit = np.linspace(observed.min(), observed.max(), 50)
        d_ext = np.linspace(observed.max(), fit["d_star"], 50)
        ax.plot(d_fit, 10 ** (fit["intercept"] + fit["slope"] * d_fit), linestyle="-", color=color)
        ax.plot(d_ext, 10 ** (fit["intercept"] + fit["slope"] * d_ext), linestyle="--", color=color)
        ax.plot(fit["d_star"], target_pl, marker="*", markersize=12, linestyle="none", color=color)

    ax.axhline(target_pl, linestyle=":", color="black", label=f"target = {target_pl:g}")

    fig.suptitle(title)
    ax.set_xscale('linear')
    ax.set_yscale('log')
    ax.set_xlabel('Code Distance')
    ax.set_ylabel('Per-Round Logical Error Rate (error bars: 1σ Wilson)')
    ax.grid(True, which="both", alpha=0.5)
    ax.legend()

    fig.savefig(str(file))
    plt.close(fig)


def render_all_suppressions(config: Config):
    sample_path = config.output.path / "samples.csv"
    samples = pd.read_csv(sample_path)
    samples = samples[samples["sweep_id"] == config.suppression.source_sweep]

    suppression_path = config.output.path / "suppression.csv"
    suppressions = pd.read_csv(suppression_path)

    figures_dir = config.output.path / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    group_columns = ["code", "basis", *config.noise.params.keys()]
    for key, group_samples in samples.groupby(group_columns):
        tag = make_figure_tag(key)
        path = figures_dir / f"suppression{tag}.pdf"

        key_dict = dict(zip(group_columns, key))
        group_suppressions = suppressions.loc[suppressions[list(key_dict)].eq(pd.Series(key_dict)).all(axis=1)]

        render_one_suppression(group_samples, group_suppressions, config.suppression.target_pl, path)
