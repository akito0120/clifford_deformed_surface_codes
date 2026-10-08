from cdsc.noise.builtin import biased_noise
from cdsc.noise.registry import register_noise


@register_noise("dephasing")
def dephasing_noise(p, params):
    # Pure Z noise: the biased noise at infinite bias
    return biased_noise(p, {"eta": float("inf")})
