# Usage:
# python case_studies/r1_regular_deformations/plot_patterns.py [--distance 7] [--out DIR]

import argparse
import math
import sys
import textwrap
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyBboxPatch, Patch, Polygon, Wedge

from cdsc.codes.definition import CodeDefinition
from cdsc.codes.registry import build_code, registered_codes

# A sibling of this script, importable because Python puts the script's directory on sys.path
from codes import FAMILIES, PATCH

# Each family's rule for the letter index k of data qubit (c, r), as FAMILIES computes it, and how it looks
RULES = {
    "cell": ("k = 2 (r mod 2) + (c mod 2)", "2×2 unit cell: top row, then bottom row"),
    "row3": ("k = c mod 3", "period 3 along a row: columns are constant"),
    "col3": ("k = r mod 3", "period 3 along a column: rows are constant"),
    "diag3": ("k = (r + c) mod 3", "constant along every / diagonal"),
    "anti3": ("k = (r − c) mod 3", "constant along every \\ diagonal"),
    "diag4": ("k = (r + c) mod 4", "constant along every / diagonal"),
}

# The data qubits (c, r) that spell the suffix in order
KEYS = {
    "cell": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "row3": [(0, 0), (1, 0), (2, 0)],
    "col3": [(0, 0), (0, 1), (0, 2)],
    "diag3": [(0, 0), (1, 0), (2, 0)],
    "anti3": [(0, 0), (0, 1), (0, 2)],
    "diag4": [(0, 0), (1, 0), (2, 0), (3, 0)],
}

# The registered code drawn as each family's example
EXAMPLES = {
    "cell": "cell_IV_HI", "row3": "row3_IVH", "col3": "col3_IVH",
    "diag3": "diag3_IVH", "anti3": "anti3_IVH", "diag4": "diag4_IVHI",
}

READING = "data qubit (c, r) takes letter k of the name's suffix (k = 0 is the first letter)"
ORIENTATION = ("(c, r) = (0, 0) is the data qubit at (1, 1), top left; x = 2c + 1 grows to the right and "
               "y = 2r + 1 grows down, as in stim's diagrams")

INK, INK_SECONDARY, INK_MUTED, HAIRLINE = "#0b0b0b", "#52514e", "#898781", "#c3c2b7"
# k: a gray ramp from light to dark, the same in every family
INDEX_FILL = {"0": "#e1e0d9", "1": "#c3c2b7", "2": "#898781", "3": "#52514e"}
INDEX_TEXT = {"0": INK, "1": INK, "2": INK, "3": "#ffffff"}
# Labels: I leaves the qubit undeformed; H and V take the first two categorical colors
LABEL_FILL = {"I": "#ffffff", "H": "#2a78d6", "V": "#eb6834"}
LABEL_TEXT = {"I": INK, "H": "#ffffff", "V": "#ffffff"}
CHECK_FILL = {"Z": "#e1e0d9", "X": "#ffffff"}

RADIUS = 0.32  # of a data qubit; neighbours are 1 apart

# A deformation's label is the Pauli its Z error acts as on the CSS code: Z (I), X (H) or Y (V)
LABEL_OF_PAULI = {"Z": "I", "X": "H", "Y": "V"}


def label_grid(code: CodeDefinition) -> tuple[tuple[str, ...], ...]:
    # grid[r][c]: the label of the data qubit at column c and row r
    d = code.distance
    grid = [[""] * d for _ in range(d)]
    for q in code.data_qubits:
        deformation = code.deformation_of(q)
        pauli = next(p for p, image in deformation.items() if image == "Z")
        grid[(q[1] - 1) // 2][(q[0] - 1) // 2] = LABEL_OF_PAULI[pauli]
    return tuple(tuple(row) for row in grid)


def suffix_of(name: str) -> str:
    # The labels of a name, in the order of k
    return name.split("_", 1)[1].replace("_", "")


def name_of(prefix: str, text: str) -> str:
    # The name codes.py gives a pattern; a cell name splits the unit cell into its rows
    return f"cell_{text[:2]}_{text[2:]}" if prefix == "cell" else f"{prefix}_{text}"


def plot_xy(q) -> tuple[float, float]:
    # Lattice coordinate (x, y) to the plot's (c, r), where the data qubits sit on integers
    return (q[0] - 1) / 2, (q[1] - 1) / 2


def setup_axes(ax, d: int) -> None:
    # Columns c along the top and rows r down the left, so the panel reads like the lattice in stim's diagrams
    ax.set_xlim(-0.75, d - 0.25)
    ax.set_ylim(d - 0.25, -0.75)
    ax.set_aspect("equal")
    ax.set_xticks(range(d))
    ax.set_yticks(range(d))
    ax.xaxis.tick_top()
    ax.tick_params(length=0, labelsize=8, labelcolor=INK_MUTED)
    ax.set_xlabel("c", color=INK_MUTED, fontsize=9)
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("r", color=INK_MUTED, fontsize=9, rotation=0, labelpad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)


def caption(ax, text: str, fontsize: float) -> None:
    ax.text(0.5, -0.03, text, transform=ax.transAxes, ha="center", va="top", fontsize=fontsize, color=INK_SECONDARY)


def draw_checks(ax, d: int) -> None:
    # The checks of the CSS code: squares in the bulk and half discs on the boundary
    for ancilla, legs in build_code("rotated_surface", distance=d).stabilizers.items():
        style = dict(facecolor=CHECK_FILL[next(iter(legs.values()))], edgecolor=HAIRLINE, linewidth=0.6, zorder=0)
        center = plot_xy(ancilla)
        corners = [plot_xy(q) for q in legs]
        if len(corners) == 4:
            corners.sort(key=lambda p: math.atan2(p[1] - center[1], p[0] - center[0]))
            ax.add_patch(Polygon(corners, closed=True, **style))
        else:
            # A boundary check stands on its two legs and bulges toward its ancilla, outside the lattice
            mid = tuple((a + b) / 2 for a, b in zip(*corners))
            angle = math.degrees(math.atan2(center[1] - mid[1], center[0] - mid[0]))
            ax.add_patch(Wedge(mid, 0.5, angle - 90, angle + 90, **style))


def draw_qubits(ax, grid, fill: dict, text: dict, key, fontsize: float) -> None:
    # A circle per data qubit showing grid[r][c]; the qubits of the key share one rounded outline
    size = fontsize * min(1.0, 7 / len(grid))
    for r, row in enumerate(grid):
        for c, entry in enumerate(row):
            ax.add_patch(Circle((c, r), RADIUS, facecolor=fill[entry], edgecolor=INK_MUTED, linewidth=0.8, zorder=2))
            ax.text(c, r, entry, ha="center", va="center", fontsize=size, fontweight="bold",
                    color=text[entry], zorder=3)
    cs, rs = [c for c, _ in key], [r for _, r in key]
    pad = 0.47
    ax.add_patch(FancyBboxPatch(
        (min(cs) - pad, min(rs) - pad), max(cs) - min(cs) + 2 * pad, max(rs) - min(rs) + 2 * pad,
        boxstyle="round,pad=0,rounding_size=0.25", facecolor="none", edgecolor=INK, linewidth=1.8, zorder=4,
    ))


def draw_rule(ax, prefix: str, index_of, d: int, fontsize: float) -> None:
    # The letter index k of every data qubit
    setup_axes(ax, d)
    grid = [[str(index_of(c, r)) for c in range(d)] for r in range(d)]
    draw_qubits(ax, grid, INDEX_FILL, INDEX_TEXT, KEYS[prefix], fontsize)
    formula, look = RULES[prefix]
    ax.set_title(f"{prefix}: {formula}", fontsize=fontsize + 1, fontweight="bold", color=INK)
    caption(ax, look, fontsize)


def draw_example(ax, prefix: str, index_of, d: int, fontsize: float) -> None:
    # The example code as the framework builds it, which must follow the rule
    name = EXAMPLES[prefix]
    suffix = suffix_of(name)
    grid = label_grid(build_code(name, distance=d))
    assert grid == tuple(tuple(suffix[index_of(c, r)] for c in range(d)) for r in range(d)), name
    setup_axes(ax, d)
    draw_checks(ax, d)
    draw_qubits(ax, grid, LABEL_FILL, LABEL_TEXT, KEYS[prefix], fontsize)
    ax.set_title(f"{name}, d = {d}", fontsize=fontsize + 1, fontweight="bold", color=INK)
    caption(ax, "k = " + ", ".join(f"{k} → {label}" for k, label in enumerate(suffix)), fontsize)


def add_legend(fig: plt.Figure, ncol: int, y: float) -> None:
    def qubit(label: str, text: str) -> Line2D:
        return Line2D([], [], marker="o", linestyle="none", markersize=12, markerfacecolor=LABEL_FILL[label],
                      markeredgecolor=INK_MUTED, label=text)

    handles = [
        qubit("I", "I: none; a Z error stays a Z error"),
        qubit("H", "H: Hadamard; a Z error acts as X on the CSS code"),
        qubit("V", "V: √X; a Z error acts as Y on the CSS code"),
        Patch(facecolor=CHECK_FILL["Z"], edgecolor=HAIRLINE, label="Z check of the CSS code"),
        Patch(facecolor=CHECK_FILL["X"], edgecolor=HAIRLINE, label="X check of the CSS code"),
        Patch(facecolor="none", edgecolor=INK, linewidth=1.8, label="the qubits that spell the suffix in order"),
    ]
    # matplotlib fills a legend column by column; reorder so that it reads row by row
    rows = math.ceil(len(handles) / ncol)
    handles = [handles[row * ncol + column] for column in range(ncol) for row in range(rows)]
    fig.legend(handles=handles, loc="center", bbox_to_anchor=(0.5, y), ncol=ncol, frameon=False, fontsize=9)


def skipped_suffixes(prefix: str, size: int, index_of, owner: dict) -> tuple[int, list[str]]:
    # How many suffixes of the family are registered, and the others, each with the code of the same pattern
    names = set(registered_codes())
    skipped = []
    for labels in product("IHV", repeat=size):
        name = name_of(prefix, "".join(labels))
        if name not in names:
            grid = tuple(tuple(labels[index_of(c, r)] for c in range(PATCH)) for r in range(PATCH))
            skipped.append(f"{name.split('_', 1)[1]} = {owner[grid]}")
    registered = sum(name.startswith(f"{prefix}_") for name in names)
    assert registered + len(skipped) == 3 ** size, f"{prefix}: name_of does not match codes.py"
    return registered, skipped


def family_figure(prefix: str, size: int, index_of, d: int, owner: dict) -> plt.Figure:
    fig, (rule_ax, example_ax) = plt.subplots(1, 2, figsize=(10, 6.6))
    fig.subplots_adjust(left=0.05, right=0.97, top=0.80, bottom=0.22, wspace=0.15)
    draw_rule(rule_ax, prefix, index_of, d, fontsize=10)
    draw_example(example_ax, prefix, index_of, d, fontsize=10)
    fig.suptitle(f"{prefix}: {READING}", y=0.97, fontsize=12, fontweight="bold", color=INK)
    fig.text(0.5, 0.925, ORIENTATION, ha="center", fontsize=9, color=INK_SECONDARY)
    add_legend(fig, ncol=3, y=0.11)
    registered, skipped = skipped_suffixes(prefix, size, index_of, owner)
    footer = (f"{registered} of {3 ** size} suffixes are registered; the others repeat an earlier code: "
              + ", ".join(skipped))
    fig.text(0.5, 0.025, textwrap.fill(footer, 140), ha="center", va="bottom", fontsize=8, color=INK_SECONDARY)
    return fig


def overview_figure(d: int) -> plt.Figure:
    fig, axes = plt.subplots(2, len(FAMILIES), figsize=(3.6 * len(FAMILIES), 9.6))
    fig.subplots_adjust(left=0.02, right=0.99, top=0.84, bottom=0.13, wspace=0.12, hspace=0.4)
    for column, (prefix, _, index_of) in enumerate(FAMILIES):
        draw_rule(axes[0, column], prefix, index_of, d, fontsize=9)
        draw_example(axes[1, column], prefix, index_of, d, fontsize=9)
    fig.suptitle(f"R1 code names: {READING}", y=0.97, fontsize=14, fontweight="bold", color=INK)
    fig.text(0.5, 0.93, ORIENTATION, ha="center", fontsize=10, color=INK_SECONDARY)
    add_legend(fig, ncol=6, y=0.05)
    return fig


def save(fig: plt.Figure, stem: Path) -> list[Path]:
    path = stem.with_suffix(".pdf")
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return [path]


def main() -> int:
    parser = argparse.ArgumentParser(description="Draw the R1 deformation patterns, as a key to the code names.")
    parser.add_argument("--distance", type=int, default=7, help="distance of the drawn codes (default: 7)")
    parser.add_argument("--out", help="output directory (default: results/patterns next to this script)")
    args = parser.parse_args()
    if args.distance < 4:
        parser.error("--distance must be at least 4, the length of the diag4 key")

    out = Path(args.out) if args.out else Path(__file__).parent / "results" / "patterns"
    out.mkdir(parents=True, exist_ok=True)

    # Every registered code by its pattern; codes.py registers each pattern once
    owner = {label_grid(build_code(name, distance=PATCH)): name for name in registered_codes()}
    assert len(owner) == len(registered_codes()), "two registered codes share a pattern"

    paths = []
    for prefix, size, index_of in FAMILIES:
        assert [index_of(c, r) for c, r in KEYS[prefix]] == list(range(size)), f"{prefix}: the key does not spell the suffix"
        paths += save(family_figure(prefix, size, index_of, args.distance, owner), out / f"pattern_{prefix}")
    paths += save(overview_figure(args.distance), out / "patterns_overview")
    for path in paths:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
