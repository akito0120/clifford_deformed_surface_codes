# A1: Depolarizing code-capacity threshold

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Criger2018 | B. Criger and I. Ashraf, "Multi-path summation for decoding 2D topological codes" [arXiv:1709.02154](https://arxiv.org/abs/1709.02154) | Fig. 7 (top), §4 | 9.97 ± 0.01%, i.e. 14.95 ± 0.02% at p = 1.5q | Rotated code, independent X and Z flips (probability q each), perfect measurement, MWPM with Manhattan-distance (unit) weights, d = 7, 11, 15, 19, 23, q = 0.08–0.13 (25 points) |
| Criger2018 | (same) | Fig. 10 (top), §5 | 14.88 ± 0.02% | The same, with depolarizing noise, p = 0.13–0.18 (25 points) |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Table 1, ℓ = 2, η = 0.5 | 14.8%, one value for CSS and the deformed codes (uncertainty ≤ 0.8%) | Code capacity, PyMatching with weights log((1−p)/p), quadratic FSS fit, d = 11–19 (CSS) and 27–43 (deformed codes) |

- **Both papers count a failure of either logical operator.**
  - A shot fails whenever the residual error is a non-trivial logical, X, Y or Z.
  - Criger2018's code returns I, X, Y or Z for the residual and counts everything but I.
  - Campos2026 checks "whether the residual error is trivial" (§Methods).
- **Fig. 7 is the equivalent reference for one basis.**
  - In one memory basis, the decoder sees one component of each qubit's error: Z for the X basis.
  - Under depolarizing noise, that component appears with probability p_Z + p_Y = 2p/3, independently on each qubit. MWPM decodes it on its own graph with uniform weights. That is Criger2018's independent-flip problem at q = 2p/3.


## Setup

- Config: [config.yaml](config.yaml)
- Codes: `rotated_surface`, `xzzx` and `xy`
- `code_capacity` with `depolarizing` noise
- Decoder: `mwpm`
- d = 7, 11, 15, 19, 23
- Bases: X and Z
- p = 0.136–0.164 in steps of 0.002
- Each point ran to at least 20,000 errors (20,000–26,513)
- Fit: quadratic FSS with x_window = 0.1 and ν0 = 1.5

## Result

From [results/threshold.csv](results/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red |
|---|---|---|---|---|
| rotated_surface | X | 14.962 ± 0.013 | 1.61 | 2.48 |
| rotated_surface | Z | 14.973 ± 0.013 | 1.59 | 2.12 |
| xzzx | X | 14.946 ± 0.013 | 1.56 | 1.75 |
| xzzx | Z | 14.965 ± 0.013 | 1.58 | 2.10 |
| xy | X | 14.962 ± 0.014 | 1.66 | 2.06 |
| xy | Z | 14.955 ± 0.013 | 1.59 | 2.04 |

- Weighted mean: 14.961 ± 0.005%.
- Spread: 0.028 points.


## Verdict

- **Clifford invariance: pass.** The six series agree point by point and in p_th, and their DEMs have the same structure at every simulated distance.
- **Criger2018 Fig. 7 (1.5 × (9.968 ± 0.012)% = 14.952 ± 0.018%): consistent within its stated uncertainty.**
- **Criger2018 Fig. 10 (14.88%): consistent, with a different metric.**
  - Fig. 10 counts a failure of either logical operator.
  - The 0.08-point difference splits into the failure criterion, the p range and the fit method.
- **Campos2026 (14.8%): consistent within its stated uncertainty.**


## Excerpts

Verbatim from the sources, for text search in the originals. Math is in plain text, and citations are shown as […].

### Criger2018 (arXiv v6, published as Quantum 2, 102)

- Measurement (§1):
  > In this work, we restrict ourselves to a simpler model, in which Pauli errors occur at random on data qubits, and the measured eigenvalues are correct, and obtained without consequence.
- Code and edge weights (§2):
  > Specifically, we focus on the rotated surface code, with the boundary conditions from Figure 1.

  > This implies that the weight of the corresponding edge is given by the rotated Manhattan distance between the vertices it connects, see Figure 2.
- Noise (§3):
  > The derivation of the objective function in Equation (6) assumed that X and Z errors occur independently, with identical probability on each qubit.

  > Consider the frequently used example of depolarizing noise, in which each type of error is applied with equal probability.
- Fig. 7 (§4), caption and title of the top panel:
  > Threshold of the rotated surface code correcting IID X/Z errors. Above: Edge weights for MWPM are derived using the Manhattan distance, resulting threshold is 9.97 ± 0.01%, lower than the value of 10.3% obtained using alternate boundary conditions in […].

  > Error bars represent a 99% confidence interval. Solid lines are maximum-likelihood fits to data near the threshold.

  > IID X/Z Error Model, without multi-path summation
- Fig. 10 (§5), caption and title of the top panel:
  > Threshold for the rotated surface code correcting depolarizing errors. Above: Using uniform edge weights, the threshold is 14.88 ± 0.02%, less than the value of 15.5 ± 0.5% obtained using smooth/rough boundary conditions in […].

  > Error bars are 99% confidence intervals. Solid lines are maximum-likelihood fits to data points near the threshold.

  > Depolarizing Error Model, without BP/multi-path summation
- d and p: the legend of both top panels reads "d = 7 d = 11 d = 15 d = 19 d = 23". The p values are not in the text. The arXiv source files `paper_iidxz_no_bp.tex` and `paper_dep_no_bp.tex` plot 25 points per d, from 0.08 to 0.13 and from 0.13 to 0.18.
- Code: [bcriger/sc_decoding](https://github.com/bcriger/sc_decoding) at commit 260f383, cited in Acknowledgements/Remarks ("Additional software produced for this work is available on Github […].").
  - IID X/Z noise, [decoding_2d.py L45–47, L76](https://github.com/bcriger/sc_decoding/blob/260f383/decoding_2d.py#L45-L76):
    ```python
    This is a pretty bare-bones simulation of the 2D rotated surface
    code. We take a surface code of distance d, and put it up against
    an IID X/Z error model with probability p.
    ...
    self.error_model = em.PauliErrorModel([(1. - p)**2, p * (1. - p), p * (1. - p), p**2],
    ```
  - Depolarizing noise, [run_script.py L97–98](https://github.com/bcriger/sc_decoding/blob/260f383/run_script.py#L97-L98) and [error_model.py L99–100](https://github.com/bcriger/sc_decoding/blob/260f383/error_model.py#L99-L100):
    ```python
    if sim_type == 'dep':
        current_sim.error_model = em.depolarize(err,
    ```
    ```python
    def depolarize(p, q_set):
        p_vec = [1. - p, p / 3., p / 3., p / 3.]
    ```
  - Failure criterion, [decoding_2d.py L436–440, L519–520](https://github.com/bcriger/sc_decoding/blob/260f383/decoding_2d.py#L436-L520) and [plot_utils.py L89–92](https://github.com/bcriger/sc_decoding/blob/260f383/plot_utils.py#L89-L92):
    ```python
    def logical_error(self, error, x_corr, z_corr):
        """
        Given an error and a correction, multiplies them and returns a
        single letter recording the resulting logical error (may be I,
        X, Y or Z)
    ...
    log = self.logical_error(err, x_corr, z_corr)
    self.errors[log] += 1
    ```
    ```python
    def error_rate_plot(flnm, ltr='I'):
        """
        makes those fancy plots people like so much.
        Always plots an error rate (i.e. plots 1 - p for ltr = 'I').
    ```

### Campos2026 (arXiv v3, published as Quantum 10, 2073)

- Noise (§2.1):
  > We consider a single-qubit Pauli noise channel where all qubits can experience a Pauli error with probability p = p_x + p_y + p_z. Here, p_x, p_y and p_z correspond to the probabilities of X, Y and Z errors respectively. These errors occur independently and uniformly across the lattice.

  > This bias is quantified by η = p_z/(p_x + p_y). For simplicity, we assume p_x = p_y. We obtain the depolarizing channel when η = 0.5.
- Decoder (§3):
  > For the codes we consider, an efficient and sufficiently accurate decoding algorithm is the minimum-weight perfect matching (MWPM) decoder, which we implement using PyMatching […].

  > The vertices of the graph correspond to stabilizers, the edges correspond to qubits, and the weights of each edge are a logarithmic function of the probability of error of the qubit it corresponds to (w_ij = log((1 − p_ij)/p_ij)).
- Failure criterion and fit (§4):
  > In each shot, we create a noise vector, determine the corresponding syndrome, and decode the syndrome to get a correction. After decoding, we determine whether the residual error is trivial or if a logical error has occurred.

  > Namely, near the threshold p_th we assume that the logical error rate is a quadratic function of (p − p_th)L^(1/ν) where p_th is the threshold, L is the distance, and ν is a critical exponent […].
- Value (App. A, Table 1, row η = 0.5, column ℓ = 2: 14.8), caption:
  > Thresholds for CSS, XZZX□-deformed and ZXXZ□-deformed compass codes at all elongation parameters and biases under code capacity noise. When η = 0.5, the thresholds of codes are the same since p_x = p_z and thus the deformations do not change the weights.

  > Numerical uncertainty of these threshold values do not exceed 0.8%. Thresholds are estimated using finite-size scaling fits near threshold.
- Distances (App. C):
  > In particular, we use odd distances between 27 and 43 for the deformed codes and distances between 11 and 19 for CSS codes.
