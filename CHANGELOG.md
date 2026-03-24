# Changelog

All notable changes to SPYN are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

---

## [Unreleased] — v2.0.0

### Added
- `spyn_core.py`: pure-Python functions (`boltzmann_distribution`,
  `lorentzian`, `parse_gipaw_output`, `parse_giao_output`,
  `sigma_to_delta`) importable without PyQt5
- `spyn/__init__.py`: proper package initialisation with version, authors,
  and DOI metadata
- `setup.py` and `pyproject.toml`: standard Python packaging
- `requirements.txt` and `environment.yml`: reproducible dependency specs
- `tests/`: pytest test suite covering Boltzmann, Lorentzian, GIPAW
  parser, and GIAO parser modules (≥ 60 % coverage)
- `.github/workflows/ci.yml`: GitHub Actions CI on Python 3.8 / 3.9 / 3.10
- `examples/lamivudine/run_example.py`: headless reproducible example
  (no QE required, < 30 s runtime)
- `docs/`: installation guide, quickstart tutorial, API module reference,
  and tool comparison table
- `docs/figures/generate_workflow_comparison.py`: workflow comparison figure
  (manual vs SPYN — 11 steps vs 6 steps)
- `.zenodo.json`: Zenodo v2.0.0 metadata for automatic DOI minting
- `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`

### Fixed
- `scripts/scraping.sh`: removed hardcoded absolute path
  (`/home/jefferson/Dropbox/...`); now accepts log path as argument `$1`

---

## [1.0.0] — 2020-09-08

Initial release deposited on Zenodo (DOI: 10.5281/zenodo.4019024).

### Features
- Conformational search with genetic algorithm (OpenBabel)
- Boltzmann distribution calculation (manual and automatic modes)
- Solid-state NMR via GIPAW (Quantum ESPRESSO 6.3 integration)
- GIAO result import (Gaussian 09 `.log` files)
- Lorentzian broadening with Savitzky-Golay smoothing
- Experimental NMR overlay (CSV import)
- PyQt5 GUI with four tabs
- Jmol integration for 3D molecular visualisation
- Tested on Debian 10, Ubuntu 18.04 LTS, Linux Mint 19.3, Elementary OS 5.1
