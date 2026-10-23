from dataclasses import replace

from cdsc.noise.builtin import depolarizing_noise
from cdsc.noise.registry import register_noise


@register_noise("depolarizing_sd")
def depolarizing_sd_noise(p, params):
    # The built-in depolarizing noise, with measurement flips at p xor 2p/3 = 5p/3 - 4p^2/3 instead of p.
    # The extra 2p/3 is the depolarizing error after the second Hadamard of the SD circuits in O'Rourke & Devitt (2025):
    # it only flips the ancilla's measurement. The final data readout gets the same flip, which they do not have.
    return replace(depolarizing_noise(p, params), meas_flip=p + 2 * p / 3 - 2 * p * (2 * p / 3))
