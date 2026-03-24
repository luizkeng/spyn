"""
generate_workflow_comparison.py

Produces a two-panel figure comparing the manual GIPAW workflow (≥11 steps)
against the SPYN workflow (6 steps).

Usage:
    python docs/figures/generate_workflow_comparison.py
    # → saves workflow_comparison.png and workflow_comparison.pdf
"""

import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

OUT = pathlib.Path(__file__).parent

MANUAL_STEPS = [
    "1. Obtain CIF file",
    "2. Convert CIF → QE format",
    "3. Download pseudopotentials",
    "4. Edit SCF input manually",
    "5. Run pw.x (terminal)",
    "6. Verify convergence (grep)",
    "7. Edit GIPAW input manually",
    "8. Run gipaw.x (terminal)",
    "9. Parse output (grep script)",
    "10. Compute δ = σref − σiso",
    "11. Plot spectrum (script)",
]

SPYN_STEPS = [
    "1. Open SPYN",
    "2. File → Import CIF",
    "3. Set SCF parameters",
    "4. Click Calculate SCF",
    "5. Click Calculate GIPAW",
    "6. Set reference → Plot",
]

COLOR_MANUAL = "#e05252"   # red
COLOR_SPYN   = "#4caf50"   # green
BOX_H        = 0.55
BOX_W        = 3.2
GAP          = 0.15
FONT         = 9


def draw_steps(ax, steps, x_left, color, title):
    n = len(steps)
    total_h = n * (BOX_H + GAP) - GAP
    y_start = total_h / 2 - BOX_H / 2

    ax.text(x_left + BOX_W / 2, y_start + BOX_H + 0.3, title,
            ha='center', va='bottom', fontsize=11, fontweight='bold',
            color=color)

    for i, step in enumerate(steps):
        y = y_start - i * (BOX_H + GAP)
        rect = mpatches.FancyBboxPatch(
            (x_left, y), BOX_W, BOX_H,
            boxstyle="round,pad=0.05",
            linewidth=1, edgecolor=color,
            facecolor=color + "22",   # light fill
        )
        ax.add_patch(rect)
        ax.text(x_left + BOX_W / 2, y + BOX_H / 2, step,
                ha='center', va='center', fontsize=FONT, color="#222222")

        # Arrow to next step
        if i < n - 1:
            y_arrow = y - GAP / 2
            ax.annotate(
                '', xy=(x_left + BOX_W / 2, y - GAP + 0.02),
                xytext=(x_left + BOX_W / 2, y - 0.02),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
            )

    # Step count badge
    ax.text(x_left + BOX_W / 2, y_start - (n - 0.5) * (BOX_H + GAP) - 0.1,
            f"{n} steps", ha='center', va='top',
            fontsize=10, fontweight='bold', color=color)


def main():
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_xlim(0, 8)
    ax.set_ylim(-1, 9)
    ax.axis('off')

    draw_steps(ax, MANUAL_STEPS, x_left=0.3,  color=COLOR_MANUAL,
               title="Manual Workflow")
    draw_steps(ax, SPYN_STEPS,   x_left=4.5,  color=COLOR_SPYN,
               title="SPYN Workflow")

    # VS label
    ax.text(4.0, 4.0, "vs", ha='center', va='center',
            fontsize=18, fontweight='bold', color='#666666',
            style='italic')

    fig.suptitle("GIPAW NMR Workflow Comparison",
                 fontsize=13, fontweight='bold', y=0.98)

    fig.tight_layout()
    for fmt in ("png", "pdf"):
        path = OUT / f"workflow_comparison.{fmt}"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"Saved: {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
