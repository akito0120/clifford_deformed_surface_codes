from dataclasses import replace

from cdsc.noise.builtin import biased_noise, biased_pauli_rates
from cdsc.noise.registry import register_noise


@register_noise("biased_meas_yz", required_params=("eta",))
def biased_meas_yz_noise(p, params):
    # The built-in biased noise, with measurement flips at p_Y + p_Z = p(2 eta + 1)/(2(1 + eta)) instead of p.
    # This is the measurement error of BonillaAtaides2021 (q = p_hr + p_lr) and of Campos2026 for l = 2 (p_m = p_y + p_z).
    # At eta = inf it is p.
    _, py, pz = biased_pauli_rates(p, params["eta"])
    return replace(biased_noise(p, params), meas_flip=py + pz)
