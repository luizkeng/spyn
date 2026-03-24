[![CI](https://github.com/jeffrichardchemistry/spyn/actions/workflows/ci.yml/badge.svg)](https://github.com/jeffrichardchemistry/spyn/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4019023.svg)](https://doi.org/10.5281/zenodo.4019023)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

# SPYN

**SPYN** is an open-source Python/PyQt5 desktop application for NMR crystallography workflows. It provides a unified graphical interface for four interconnected tasks that typically require separate tools and manual scripting:

1. **Conformational search** — genetic algorithm via OpenBabel to generate and rank conformer ensembles from CIF, MOL, or SDF input files.
2. **Boltzmann distribution** — population analysis of conformers at a user-defined temperature (kcal/mol or kJ/mol), with automatic import from the conformer search output.
3. **Solid-state NMR (GIPAW)** — automated generation of Quantum ESPRESSO SCF and GIPAW input files from CIF structures, execution monitoring, and output parsing to extract isotropic shielding tensors (σ_iso).
4. **Spectral visualisation** — conversion of calculated σ_iso to chemical shifts (δ = σ_ref − σ_iso), Lorentzian broadening with Savitzky-Golay smoothing, and overlay of theoretical and experimental spectra (CSV import).

SPYN reduces a typical GIPAW NMR workflow from ≥ 11 manual command-line steps to 6 GUI interactions, making solid-state NMR calculations accessible to researchers without extensive computational chemistry expertise.

## Quick install

```bash
git clone https://github.com/jeffrichardchemistry/spyn.git
cd spyn/Spyn_2.0_alpha
python3 install_ui.py
```

The graphical installer handles everything automatically: system packages,
Python dependencies, Quantum ESPRESSO 6.3 compilation with GIPAW support,
and system links (`pw`, `gipaw`). See [docs/installation.md](docs/installation.md) for details.

## Quick start — reproducible example (no QE required)

```bash
cd examples/lamivudine
python run_example.py
# → prints Boltzmann populations + 13C shifts, saves example_spectrum.png
```

## Quick start — full GUI workflow

```bash
cd code/spyn
python spyn_main.py
```

Then follow the tabs: **Conformational Searching → Boltzmann Distribution → ss-NMR → Spectro-NMR**.
See [docs/quickstart.md](docs/quickstart.md) for a step-by-step tutorial.

## Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| Python | ≥ 3.6 | 3.8 recommended |
| PyQt5 | ≥ 5.12 | GUI framework |
| NumPy / SciPy / Pandas / Matplotlib | see requirements.txt | Pure-Python stack |
| OpenBabel | ≥ 3.0 | Conformer search (`obabel`, `obenergy`) |
| Quantum ESPRESSO + GIPAW | ≥ 6.3 | ss-NMR calculations (`pw`, `gipaw`) |
| xterm | any | Terminal emulator for QE subprocess |
| Jmol | any | Optional 3D molecular viewer |
| OS | Linux | Tested: Debian 10/11, Ubuntu 18–22, Mint 19–20, Elementary OS 5 |

## Documentation

- [Installation guide](docs/installation.md) — step-by-step for Ubuntu/Debian/Mint including QE compilation
- [Quickstart tutorial](docs/quickstart.md) — walkthrough of all four GUI tabs
- [API modules](docs/modules/) — documented pure-Python functions for scripting

## How to cite

If you use SPYN in published work, please cite:

```bibtex
@software{spyn2020,
  author  = {Dias da Silva, Jefferson Richard and
             Keng Queiroz Junior, Luiz Henrique},
  title   = {{SPYN}: An Open-Source Python Platform with GUI
             for NMR Crystallography},
  year    = {2020},
  doi     = {10.5281/zenodo.4019023},
  url     = {https://github.com/jeffrichardchemistry/spyn},
  license = {GPL-3.0}
}
```

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.
