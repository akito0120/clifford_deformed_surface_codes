# B1: Decoder comparison at code capacity

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Criger2018 | B. Criger and I. Ashraf, "Multi-path summation for decoding 2D topological codes" [arXiv:1709.02154](https://arxiv.org/abs/1709.02154) | Fig. 7 (§4), Fig. 10 (§5) | Independent flips: MWPM 9.97 ± 0.01%, path-counting MWPM 10.34 ± 0.01%. Depolarizing: MWPM 14.88 ± 0.02%, BP with multi-path summation 17.76 ± 0.02% | Rotated code, d = 7, 11, 15, 19, 23, 25 values of p per figure. BP runs d iterations. A shot fails on either logical |
| LinLai2025 | T.-H. Lin and C.-Y. Lai, "Union-Intersection Union-Find for Decoding Depolarizing Errors in Topological Codes" [arXiv:2506.14745](https://arxiv.org/abs/2506.14745) | Table IV (§V-B), Table V (§V-C) | Rotated code, depolarizing: UF 14.68%, UF with weighted growth 15.03%, MWPM 15.19% | UF (§II-D): every invalid cluster grows by half-edges, then peeling. UF counts any logical error, MWPM the logical X error; the paper calls the two estimates very close. 10⁶ samples per point; distances not stated |
| Delfosse2021 | N. Delfosse and N. H. Nickerson, "Almost-linear time decoding algorithm for topological codes" [arXiv:1709.06218](https://arxiv.org/abs/1709.06218) | Table 1, §5 | Toric code, phase flips: UF 9.2% (uniform growth), 9.9% (smallest cluster first); MWPM 10.3%, cited from Dennis2002 | Half-edge growth and peeling; at least 10⁴ failures per point |
| deMartiIOlius2024 | A. de Martí i Olius et al., "Decoding algorithms for surface codes" [arXiv:2307.14989](https://arxiv.org/abs/2307.14989) | Tables 1 and 2 | Rotated code, η = 0.5: UF 11.6%, MWPM 14.0% | Review. d = 3–11, any logical error, N_runs = 100/P_L. MWPM from QECSIM, UF coded by the authors (App. C) |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Table 1, CSS, η = 100 | MWPM 10.0% | Rotated code (ℓ = 2), d = 11–19, either logical. At η = 100 the Z component flips at 0.995p, i.e. about 9.95% at η = ∞ |

- No decoder may exceed the optimal thresholds: 18.9% for depolarizing noise (Bombin2012) and 10.93% for independent flips (Merz and Chalker, quoted in Wang2003).

## Setup

- Configs, one per noise and decoder:
  - [config_depolarizing_bp.yaml](config_depolarizing_bp.yaml)
  - [config_depolarizing_uf.yaml](config_depolarizing_uf.yaml)
  - [config_dephasing_mwpm.yaml](config_dephasing_mwpm.yaml)
  - [config_dephasing_bp.yaml](config_dephasing_bp.yaml)
  - [config_dephasing_uf.yaml](config_dephasing_uf.yaml)
- `rotated_surface`, `code_capacity`
- d = 7, 11, 15, 19, 23
- p in steps of 0.2 points around each threshold
- Depolarizing: `depolarizing`, Z basis. The MWPM reference is [A1](../a1_code_capacity_depolarizing/result.md)'s Z basis.
- Independent Z flips: `biased` with η = inf, X basis
- Each point ran to 10,000 errors (`bp`) or 20,000 (others), with 0.5–3.3 × 10⁵ shots.
- `results/*/suppression.csv` comes from the sweep the config schema requires and is not a result.

## Result

From `results/*/threshold.csv` and A1's [results/threshold.csv](../a1_code_capacity_depolarizing/results/threshold.csv):

| Noise | Decoder | p_th (%) | ν | χ²_red | Ratio to MWPM | p_th, d = 11–23 (%) |
|---|---|---|---|---|---|---|
| Depolarizing | `mwpm` (A1) | 14.973 ± 0.013 | 1.59 | 2.12 | — | 15.090 |
| Depolarizing | `bp` | 17.649 ± 0.025 | 1.67 | 0.94 | 1.179 | 17.657 |
| Depolarizing | `uf` | 13.380 ± 0.013 | 1.63 | 1.56 | 0.894 | 13.459 |
| Independent Z | `mwpm` | 9.972 ± 0.010 | 1.61 | 2.06 | — | 10.035 |
| Independent Z | `bp` | 10.311 ± 0.016 | 1.67 | 2.52 | 1.034 | 10.441 |
| Independent Z | `uf` | 8.813 ± 0.010 | 1.62 | 2.15 | 0.884 | 8.878 |

- Without d = 7, χ²_red falls to 1.0–1.3.

## Verdict

- **`mwpm`, independent Z: pass.** 9.972 ± 0.010% against Criger2018's 9.97 ± 0.01%, the equivalent setting, and Campos2026's 10.0%.
- **`bp`, depolarizing: pass.** Between MWPM and 18.9%. 0.11 points below Criger2018's 17.76%, a different algorithm counting either logical, with the same gain over MWPM (1.18 against 1.19).
- **`bp`, independent Z: pass.** 3.4% above MWPM, close to the 3.7% gain of Criger2018's path counting, and below 10.93%. Most of `bp`'s depolarizing gain (+18%) therefore comes from the X–Z correlation of Y errors.
- **`uf`, depolarizing: pass.** Below MWPM, and inside the published UF range (11.6–14.68%; ratios 0.83–0.966).
- **`uf`, independent Z: pass.** Its ratio to MWPM, 0.884, is within 1% of Delfosse2021's uniform growth (0.893). LinLai2025's uniform-growth UF keeps 0.966, so UF thresholds depend on the implementation.


## Excerpts

Verbatim from the sources, for text search in the originals. Math is in plain text, and citations are shown as […].

### Criger2018 (arXiv v6, published as Quantum 2, 102)

- Measurement (§1):
  > In this work, we restrict ourselves to a simpler model, in which Pauli errors occur at random on data qubits, and the measured eigenvalues are correct, and obtained without consequence.
- Code (§2):
  > Specifically, we focus on the rotated surface code, with the boundary conditions from Figure 1.
- Noise (§3):
  > The derivation of the objective function in Equation (6) assumed that X and Z errors occur independently, with identical probability on each qubit.

  > Consider the frequently used example of depolarizing noise, in which each type of error is applied with equal probability.
- Path counting (§4):
  > Using this function to calculate Ω_e, we can replicate the result of Barrett/Stace/Doherty using the rotated surface code, see Figure 7.
- Fig. 7 (§4), caption and the titles of its two panels:
  > Threshold of the rotated surface code correcting IID X/Z errors. Above: Edge weights for MWPM are derived using the Manhattan distance, resulting threshold is 9.97 ± 0.01%, lower than the value of 10.3% obtained using alternate boundary conditions in […]. Below: Edge weights for MWPM are derived using path-counting, resulting in a threshold of 10.34 ± 0.01%, compensating for the disadvantage imposed by the rotated boundary conditions.

  > IID X/Z Error Model, without multi-path summation

  > IID X/Z Error Model, with multi-path summation
- BP (§5):
  > Using d rounds of belief propagation and the cost calculation in Section 4, we obtain a threshold of 17.76 ± 0.02% when correcting depolarizing noise, see Figure 10.
- Fig. 10 (§5), caption and the titles of its two panels:
  > Threshold for the rotated surface code correcting depolarizing errors. Above: Using uniform edge weights, the threshold is 14.88 ± 0.02%, less than the value of 15.5 ± 0.5% obtained using smooth/rough boundary conditions in […]. Below: When using multi-path odds summation as discussed in Section 4, the threshold improves to 17.76 ± 0.02%.

  > Depolarizing Error Model, without BP/multi-path summation

  > Depolarizing Error Model, with BP/multi-path summation
- d and p: the legend of all four panels reads "d = 7 d = 11 d = 15 d = 19 d = 23". The p values are not in the text. The arXiv source files plot 25 points per d: from 0.08 to 0.13 in `paper_iidxz_no_bp.tex` and `paper_iidxz_ext.tex` (Fig. 7), from 0.13 to 0.18 in `paper_dep_no_bp.tex` and from 0.15 to 0.20 in `paper_dep.tex` (Fig. 10).
- Code: [bcriger/sc_decoding](https://github.com/bcriger/sc_decoding) at commit 260f383, cited in Acknowledgements/Remarks ("Additional software produced for this work is available on Github […].").
  - BP, multi-path summation and failure counting, [decoding_2d.py L477–478, L498–499, L503–506, L519–520](https://github.com/bcriger/sc_decoding/blob/260f383/decoding_2d.py#L477-L520):
    ```python
    def run(self, n_trials, verbose=False, progress=True,
                dist_func=None, bp=False, bp_rounds=None):
    ...
            if bp:
                blfs = self.beliefs(err, bp_rounds=bp_rounds)
    ...
                prcsn = 4 if self.useBlossom else None
                x_graph, z_graph = mw.path_sum_graphs(self, err, beliefs=blfs, precision=prcsn)
                x_corr = self.correction(x_graph, 'Z')
                z_corr = self.correction(z_graph, 'X')
    ...
            log = self.logical_error(err, x_corr, z_corr)
            self.errors[log] += 1
    ```
  - BP rounds, [matched_weights.py L278–281, L291–294](https://github.com/bcriger/sc_decoding/blob/260f383/matched_weights.py#L278-L294). The docstring says d, but the code runs max(d, 10) rounds, i.e. 10 at d = 7:
    ```python
    def input_beliefs(sim, err, bp_rounds=None):
        """
        bp_rounds defaults to d.
        """
    ...
        if bp_rounds is None:
            bp_rounds = max(sim.dx, sim.dy, 10)

        propagate_beliefs(tg, bp_rounds)
    ```
  - Failure criterion, [decoding_2d.py L436–440](https://github.com/bcriger/sc_decoding/blob/260f383/decoding_2d.py#L436-L440) and [plot_utils.py L89–92](https://github.com/bcriger/sc_decoding/blob/260f383/plot_utils.py#L89-L92):
    ```python
    def logical_error(self, error, x_corr, z_corr):
        """
        Given an error and a correction, multiplies them and returns a
        single letter recording the resulting logical error (may be I,
        X, Y or Z)
    ```
    ```python
    def error_rate_plot(flnm, ltr='I'):
        """
        makes those fancy plots people like so much.
        Always plots an error rate (i.e. plots 1 - p for ltr = 'I').
    ```

### LinLai2025 (arXiv v1, published in IEEE JSAIT, doi:10.1109/JSAIT.2025.3581810)

- Code capacity noise and logical errors (§II-B):
  > We first consider the code capacity noise model with perfect syndrome extraction. We assume that each qubit experiences independent depolarizing Pauli errors at a physical error rate of ε, where a qubit undergoes an X, Y, or Z error with probability ε/3.

  > A logical error occurs if ÊE is not a stabilizer in S up to a global phase.
- UF decoder (§II-D):
  > The UF decoder can jointly decode erasures and Pauli errors by reducing the Pauli error decoding problem to an erasure decoding problem […]. Once this reduction is done, the peeling decoder is used to determine the correction operator.

  > Invalid clusters then expand outward by one half-edge. When two or more invalid clusters become connected, they are fused into a single valid cluster. This process repeats until all remaining clusters are valid. The peeling decoder then treats these clusters as an erasure set, resolving errors based on the syndrome information.
- Weighted growth (§IV-C):
  > In […], a weighted growth (WG) strategy is proposed for syndrome validation, prioritizing the growth of the smallest cluster first.
- Codes and distances (§V):
  > These decoders are applied to toric, rotated toric, surface, and rotated surface codes of various distances under depolarizing errors with perfect syndrome measurements and also the phenomenological noise model with faulty syndrome measurements.
- Samples (§V-B):
  > Figure 11(a) illustrates the decoding performance of UIUF with WG for the [[2d^2, 2, d]] toric codes near the threshold of this code family, where each data point is generated using 10^6 samples.

  > The determined thresholds are robust that even using 10^5 samples for each data point generates almost identical values in our simulations.
- Value: Table IV, row "Rotated Surface": UF 14.68%, UF + WG 15.03%, UIUF 15.16%, UIUF + WG 15.63%. Caption:
  > Thresholds of the UF and UIUF decoders with and without WG for the four topological code families.
- MWPM (§V-C):
  > For the MWPM decoder, we use the PyMatching v2 implementation […] in our simulations.
- Value: Table V, columns "code capacity" and "rotated surface codes": MWPM 15.19%†, UF+WG 15.03%. Caption and footnote:
  > Comparison between the MWPM and UIUF decoders in the code capacity and phenomenological noise models.

  > †: Estimate from PyMatching simulations of logical X error rates.
- Logical X against overall (§V-C):
  > We note that the estimate using logical X error rates is very close to the estimate obtained from overall logical error rates with UF-type decoders.

### Delfosse2021 (arXiv v3, published as Quantum 5, 595)

- Noise (§1):
  > For simplicity, we consider only i.i.d. phase-flip errors, where each qubit is subjected to a Z-error with probability p_Z. The X-part of a Pauli error can be corrected identically. In addition to Pauli errors, a qubit may be erased, with probability p_e.
- Value: Table 1, row "2d-toric code": UF decoder 9.9%, MWPM decoder 10.3% […]. Caption:
  > Comparison of the Union-Find and MWPM decoders' thresholds under phase-flip error.
  - The MWPM entry cites "Eric Dennis, Alexei Kitaev, Andrew Landahl, and John Preskill. Topological quantum memory. Journal of Mathematical Physics, 43 (9): 4452–4505, 2002."
- Half-edge growth and peeling (§2, Algorithm 1 "Union-Find decoder – Naive version"):
  > Grow C_i by increasing its radius by one half-edge.

  > Apply the peeling decoder to the erasure to find C.
- Uniform and weighted growth (§5):
  > The algorithm we have described so far grows all (odd) clusters uniformly in each round.

  > The Weighted Growth version of the Union-Find decoder is achieved by always growing the cluster with the smallest boundary size. This small modification improves the threshold of the 2d toric code from 9.2% to 9.9% for phase-flip errors and from 2.4% to 2.6% with faulty-syndrome measurements.
- Failures per point (App. B):
  > All data points were computed by repeated montecarlo simulations of random erasure and noise on a surface code followed by decoding. The simulations were repeated until at least 10,000 failures had been observed. Figure 6(a) shows the threshold for the 2d toric code, when p_e = 0, for which we find a threshold of 9.9%.

### deMartiIOlius2024 (arXiv v6, published as Quantum 8, 1498)

- Bias (§4.2; the footnote after "bias" is left out):
  > Therefore, the latter is usually referred as the biased noise model, where the bias is defined as η = p_z/(p_x+p_y) ≈ T_1/T_2 − 1/2 […].
- Noise and P_L (§5.1.2):
  > In FIG. 8 we plot the performance of the rotated planar code in terms of the logical error probability (P_L), that is, the probability of the decoding process failing in predicting an error given its syndrome, as a function of the physical error probability (p = p_x + p_y + p_z) whenever it is decoded using a MWPM decoder. Two noise models are considered: the top figure considers an i.i.d. depolarizing error model (p_x = p_y = p_z), while in the bottom figure considers an i.i.d. biased Pauli channel with bias η = 100.
- Values: Table 1 (MWPM, §5.1.2) and Table 2 (UF, §5.2.3), row η = 1/2: 0.140 and 0.116. Captions:
  > Probability threshold values for different biases in the rotated planar code under the MWPM decoding scheme.

  > Probability threshold values for different biases in the rotated planar code under the UF decoding scheme.
- Distances, failure, implementations and runs (App. C):
  > Monte Carlo computer simulations of the d×d rotated planar codes with d ∈ {3,5,7,9,11} have been performed with the objective of obtaining the performance curves and thresholds of the code when decoded with MWPM, UF, BPOSD and TN decoders.

  > Each round of the numerical simulation is performed by generating an N-qubit Pauli operator, calculating its associated syndrome, and finally running the decoding algorithm using the associated syndrome as its input (note that for the simulations performed in this paper, no SPAM or gate errors are considered). Once the error is estimated by the decoder, it is used to determine if a logical error has occurred on the codestate by using the channel error […]. The operational figure of merit we use to evaluate the performance of these quantum error correction schemes is the Logical Error Rate (P_L), i.e. the probability that a logical error has occurred after the recovery operation.

  > Regarding the software implementations of the decoders used to obtain the simulations in Section 5 have been: QECSIM for the MWPM and tensor network decoder, the LDPC implementation of Joschka Roffe for the BPOSD decoder and an implementation coded by ourselves for the UF decoder by Delfosse and Nickerson.

  > For the numerical Monte Carlo methods employed to estimate the P_L of the rotated planar codes, we have applied the following rule of thumb to select the number of simulation runs, N_runs […], as N_runs = 100/P_L.

### Campos2026 (arXiv v3, published as Quantum 10, 2073)

- Noise (§2.1):
  > We consider a single-qubit Pauli noise channel where all qubits can experience a Pauli error with probability p = p_x + p_y + p_z. Here, p_x, p_y and p_z correspond to the probabilities of X, Y and Z errors respectively. These errors occur independently and uniformly across the lattice.

  > This bias is quantified by η = p_z/(p_x + p_y). For simplicity, we assume p_x = p_y. We obtain the depolarizing channel when η = 0.5.
- Code (§2.2):
  > An elongated compass code with ℓ = 2 is the rotated surface code (Figure 1).
- Decoder (§3):
  > For the codes we consider, an efficient and sufficiently accurate decoding algorithm is the minimum-weight perfect matching (MWPM) decoder, which we implement using PyMatching […].
- Failure criterion (§4):
  > In each shot, we create a noise vector, determine the corresponding syndrome, and decode the syndrome to get a correction. After decoding, we determine whether the residual error is trivial or if a logical error has occurred.
- Value: App. A, Table 1, row η = 100, column ℓ = 2: 10.0 | 38.2 | -. Caption:
  > Thresholds for CSS, XZZX□-deformed and ZXXZ□-deformed compass codes at all elongation parameters and biases under code capacity noise.

  > We record the remaining thresholds in the following way: CSS | XZZX□ | ZXXZ□. Numerical uncertainty of these threshold values do not exceed 0.8%.
- Distances and the total threshold (App. C):
  > In particular, we use odd distances between 27 and 43 for the deformed codes and distances between 11 and 19 for CSS codes.

  > We note that, in general, the X and Z thresholds of the codes we consider do not coincide. As a result, the total threshold is determined by the lower one of the two in the thermodynamic limit.

### Bombin2012 (arXiv v2, published as Phys. Rev. X 2, 021004)

- Depolarizing channel (§I):
  > where the density matrix ρ fully describes the quantum state and the probability for each type of error to occur is p_w ∈ [0,1] with p := p_x + p_y + p_z. The depolarizing channel exhibits equal probability p_w = p/3 for each error type to arise.
- Value (abstract and §I):
  > We compute the stability of the toric code to depolarization by mapping the quantum problem onto a classical disordered eight-vertex Ising model. By studying the stability of the related ferromagnetic phase both via large-scale Monte Carlo simulations and via the duality method, we are able to demonstrate an increased error threshold of 18.9(3)% when noise correlations are taken into account.

  > We estimate the threshold under depolarizing noise for ideal error correction, such that, in particular, correlations are taken into account. We find p_c = 18.9(3)%.

### Wang2003 (arXiv quant-ph/0207088 v2, published as Annals of Physics 303, 31)

- Independent flips (§III.A, §III.B):
  > With the toric code, X errors (bit flips) and Z errors (phase flips) can be corrected independently; this suffices to protect against general Pauli errors, since a Y error is just a bit flip and a phase flip acting on the same qubit.

  > To be concrete, suppose that the Z errors are independently and identically distributed, occuring with probability p on each qubit.
- Value (§I and §IV):
  > In the case where the error syndrome can be measured flawlessly, the critical error rate is given by the critical antiferromagnetic bond concentration on the Nishimori line of the two-dimensional random-bond Ising model (RBIM). Numerical calculations performed earlier by other authors […] have established p_c = .1093 ± .0002.

  > In a recent study of the Nishimori point, Merz and Chalker found […] p_c = .1093 ± .0002, ν = 1.50 ± .03.
  - The works cited in §I are Honecker, Picco and Pujol, Phys. Rev. Lett. 87, 047201 (2001), and Merz and Chalker, Phys. Rev. B 65, 054425 (2002).
