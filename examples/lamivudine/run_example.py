"""
run_example.py — Reproducible SPYN example for lamivudine (Form II).

Demonstrates:
1. Boltzmann distribution for a set of conformer energies.
2. Theoretical 13C NMR spectrum from GIPAW shielding tensors.

Requirements: numpy, scipy, matplotlib  (no PyQt5, no Quantum ESPRESSO)
Runtime:      < 30 seconds on standard hardware

Usage:
    python run_example.py
    # → saves example_spectrum.png in the current directory
"""

import pathlib
import sys

import matplotlib
matplotlib.use("Agg")          # headless — no display needed
import matplotlib.pyplot as plt
import numpy as np

# Add package root to path if running without pip install
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from spyn.spyn_core import (
    boltzmann_distribution,
    lorentzian,
    parse_gipaw_output,
    sigma_to_delta,
    K_KCAL,
)

# ---------------------------------------------------------------------------
# 1. Boltzmann distribution — 5 synthetic conformers (kcal/mol)
# ---------------------------------------------------------------------------
conformer_energies = [0.00, 0.42, 0.87, 1.54, 2.31]   # kcal/mol, relative
T = 298.15   # K

populations = boltzmann_distribution(conformer_energies, T=T, unit='kcal/mol')

print("Boltzmann populations at {:.1f} K:".format(T))
for i, (e, p) in enumerate(zip(conformer_energies, populations), 1):
    print(f"  Conformer {i}: E = {e:.2f} kcal/mol   pop = {p*100:.1f} %")
print()

# ---------------------------------------------------------------------------
# 2. Parse GIPAW output — bundled example (lamivudine, QE 6.3)
# ---------------------------------------------------------------------------
EXAMPLES = ROOT / "code" / "spyn" / "examples"
gipaw_text = (EXAMPLES / "gipaw_output.out").read_text(
    encoding="utf-8", errors="replace"
)

# Extract 13C shielding tensors (first formula unit = first 8 C atoms)
all_c_sigmas = parse_gipaw_output(gipaw_text, element='C')
sigma_c = all_c_sigmas[:8]   # one formula unit

# Convert to chemical shifts (δ = σ_ref − σ_iso)
# Reference: glycine Cα σ_iso from the same calculation level ≈ 173.0 ppm
REF_SIGMA = 173.0
delta_c = sigma_to_delta(sigma_c, REF_SIGMA)
print("13C chemical shifts (GIPAW, ppm):")
for i, (s, d) in enumerate(zip(sigma_c, delta_c), 1):
    print(f"  C{i:2d}  sigma_iso = {s:7.2f}   delta_calc = {d:7.2f} ppm")
print()

# ---------------------------------------------------------------------------
# 3. Generate theoretical spectrum with Lorentzian broadening
# ---------------------------------------------------------------------------
x_ppm = np.arange(0, 250, 0.05)
A      = 1.0
width  = 5.0   # FWHM in ppm — typical solid-state 13C

spectrum = lorentzian(x_ppm, peaks=delta_c, A=A, width=width)

# ---------------------------------------------------------------------------
# 4. Plot and save
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left: Boltzmann populations
ax = axes[0]
labels = [f"C{i}" for i in range(1, len(conformer_energies) + 1)]
ax.bar(labels, [p * 100 for p in populations], color="steelblue", alpha=0.8)
ax.set_xlabel("Conformer")
ax.set_ylabel("Population (%)")
ax.set_title("Boltzmann Distribution (298 K)")
ax.set_ylim(0, 100)

# Right: 13C NMR spectrum
ax = axes[1]
ax.plot(x_ppm, spectrum, color="darkred", linewidth=1.2)
for d in delta_c:
    ax.axvline(d, ymin=0, ymax=0.08, color="darkred", linewidth=0.8, alpha=0.6)
ax.set_xlim(250, 0)   # NMR convention: high ppm on left
ax.set_xlabel("Chemical shift (ppm)")
ax.set_ylabel("Intensity (a.u.)")
ax.set_title("Theoretical 13C ss-NMR — Lamivudine (GIPAW)")

fig.tight_layout()
out = pathlib.Path(__file__).parent / "example_spectrum.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"Spectrum saved to: {out}")
plt.close(fig)
