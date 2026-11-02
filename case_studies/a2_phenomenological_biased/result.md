# A2: Phenomenological threshold against bias

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| BonillaAtaides2021 | J. P. Bonilla Ataides, D. K. Tuckett, S. D. Bartlett, S. T. Flammia and B. J. Brown, "The XZZX surface code" [arXiv:2009.07851](https://arxiv.org/abs/2009.07851) | Fig. 5(e) | CSS reference line p_hr + p_lr = 2.9%. The XZZX threshold rises with η, to about 10% at high bias | Toric d×d code, d rounds with periodic time, measurement flips q = p_hr + p_lr, MWPM, d = 12–20 at finite bias, 3 × 10⁴ samples per point |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Fig. 6, ℓ = 2 | CSS (a): 4.4, 3.2, 3.0, 2.9, 2.9, 2.9%. XZZX (b): 4.4, 5.1, 5.6, 6.3, 6.9, 7.4%. Both at η = 0.5, 5, 10, 25, 50, 100, each ±0.2 points | Rotated code, measurement flips p_Y + p_Z, a perfect last round, PyMatching, quadratic FSS fit, "distances up to 40" |

- **Both papers count a failure of either logical operator.**
  - Campos2026 checks "whether the residual error is trivial" (§Methods).
  - BonillaAtaides2021 also counts a non-trivial cycle along the time axis.
  - The framework counts one memory basis.
- **The CSS reference line is not a simulation.**
  - It is Wang2003's 2.9% for independent flips, written as p_hr + p_lr = 2.9%.
  - In terms of p it is p_th(η) = 2.9% × 2(η + 1)/(2η + 1). That gives 4.350, 3.038, 2.957, 2.929, 2.914 and 2.900% at η = 0.5, 10, 25, 50, 100 and inf.
- Campos2026's values were read from the vector PDF of Fig. 6 in its arXiv source (v3) into [Campos2026_fig6_l2.csv](Campos2026_fig6_l2.csv).
- BonillaAtaides2021's XZZX curve is compared in trend only, because of its periodic boundaries.

## Setup

- Decoder: `mwpm`
- d = 11, 13, 15, 17, 19
- `phenomenological` noise with the plugin `biased_meas_yz` from [noises.py](noises.py)
  - It is the built-in `biased` noise, with measurement flips at p_Y + p_Z instead of p
  - d noisy rounds are followed by a data readout flipped at the same rate. Campos2026 makes its last round perfect instead
- CSS:
  - Config: [config_css.yaml](config_css.yaml)
  - Code: `rotated_surface` with η = 0.5, 10, 25, 50, 100, inf
  - p: 11 points per η around the reference line
  - Bases: X only (The Z memory sees only X and Y errors, at rate p/(1 + η), so its threshold is far higher)
- XZZX:
  - Config: [config_xzzx.yaml](config_xzzx.yaml)
  - Code: `xzzx` with η = 0.5, 10, 25, 50, 100
  - p: 9 points per (η, basis) around a pilot crossing
  - Bases: X and Z (The lower of the two thresholds is compared)


## Result

From [results/css/threshold.csv](results/css/threshold.csv). Difference is (framework − Campos2026) in units of Campos2026's ±0.2-point error bar.

| η | p_th (%) | Reference line (%) | Campos2026 (%) | Difference (error bars) |
|---|---|---|---|---|
| 0.5 | 4.365 ± 0.004 | 4.350 | 4.4 | −0.2 |
| 10 | 3.045 ± 0.003 | 3.038 | 3.0 | +0.2 |
| 25 | 2.969 ± 0.003 | 2.957 | 2.9 | +0.3 |
| 50 | 2.938 ± 0.003 | 2.929 | 2.9 | +0.2 |
| 100 | 2.924 ± 0.003 | 2.914 | 2.9 | +0.1 |
| inf | 2.911 ± 0.003 | 2.900 | — | — |

- Every η is 0.2–0.4% (relative) above the reference line, which is built from the rounded 2.9%.
- In terms of q = p_Y + p_Z, the six thresholds coincide: 2.910 ± 0.001%, with χ² = 1.78 for 5 degrees of freedom.

---

From [results/xzzx/threshold.csv](results/xzzx/threshold.csv). The difference is that of the lower basis, in the same units.

| η | X basis (%) | Z basis (%) | Campos2026 (%) | Difference (error bars) |
|---|---|---|---|---|
| 0.5 | 4.352 ± 0.007 | 4.363 ± 0.007 | 4.4 | −0.2 |
| 10 | 5.784 ± 0.010 | 5.718 ± 0.009 | 5.6 | +0.6 |
| 25 | 6.401 ± 0.011 | 6.288 ± 0.011 | 6.3 | −0.1 |
| 50 | 6.817 ± 0.016 | 6.620 ± 0.013 | 6.9 | −1.4 |
| 100 | 7.081 ± 0.015 | 6.860 ± 0.014 | 7.4 | −2.7 |

- At η = 0.5 the XZZX code agrees with the CSS code point by point: χ² = 20.7 (X basis) and 26.8 (Z basis) for 25 points.

## Verdict

- **Bias dependence: pass.**
  - The CSS threshold falls with η, from 4.36% to 2.91%. The XZZX threshold rises, from 4.35% to 6.86%.
  - This matches the trend of both papers.
- **Biased noise and deformation: pass.** The CSS thresholds coincide in q, and at η = 0.5 the XZZX and CSS codes agree point by point.
- **CSS against both papers: pass.** At every η, the threshold is within 0.4% (relative) of the reference line and within 0.4 error bars of Campos2026.
- **XZZX against Campos2026: consistent for η ≤ 50 (within 1.4 error bars), low at η = 100.**
  - At η = 100 the threshold is 0.54 points (7%, 2.7 error bars) below 7.4%.
  - Two conditions differ. Campos2026 uses distances up to 40 and counts either logical. Here the distances are d = 11–19, and the lower basis is compared.
  - Counting either logical, with X and Z failures assumed independent, gives 6.97% (−2.2 error bars).
  - A small pilot at d = 19–35 showed the crossing rising with d, toward about 7.2%.
  - Neither effect has been confirmed with a production run.


## Excerpts

Verbatim from the sources, for text search in the originals. Math is in plain text, and citations are shown as […].

### BonillaAtaides2021 (arXiv v3, published as Nat. Commun. 12, 2172)

- Code, rounds and failure (Results, "Fault-tolerant thresholds"):
  > We simulate the XZZX code on a d×d lattice with periodic boundary conditions, and we perform d rounds of stabilizer measurements. We regard a given sample as a failure if the decoder introduces a logical error to the code qubits, or if the combination of the error string and its correction returned by the decoder includes a non-trivial cycle along the temporal axis.
- Noise (same section):
  > The phenomenological noise model is defined such that qubits experience errors with probability p per unit time. These errors may be either high-rate Pauli-Z errors that occur with probability p_h.r. per unit time, or low-rate Pauli X or Pauli-Y errors each occurring with probability p_l.r. per unit time. The noise bias with this phenomenological noise model is defined as η = p_h.r./(2p_l.r.).

  > Each stabilizer measurement returns the incorrect outcome with probability q = p_h.r. + p_l.r..

  > At η = 1/2 this noise model interpolates to a conventional noise model where q = 2p/3 […].
- Rates in terms of p (Methods, "The minimum-weight perfect-matching decoder"):
  > Pauli-Z errors occur at a higher rate, p_h.r. = pη/(η + 1), and Pauli-X and Pauli-Y errors both occur at the same low error rate p_l.r. = p/2(η + 1).
- Fig. 5(e) caption:
  > (e) Fault-tolerant threshold error rates p_c as a function of noise bias η and measurement error rates q = p_h.r. + p_l.r..

  > At a fixed bias, data points are found with 3 × 10^4 Monte Carlo samples for each physical error rate sampled and for each square lattice with distance d ∈ {12, 14, …, 20} at finite bias and d ∈ {24, 28, …, 40} at infinite bias.

  > The solid line shows the threshold of the conventional matching decoder for the CSS surface code undergoing phenomenological noise where bit-flip and dephasing errors are decoded independently. Specifically, it follows the function p_h.r. + p_l.r. = 0.029 where ∼2.9% is the phenomenological threshold […]. We note that our decoder is equivalent to the conventional matching decoder at η = 1/2.
- XZZX at high bias (Results, "Fault-tolerant thresholds"):
  > In the fault-tolerant case, we find our decoder tends towards a threshold of ∼10% as the bias becomes large.
- Code: qsdxzzx, cited in Code availability ("Software for all simulations performed for this study is available at https://bitbucket.org/qecsim/qsdxzzx/ and released under the OSI-approved BSD 3-Clause licence."). The Bitbucket workspace has been deactivated, so the files below are from the [Software Heritage archive](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://bitbucket.org/qecsim/qsdxzzx) (master 5fa612e). Its `data/README.rst`, section "Fault-Tolerant Thresholds", names the module: "To obtain logical failure rates for fault-tolerant threshold estimation for a square lattice XZZX code using MWPM, use the module".
  - Measurement flips, [ft_square_lattice_decoder.py L364–369](https://archive.softwareheritage.org/browse/content/sha1_git:e3d064d8cba1d33d959683d79c3b65e2d4dbca77/#L364-L369):
    ```python
    if q == 'standard' and bias == 'inf':
        q = p
    elif q == 'standard' and bias != 'inf':
        pZ = (p * bias) / (bias + 1)
        pX = p / (2 * (bias + 1))
        q = pZ + pX
    ```
  - d rounds, periodic in time, [L381–383](https://archive.softwareheritage.org/browse/content/sha1_git:e3d064d8cba1d33d959683d79c3b65e2d4dbca77/#L381-L383) and [L122–127](https://archive.softwareheritage.org/browse/content/sha1_git:e3d064d8cba1d33d959683d79c3b65e2d4dbca77/#L122-L127):
    ```python
    # Make the time dimension the same as the surface code dimension so that
    # the (2+1)-dimensional structure is a cube.
    T = L
    ```
    ```python
    # If there was a measurement error between 2 time stamps on a
    # certain plaquette, flip the plaquette state on each of time
    # stamps.
    if err.plaquettes[i][j].state == 1:
        lattice3d[k].plaquettes[i][j].state ^= 1
        lattice3d[(k - 1) % T].plaquettes[i][j].state ^= 1
    ```
  - Failure, [L396–398, L406–407](https://archive.softwareheritage.org/browse/content/sha1_git:e3d064d8cba1d33d959683d79c3b65e2d4dbca77/#L396-L407):
    ```python
    # Check for spatial logical errors.
    if (not result_lat.is_in_trivial_state()) or (not result_lat.is_in_trivial_state_Z()):
        spat_fail = True
    ...
    if spat_fail or temp_fail:
        total_fail += 1
    ```

### Campos2026 (arXiv v3, published as Quantum 10, 2073)

- Noise (§2.1):
  > We consider a single-qubit Pauli noise channel where all qubits can experience a Pauli error with probability p = p_x + p_y + p_z. Here, p_x, p_y and p_z correspond to the probabilities of X, Y and Z errors respectively. These errors occur independently and uniformly across the lattice.

  > This bias is quantified by η = p_z/(p_x + p_y). For simplicity, we assume p_x = p_y. We obtain the depolarizing channel when η = 0.5.

  > In this noise model, we include measurement error rates that scale with the weight of the stabilizers, in addition to the memory errors described above. Furthermore, we normalize the measurement errors so that they match the typical phenomenological noise model on the surface code at standard depolarizing noise. Specifically, the probability of measurement error p_m is w(p_y + p_z)/4 where w ≥ 4 is the weight of the stabilizer. For weight-2 stabilizers, we set p_m = p_y + p_z. This measurement noise model extends the noise model presented for the XZZX code […].
- Codes at ℓ = 2 (§2.2, §2.3):
  > An elongated compass code with ℓ = 2 is the rotated surface code (Figure 1).

  > In the case of ℓ = 2, the ZXXZ□ deformation is equivalent to the XZZX and XZZX□ deformations since it only switches the directions in which the low and high-weight edges are aligned (Figure 2).
- Decoder (§3):
  > For the codes we consider, an efficient and sufficiently accurate decoding algorithm is the minimum-weight perfect matching (MWPM) decoder, which we implement using PyMatching […].
- Shots, rounds and failure (§4):
  > In each shot, we create a noise vector, determine the corresponding syndrome, and decode the syndrome to get a correction. After decoding, we determine whether the residual error is trivial or if a logical error has occurred. Under phenomenological noise, the noise vectors and decoder graph are three-dimensional to include L measurement rounds. We assume the last round of measurements is perfect.
- Fit (§4) and distances (App. C):
  > Namely, near the threshold p_th we assume that the logical error rate is a quadratic function of (p − p_th)L^(1/ν) where p_th is the threshold, L is the distance, and ν is a critical exponent […].

  > We use a similar method to determine phenomenological thresholds by simulating codes with distances up to 40.
- Fig. 6, caption and the ℓ = 2 legend entries of (a) and (b):
  > Phenomenological thresholds of a) CSS and b) ZXXZ□-deformed elongated compass codes. Lines are drawn to guide the eye.

  > CSS, ℓ = 2

  > XZZX□, ℓ = 2
- Values: not in the text. They are the plotted points of Fig. 6, in the arXiv source files `CSS_PhenomThresholds_Rev1_1.pdf` and `ZXXZ_PhenomThresholds_Rev1_1.pdf`.

### Wang2003 (cited by BonillaAtaides2021 for the 2.9%; arXiv quant-ph/0207088 v2, published as Annals of Physics 303, 31)

- Conclusions:
  > Our result means that stored quantum data can be preserved with arbitrarily good fidelity if, in each round of syndrome measurement, qubit errors and syndrome measurement errors are independently and identically distributed, with error probability per qubit and per syndrome bit both below 2.9%.
