# Comparison with Related Tools

## Feature comparison

| Feature | **SPYN** | CCP-NC toolbox¹ | magresview² | Manual QE workflow |
|---------|----------|-----------------|-------------|-------------------|
| GUI | ✅ PyQt5 | ❌ CLI scripts | ✅ Web/desktop viewer | ❌ Command line |
| Conformational search (integrated) | ✅ GA via OpenBabel | ❌ | ❌ | ❌ |
| Boltzmann population analysis | ✅ | ❌ | ❌ | ❌ (manual) |
| GIPAW calculations (integrated) | ✅ QE 6.3+ | ❌ (external QE) | ❌ | ✅ |
| GIAO result import (Gaussian) | ✅ | ❌ | ❌ | ❌ |
| Lorentzian broadening | ✅ | ❌ | ❌ | ❌ (manual script) |
| Experimental/theoretical overlay | ✅ CSV import | ❌ | ✅ (tensor vis.) | ❌ (manual) |
| Input formats | CIF, MOL, SDF | .magres, CIF | .magres | CIF (manual convert) |
| Output export | PNG, PDF, SVG | CSV, scripts | PNG | Text files |
| License | GPL-3.0 | BSD/LGPL | — | — |
| OS | Linux | Linux/macOS | Linux/macOS/Win | Linux |
| Implementation | Python/PyQt5 | Python | Python/C++ | Shell + Fortran (QE) |
| Learning curve | Low | Medium | Medium | High |
| Available without paywall | ✅ | ✅ | ✅ | ✅ |

¹ Szell PMJ et al. (2021) *Solid State NMR* — CCP-NC toolbox
² Hanwell MD et al. (2012) *J Cheminformatics* — magresview

---

## Usability benchmark: steps to complete a GIPAW NMR calculation

### Without SPYN (manual workflow)

1. Obtain CIF file from CCDC or CSD
2. Convert CIF to QE format with `cif2qe` or manual editing
3. Download correct pseudopotentials
4. Edit SCF input manually (cutoff, k-points, convergence)
5. Run `mpirun ... pw.x < scf.in > scf.out` in terminal
6. Verify convergence (`grep 'convergence' scf.out`)
7. Edit GIPAW input manually
8. Run `mpirun ... gipaw.x < gipaw.in > gipaw.out`
9. Parse output (`grep 'Total sigma' gipaw.out`)
10. Compute δ = σ_ref − σ_iso manually (spreadsheet/script)
11. Plot spectrum (separate matplotlib script or third-party software)

**Total: ≥ 11 steps — requires expertise in QE input syntax, Linux
command line, and NMR crystallography conventions.**

### With SPYN

1. Open SPYN (`python spyn_main.py`)
2. File → Import CIF
3. Set SCF parameters (3 numeric fields + k-point choice)
4. Click **Calculate SCF**
5. Click **Calculate GIPAW**
6. Spectro-NMR tab: enter reference σ → click **Plot**

**Total: 6 steps — no knowledge of QE input syntax required.**
