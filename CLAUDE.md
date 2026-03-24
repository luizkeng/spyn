# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spyn** is a Python/PyQt5 desktop GUI application for computational chemistry workflows:
- Conformational search via genetic algorithm (OpenBabel)
- Boltzmann distribution calculations
- Solid-state NMR (ss-NMR) calculations using GIPAW (Quantum-Espresso)
- GIAO calculations (Gaussian output import)
- Spectral visualization with Lorentzian broadening

Runs on Linux only (tested on Debian, Ubuntu, Linux Mint, Elementary OS).

## Running the Application

```bash
# From the source directory
cd code/spyn
python3 spyn_main.py

# Or via the splash screen initializer
python3 spyninit.py
```

## Installation

```bash
cd Spyn_1.0_alpha
python3 install_ui.py
```

System dependencies (Debian-based): `gawk gfortran openmpi-bin openmpi-doc libopenmpi-dev xterm openbabel jmol python3-dev python3-pip python3-pyqt5`

Python dependencies: `PyQt5 matplotlib pandas scipy numpy`

## No Build/Test Infrastructure

There is currently **no test suite, no linting config, and no CI/CD**. There is also no `setup.py` or `pyproject.toml` — the project is distributed as a `.tar.gz`.

## Architecture

All source code lives in `code/spyn/`. The main entry point is `spyn_main.py` (QMainWindow subclass). The UI is defined in `spynUixml.ui` and auto-generated into `spyn_ui.py`.

### Key Modules

| Module | Role |
|--------|------|
| `spyn_main.py` | Main window, event wiring, orchestration |
| `spyn_ui.py` | Auto-generated PyQt5 UI (do not edit manually) |
| `csGA.py` | Genetic algorithm conformer search via OpenBabel |
| `energy.py` | Conformer energy evaluation (`obenergy`) |
| `boltz.py` | Boltzmann distribution from energy rankings |
| `pwscfnmr.py` | Quantum-Espresso SCF + GIPAW calculation management |
| `grepout.py` | Parses QE output files (grep-based) |
| `giao.py` | Gaussian GIAO output import and parsing |
| `plots.py` | Matplotlib spectral plots with Lorentzian broadening |
| `imports.py` | PyQt5 file dialogs for importing various file types |
| `dir.py` / `direct.py` | Directory and file path management |
| `killprocess.py` | Process/terminal management |
| `mplwidget.py` | Embedded Matplotlib widget for PyQt5 |

### External Binary Dependencies

| Executable | Purpose |
|-----------|---------|
| `obabel` | Conformer generation |
| `obenergy` | Conformer energy evaluation |
| `pw` (symlink to `pw.x`) | Quantum-Espresso SCF |
| `gipaw` (symlink to `gipaw.x`) | GIPAW NMR calculation |
| `xterm` | Terminal for subprocess execution |
| `jmol` | Optional molecular visualization |

### Typical Workflow

1. **Conformational Search:** Import CIF/MOL/SDF → run `csGA.py` (calls `obabel`) → energy ranking via `energy.py` → Boltzmann weighting via `boltz.py`
2. **ss-NMR with GIPAW:** Import CIF → generate QE input (shell scripts in `scripts/`) → run SCF then GIPAW via `pwscfnmr.py` → parse output via `grepout.py` → plot via `plots.py`
3. **GIAO (Gaussian):** Import `.log` file via `imports.py` → parse via `giao.py` → overlay with experimental CSV data → plot via `plots.py`

### Shell Scripts

The `scripts/` directory contains shell scripts for generating Quantum-Espresso input files (K-point grids, SCF parameters, etc.), invoked from `pwscfnmr.py`.

### Example Data

Sample files are in `code/spyn/examples/`: lamivudine conformers (`.sdf`), glycine (`.cif`), GIPAW output (`.out`), GIAO output (`.log`), and experimental NMR data (`.csv`).
