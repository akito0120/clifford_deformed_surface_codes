# A5-refit: Suppression fit on published data

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| McEwen2023 | M. McEwen, D. Bacon and C. Gidney, "Relaxing hardware requirements for surface code circuits using time-dynamics" [arXiv:2302.02192](https://arxiv.org/abs/2302.02192) | Figs. 9, 13, 17, E.1 (4-CZ) and E.2 (4-CX); data [Zenodo 7587578](https://zenodo.org/records/7587578) ([fused_stats.csv](fused_stats.csv), CC-BY 4.0); fit in [midout](https://github.com/Strilanc/midout/blob/main/tools/plot_footprint) | Teraquop footprints in figures, and refit values with paper's method | Standard circuit 4-CZ (SI1000) and 4-CX (uniform depolarizing), d = 3–15, r = 4d. p_L per d rounds, √q against ln p_L, unweighted `sinter.fit_line_y_at_x` with `max_extra_squared_error=1`, at 10⁻¹² |

- The reference is McEwen2023's own fit, re-run on their data, because the paper prints no footprint numbers.
- The fits differ in how to take the y axis: cdsc fits a line to log p_L **per round**, McEwen2023 to ln p_L **per d rounds**. So cdsc is also run with McEwen2023's model (rounds = r/d).

## Setup

- [refit_mcewen2023.py](refit_mcewen2023.py) on [fused_stats.csv](fused_stats.csv). The script re-implements McEwen2023's fit and calls `estimate_suppression` of cdsc.
- No sampling and no config.

## Result

From [mcewen2023_footprint.csv](mcewen2023_footprint.csv). Footprints in qubits; * = outside McEwen2023's band.

4-CZ (SI1000):

| p | McEwen2023 [band] | cdsc, per round | cdsc, per d rounds |
|---|---|---|---|
| 0.0001 | 260 [191, 341] | 258 | 275 |
| 0.0002 | 392 [322, 469] | 376 | 411 |
| 0.0003 | 512 [447, 581] | 491 | 541 |
| 0.0005 | 798 [684, 921] | 727 | 813 |
| 0.0008 | 1131 [1036, 1230] | 1096 | 1239* |
| 0.001 | 1507 [1372, 1649] | 1397 | 1587 |
| 0.002 | 5325 [4752, 5930] | 4134* | 5274 |
| 0.003 | 24106 [21238, 27156] | 12603* | 23449 |
| 0.004 | 389832 [338489, 444799] | 50299* | 386054 |

4-CX (uniform depolarizing):

| p | McEwen2023 [band] | cdsc, per round | cdsc, per d rounds |
|---|---|---|---|
| 0.0001 | 204 [153, 262] | 233 | 247 |
| 0.0002 | 338 [280, 401] | 329 | 359 |
| 0.0003 | 407 [333, 487] | 396 | 434 |
| 0.0005 | 555 [483, 633] | 537 | 591 |
| 0.0008 | 767 [689, 849] | 744 | 830 |
| 0.001 | 921 [823, 1025] | 888 | 992 |
| 0.002 | 2099 [1899, 2309] | 1871* | 2141 |
| 0.003 | 4280 [3830, 4755] | 3451* | 4244 |
| 0.004 | 9305 [8257, 10416] | 6421* | 9140 |
| 0.005 | 23191 [20436, 26119] | 12259* | 22290 |

- McEwen2023's fit, re-run, matches Fig. 9's 4-CZ curve and Fig. E.2's 4-CX curve as read off the figures
- With McEwen2023's model (fit with p_L per d rounds), cdsc is in the band at 18 of 19 points.
- The per-round line extrapolates to smaller footprints near the threshold.

## Verdict

- **McEwen2023: pass.**
  - With McEwen2023's model, cdsc reproduces its footprints within its band at 18 of 19 points.
  - With p_L per round (cdsc's own model), they agree at p ≤ 0.001. Near threshold it falls outside the band, which the difference in model explains. Fitting p_L per round is common, so this does not indicate an error in cdsc's method.
