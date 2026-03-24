# Lamivudine Example

This directory contains a fully reproducible example of SPYN's core
numerical functions — **no Quantum ESPRESSO installation required**.

## What it demonstrates

1. **Boltzmann distribution** — population analysis for 5 conformers at 298 K.
2. **GIPAW output parsing** — reading `¹³C` shielding tensors from a real
   Quantum ESPRESSO GIPAW calculation (lamivudine Form II, bundled in
   `code/spyn/examples/gipaw_output.out`).
3. **Lorentzian broadening** — generating a theoretical solid-state `¹³C`
   NMR spectrum from the computed shielding tensors.

The bundled GIPAW output was produced with Quantum ESPRESSO 6.3 / GIPAW,
using PBE functional and `pbe-tm-new-gipaw-dc` pseudopotentials, on a
4×4×1 k-point grid with 100 Ry plane-wave cutoff.

## Quick start

```bash
# From the repository root:
conda activate spyn-env        # or: pip install -e .
cd examples/lamivudine
python run_example.py
# → prints Boltzmann populations and 13C shifts, saves example_spectrum.png
```

Expected output:

```
Boltzmann populations at 298.1 K:
  Conformer 1: E = 0.00 kcal/mol   pop = 51.0 %
  Conformer 2: E = 0.42 kcal/mol   pop = 24.1 %
  ...

13C chemical shifts (GIPAW, ppm):
  C 1  σ_iso =   13.68   δ_calc =  159.32 ppm
  ...

Spectrum saved to: .../examples/lamivudine/example_spectrum.png
```

## Files

| File | Description |
|------|-------------|
| `run_example.py` | Main reproducible script |
| `example_spectrum.png` | Generated output (created on first run) |

The actual input data files (`gipaw_output.out`, `giao_output.log`,
`alglycine.cif`, `lamivudine_allconfs.sdf`) live in
`code/spyn/examples/` and are shared with the GUI application.
