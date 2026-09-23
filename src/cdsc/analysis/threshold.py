from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2
import pandas as pd
from ..config import Config
from typing import Any


@dataclass(frozen=True)
class ThresholdFitResult:
    p_th: float
    p_th_err: float
    nu: float
    a: float
    b: float
    c: float
    chi2_red: float
    p_value: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "p_th": self.p_th,
            "p_th_err": self.p_th_err,
            "nu": self.nu,
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "chi2_red": self.chi2_red,
            "p_value": self.p_value
        }


def fss(X, p_th, nu, a, b, c):
    p, d = X
    x = (p - p_th) * d ** (1.0 / nu)
    return a + (b * x) + (c * x * x)


def crossing_seed(samples: pd.DataFrame):
    piv = samples.pivot_table(index="p", columns="d", values="pl").dropna()
    return float(piv.std(axis=1).idxmin())


def estimate_threshold(
    samples: pd.DataFrame,
    distances: list[int],
    x_window: float,
    nu_0: float
) -> ThresholdFitResult:
    
    ps = samples["p"].to_numpy()
    ds = samples["d"].to_numpy()
    pls = samples["pl"].to_numpy()
    sigs = samples["sigma"].to_numpy()
    shots = samples["shots"].to_numpy()

    keep = np.isin(ds, distances)
    ps, ds, pls, sigs, shots = ps[keep], ds[keep], pls[keep], sigs[keep], shots[keep]

    lower = [0.0, 1.0, -np.inf, -np.inf, -np.inf]
    upper = [1.0, 2.0, np.inf, np.inf, np.inf]
    bounds = (lower, upper)

    p_th_0 = crossing_seed(samples[samples["d"].isin(distances)])

    x_abs = np.abs((ps - p_th_0) * ds ** (1.0 / nu_0))
    in_win = x_abs <= x_window
    ps, ds, pls, sigs, shots = ps[in_win], ds[in_win], pls[in_win], sigs[in_win], shots[in_win]

    popt, pcov = curve_fit(
        fss, (ps, ds), pls, sigma=sigs, 
        p0=[p_th_0, nu_0, np.median(pls), 0.0, 0.0], 
        maxfev=50000, absolute_sigma=True, bounds=bounds
    )
    
    # Reduced chi-square
    resid = (pls - fss((ps, ds), *popt)) / sigs
    dof = max(len(pls) - len(popt), 1)
    chi2_red = float(np.sum(resid ** 2) / dof)
    p_value = chi2.sf(chi2_red * dof, dof)

    # 1-sigma error on p_th from the fit covariance
    p_th_err = float(np.sqrt(pcov[0][0]))

    return ThresholdFitResult(
        p_th=popt[0],
        p_th_err=p_th_err,
        nu=popt[1],
        a=popt[2], b=popt[3], c=popt[4], 
        chi2_red=chi2_red,
        p_value=p_value,
    )


def estimate_all_thresholds(config: Config) -> pd.DataFrame:
    sample_path = config.output.path / "samples.csv"
    samples = pd.read_csv(sample_path)
    samples = samples[samples["sweep_id"] == config.threshold.source_sweep]

    rows = list()

    group_columns = ["code", "basis", *config.noise.params.keys()]
    for key, group_samples in samples.groupby(group_columns):
        key_dict = dict(zip(group_columns, key))
        fit_result = estimate_threshold(
            samples=group_samples,
            distances=config.threshold.distances,
            nu_0=config.threshold.nu_0,
            x_window=config.threshold.x_window
        )
        rows.append({
            **key_dict,
            **fit_result.as_dict(),
        })

    return pd.DataFrame(rows)
