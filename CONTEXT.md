# SPYN — Project Context

This file documents the current architecture, recent changes, and development
decisions for contributors and collaborators.

---

## Version history

| Version | Date | Summary |
|---------|------|---------|
| v1.0.0 | Sep 2020 | Initial release — DOI: 10.5281/zenodo.4019024 |
| v2.0.0 | Mar 2026 | Publication-ready release (see changes below) |

---

## Changes in v2.0.0

### New files

| File | Purpose |
|------|---------|
| `code/spyn/__init__.py` | Package initialisation — version 2.0.0, authors, DOI |
| `code/spyn/spyn_core.py` | Pure-Python functions independent of PyQt5 (see below) |
| `setup.py` | Standard Python packaging |
| `pyproject.toml` | PEP 517/518 build config, pytest and coverage settings |
| `requirements.txt` | Pinned runtime and development dependencies |
| `environment.yml` | Conda environment (Python 3.9, openbabel via conda-forge) |
| `tests/conftest.py` | Shared pytest fixtures pointing to bundled example files |
| `tests/test_boltzmann.py` | 10 unit tests for `boltzmann_distribution` |
| `tests/test_lorentz.py` | 7 unit tests for `lorentzian` |
| `tests/test_parser_gipaw.py` | 8 unit tests for `parse_gipaw_output` |
| `tests/test_parser_giao.py` | 9 unit tests for `parse_giao_output` |
| `.github/workflows/ci.yml` | GitHub Actions CI — Python 3.9 / 3.10 / 3.11 |
| `.zenodo.json` | Zenodo v2.0.0 metadata — two authors, GPL-3.0, keywords |
| `examples/lamivudine/run_example.py` | Headless reproducible example (no QE required) |
| `docs/installation.md` | Full installation guide including automated installer |
| `docs/quickstart.md` | Step-by-step tutorial for all four GUI tabs |
| `docs/modules/spyn_core.md` | API reference for pure-Python functions |
| `docs/comparison.md` | Feature comparison vs CCP-NC toolbox and magresview |
| `docs/figures/generate_workflow_comparison.py` | Matplotlib figure: 11-step manual vs 6-step SPYN workflow |
| `CHANGELOG.md` | Keep-a-Changelog format, v1.0.0 and v2.0.0 |
| `CONTRIBUTING.md` | Contribution guidelines |
| `.gitignore` | Excludes build artefacts, cache, coverage files |

### Modified files

| File | Change |
|------|--------|
| `README.md` | v2.0.0: complete rewrite — badges, quick install, requirements, how-to-cite BibTeX. v2.0.1: expanded "Installation and setup" section documenting `install_ui.py` as first-class contribution — competitive positioning paragraph, two-stage ASCII flowchart of the full automation chain, summary table mapping 9 automated phases to manual equivalents (6 user actions vs ≥ 20 manual commands), CI/testing table promoted to README visibility |
| `code/spyn/scripts/scraping.sh` | Removed hardcoded absolute path `/home/jefferson/Dropbox/...`; now accepts log path as argument `$1` |

### Renamed

| Old | New |
|-----|-----|
| `Spyn_1.0_alpha/` | `Spyn_2.0_alpha/` |

---

## Architecture

All source code lives in `code/spyn/`. The application is started from
`spyn_main.py` (QMainWindow). The UI is defined in `spynUixml.ui` and
auto-generated into `spyn_ui.py` — do not edit `spyn_ui.py` manually.

### Module overview

| Module | Role |
|--------|------|
| `spyn_main.py` | Main window, event wiring |
| `spyn_ui.py` | Auto-generated PyQt5 UI — do not edit |
| `spyn_core.py` | **Pure functions — testable without PyQt5 or external binaries** |
| `csGA.py` | Genetic algorithm conformer search (OpenBabel) |
| `energy.py` | Conformer energy evaluation (`obenergy`) |
| `boltz.py` | Boltzmann distribution (GUI class) |
| `pwscfnmr.py` | Quantum ESPRESSO SCF + GIPAW interface |
| `grepout.py` | QE output parsing |
| `giao.py` | Gaussian GIAO input generation |
| `plots.py` | Spectral plots with Lorentzian broadening |
| `imports.py` | File import dialogs |
| `dir.py` / `direct.py` | Directory and path management |
| `killprocess.py` | Process termination |
| `mplwidget.py` | Embedded Matplotlib widget |

### `spyn_core.py` — pure functions

These functions contain the mathematical and parsing logic extracted
from the GUI classes so they can be imported and tested without PyQt5:

| Function | Description |
|----------|-------------|
| `boltzmann_distribution(energies, T, unit)` | Boltzmann population fractions |
| `lorentzian(x_array, peaks, A, width)` | Lorentzian peak superposition |
| `lorentzian_smoothed(...)` | Lorentzian + Savitzky-Golay smoothing |
| `parse_gipaw_output(text, element)` | Parse QE GIPAW σ_iso values |
| `parse_giao_output(text, element)` | Parse Gaussian GIAO σ_iso values |
| `sigma_to_delta(sigma_values, reference_sigma)` | σ_iso → δ conversion |

### External binary dependencies

| Executable | Purpose | Installed by |
|-----------|---------|-------------|
| `pw` | Quantum ESPRESSO SCF | `simbolic.sh` → `/usr/bin/pw` |
| `gipaw` | GIPAW NMR | `simbolic.sh` → `/usr/bin/gipaw` |
| `obabel` | Conformer generation | `dependency.sh` |
| `obenergy` | Conformer energy | `dependency.sh` |
| `xterm` | Terminal for QE subprocesses | `dependency.sh` |
| `jmol` | 3D molecular viewer (optional) | `dependency.sh` |

---

## Installation flow

```
python3 Spyn_2.0_alpha/install_ui.py
    └── GUI: user selects directory
        └── extracts spyn.tar.gz
            └── xterm runs install_spyn.py
                ├── dependency.sh      → system + Python packages
                ├── qe-7.3.tar.gz      → extract + compile pw.x + gipaw.x (bundled)
                └── simbolic.sh        → /usr/bin/pw  /usr/bin/gipaw
```

> **Branch `QE_7.x_upgrade`** — Migração do installer do QE 6.3 para QE 7.3.
> O GIPAW está integrado ao QE 7.x (não é mais um plugin externo), eliminando
> o passo `makemaster.sh` e o diretório `qe-gipaw-6.3/`. Ver detalhes abaixo.

---

## Tests

```bash
# Run from repository root with the project venv active
pytest tests/ -v --cov=spyn
```

| Test module | Cases | Coverage target |
|-------------|-------|-----------------|
| `test_boltzmann.py` | 10 | 100 % of `boltzmann_distribution` |
| `test_lorentz.py` | 7 | 100 % of `lorentzian` |
| `test_parser_gipaw.py` | 8 | ≥ 80 % of `parse_gipaw_output` |
| `test_parser_giao.py` | 9 | ≥ 80 % of `parse_giao_output` |
| **Total** | **34** | **92.86 % (spyn_core.py)** |

Coverage configuration in `pyproject.toml` omits GUI modules (PyQt5-dependent)
from measurement — only `spyn_core.py` and `__init__.py` are measured.

---

## CI/CD

GitHub Actions at `.github/workflows/ci.yml`:
- Trigger: push/PR to `master`, `main`, `develop`
- Matrix: Python 3.9, 3.10, 3.11 (Ubuntu latest)
- Steps: `pip install -e .` → `pytest --cov` → Codecov upload (3.9 only)
- Minimum Python: **3.9** (NumPy 2.0 requirement for `np.trapezoid`)

---

## QE 7.x upgrade (branch `QE_7.x_upgrade`)

Compatibilidade com Quantum ESPRESSO 7.3, avaliada em Mar 2026.

### Mudanças aplicadas

| Arquivo | Mudança |
|---------|---------|
| `install_spyn.py` | `qe-6.3` → `qe-7.3`; removido `--enable-shared` (eliminado no 7.x); removidas 3 linhas do fluxo GIPAW externo |
| `simbolic.sh` | Caminho do `gipaw.x` corrigido — agora em `qe-7.3/bin/` junto com `pw.x` |
| `pwscfnmr.py` | Removido `spline_ps = .true.` do input GIPAW (keyword descontinuada no 7.x) |
| `makemaster.sh` | **Deletado** — obsoleto; GIPAW agora é nativo no QE 7.x |

### Motivação técnica

No QE 7.0+, o GIPAW foi integrado ao pacote principal (`GIPAW/` dentro do tarball).
O fluxo anterior exigia baixar `qe-gipaw-6.3` separado, configurar com
`--with-qe-source` e compilar em etapa distinta. No QE 7.x, basta
`make gipaw` após o `configure` padrão.

---

## Pending before journal submission

- [ ] Create GitHub release v2.0.0 → triggers Zenodo DOI generation
- [ ] Add Codecov token to GitHub Secrets → enables coverage badge
- [ ] Update README BibTeX with the actual v2.0.0 Zenodo DOI
- [ ] Add comparison section to manuscript (see `docs/comparison.md`)
- [ ] Update Availability table in manuscript with CI/test metadata
- [ ] Add "Installation and Setup" section to the manuscript mirroring README — document `install_ui.py` as first-class contribution with the two-stage flowchart and summary table (see README.md for reference text)
