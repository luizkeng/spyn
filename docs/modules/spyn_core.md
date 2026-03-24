# Module: spyn_core

Pure, GUI-independent functions for scripting and testing.
Import: `from spyn.spyn_core import <function>`
All functions in this module have **no dependency on PyQt5** and can be
used in headless environments (servers, Jupyter notebooks, CI pipelines).

---

## `boltzmann_distribution(energies, T, unit='kcal/mol')`

Returns Boltzmann population fractions for a conformer ensemble.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `energies` | list of float | Conformer energies (relative values are fine) |
| `T` | float | Temperature in Kelvin |
| `unit` | str | `'kcal/mol'` (default) or `'kj/mol'` |

**Returns:** `list of float` — fractions summing to 1.0.

**Example:**
```python
from spyn.spyn_core import boltzmann_distribution

energies = [0.0, 0.42, 0.87]  # kcal/mol
pops = boltzmann_distribution(energies, T=298.15)
# pops ≈ [0.510, 0.312, 0.178]
print([f"{p*100:.1f}%" for p in pops])
```

---

## `lorentzian(x_array, peaks, A, width)`

Computes the superposition of Lorentzian peaks (same formula as the GUI).

`L(x) = A · width² / (width² + 4·(x − x₀)²)`

where `width` = FWHM.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `x_array` | array-like | x-axis values (ppm) |
| `peaks` | list of float | Peak centre positions |
| `A` | float | Amplitude at each peak centre |
| `width` | float | FWHM in ppm |

**Returns:** `numpy.ndarray` same length as `x_array`.

**Example:**
```python
import numpy as np
from spyn.spyn_core import lorentzian

x = np.arange(0, 250, 0.1)
y = lorentzian(x, peaks=[50.0, 130.0, 170.0], A=1.0, width=3.0)
```

---

## `parse_gipaw_output(text, element=None)`

Parses Quantum ESPRESSO GIPAW output and returns σ_iso shielding values.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `text` | str | Full content of the GIPAW `.out` file |
| `element` | str or None | Element symbol (e.g. `'C'`). `None` → return all as `(elem, sigma)` tuples |

**Returns:** `list of float` if element specified; `list of (str, float)` otherwise.

**Example:**
```python
from spyn.spyn_core import parse_gipaw_output, sigma_to_delta

text = open("gipaw.out").read()
sigmas = parse_gipaw_output(text, element='C')
deltas = sigma_to_delta(sigmas, reference_sigma=173.0)
```

---

## `parse_giao_output(text, element=None)`

Parses Gaussian 09/16 GIAO output and returns isotropic shielding values.

Same interface as `parse_gipaw_output`.

---

## `sigma_to_delta(sigma_values, reference_sigma)`

Converts isotropic shielding constants to chemical shifts.

`δ = σ_ref − σ_iso`

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `sigma_values` | list of float | Calculated σ_iso values (ppm) |
| `reference_sigma` | float | σ_iso of the reference compound (ppm) |

**Returns:** `list of float` — chemical shifts in ppm.

---

## Constants

| Name | Value | Description |
|------|-------|-------------|
| `K_KCAL` | `0.0019872041` | Boltzmann constant in kcal/(mol·K) |
| `K_KJ` | `0.0083144621` | Boltzmann constant in kJ/(mol·K) |
