import numpy as np
import sinter
from scipy.optimize import brentq
from ..codes.definition import CodeDefinition
from ..codes.registry import build_code
from dataclasses import dataclass
import pandas as pd
from ..config import Config
from typing import Any


def physical_qubits(code: CodeDefinition) -> int:
    return len(code.data_qubits) + len(code.ancilla_qubits)


@dataclass(frozen=True)
class SuppressionFitResult:
    slope: float
    intercept: float
    d_star: float
    d_teraquop: int
    qubits: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "slope": self.slope,
            "intercept": self.intercept,
            "d_star": self.d_star,
            "d_teraquop": self.d_teraquop,
            "qubits": self.qubits
        }


def estimate_suppression(
    samples: pd.DataFrame,
    code: str,
    target_pl: float,
) -> SuppressionFitResult:
    d = samples["d"].to_numpy(dtype=float)
    pl = samples["pl"].to_numpy(dtype=float)
    sig = samples["sigma"].to_numpy(dtype=float)
    eps = np.array([
        sinter.shot_error_rate_to_piece_error_rate(p, pieces=r) 
        for p, r in zip(pl, d)
    ])
    log_eps = np.log10(eps)
    sig_eps = sig * (1.0 - 2.0 * pl) ** (1.0 / d - 1.0) / d
    sig_log_eps = sig_eps / (eps * np.log(10.0))

    slope, intercept = np.polyfit(d, log_eps, 1, w=1.0 / sig_log_eps)
    if slope >= 0:
        raise ValueError(f"code {code!r}: non-negative slope {slope}; no suppression to extrapolate")

    # target_pl is per d rounds: find the d where the fitted per-round rate meets its per-round equivalent
    def excess(x: float) -> float:
        target_eps = sinter.shot_error_rate_to_piece_error_rate(target_pl, pieces=float(x))
        return intercept + slope * x - np.log10(target_eps)

    upper = max((np.log10(target_pl) - intercept) / slope, 2.0)
    while excess(upper) > 0:
        upper *= 2.0
    d_star = brentq(excess, 1.0, upper)

    d_teraquop = int(np.ceil(d_star))
    if d_teraquop % 2 == 0:
        d_teraquop += 1

    return SuppressionFitResult(
        slope=float(slope),
        intercept=float(intercept),
        d_star=float(d_star),
        d_teraquop=d_teraquop,
        qubits=physical_qubits(build_code(code, distance=d_teraquop))
    )


def estimate_all_suppressions(config: Config) -> pd.DataFrame:
    sample_path = config.output.path / "samples.csv"
    samples = pd.read_csv(sample_path)
    samples = samples[samples["sweep_id"] == config.suppression.source_sweep]
    samples = samples[samples["errors"] > 0]

    rows = list()

    group_columns = ["code", "basis", *config.noise.params.keys(), "p"]
    for key, group_samples in samples.groupby(group_columns):
        key_dict = dict(zip(group_columns, key))
        result = estimate_suppression(
            group_samples, key_dict["code"],
            config.suppression.target_pl
        )
        rows.append({
            **key_dict,
            **result.as_dict()
        })

    return pd.DataFrame(rows)
