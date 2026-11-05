from dataclasses import replace

from cdsc.noise.builtin import biased_noise
from cdsc.noise.registry import register_noise


@register_noise("biased_meas_ratio", required_params=("eta", "meas_ratio"))
def biased_meas_ratio_noise(p, params):
    # The built-in biased noise, with measurement flips at meas_ratio * p instead of p
    return replace(biased_noise(p, params), meas_flip=params["meas_ratio"] * p)
