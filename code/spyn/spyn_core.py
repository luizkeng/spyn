"""
spyn_core.py — Pure, GUI-independent functions for testing and scripting.

These functions contain the mathematical/parsing logic extracted from the
GUI classes so they can be imported and tested without PyQt5 or external
binaries (QE, OpenBabel).
"""

import re
import math
import numpy as np
from scipy.signal import savgol_filter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
K_KCAL = 0.0019872041   # kcal / (mol · K)
K_KJ   = 0.0083144621   # kJ  / (mol · K)


# ---------------------------------------------------------------------------
# Boltzmann distribution
# ---------------------------------------------------------------------------

def boltzmann_distribution(energies, T, unit='kcal/mol'):
    """Return Boltzmann population fractions for a list of conformer energies.

    Parameters
    ----------
    energies : list of float
        Conformer energies in the given unit.
    T : float
        Temperature in Kelvin (must be > 0).
    unit : {'kcal/mol', 'kj/mol'}
        Energy unit.  Default is 'kcal/mol'.

    Returns
    -------
    list of float
        Population fractions in the same order as *energies*.
        Values sum to 1.0.

    Raises
    ------
    TypeError
        If *energies* contains non-numeric values.
    ValueError
        If *T* <= 0.
    """
    if T <= 0:
        raise ValueError("Temperature must be positive (T > 0 K).")
    k = K_KJ if unit == 'kj/mol' else K_KCAL
    beta = 1.0 / (T * k)
    # Shift by minimum energy for numerical stability (invariant to the math)
    e_min = min(float(e) for e in energies)
    exp_terms = [math.exp(-beta * (float(e) - e_min)) for e in energies]
    total = sum(exp_terms)
    return [v / total for v in exp_terms]


# ---------------------------------------------------------------------------
# Lorentzian line shape
# ---------------------------------------------------------------------------

def lorentzian(x_array, peaks, A, width):
    """Compute the superposition of Lorentzian peaks.

    Uses the same formula as the SPYN GUI:
        L(x) = A * width² / (width² + 4 * (x - x0)²)

    where *width* equals the FWHM (full width at half maximum).

    Parameters
    ----------
    x_array : array-like of float
        x-axis values (ppm axis).
    peaks : list of float
        Centre positions (x0) of each Lorentzian peak.
    A : float
        Amplitude (height at each peak centre).
    width : float
        Full width at half maximum (FWHM).  Must be != 0.

    Returns
    -------
    numpy.ndarray
        y values of the superimposed spectrum, same length as *x_array*.

    Raises
    ------
    ValueError
        If *width* == 0.
    """
    if width == 0:
        raise ValueError("width (FWHM) must not be zero.")
    x = np.asarray(x_array, dtype=float)
    y = np.zeros_like(x)
    for x0 in peaks:
        y += (A * width ** 2) / (width ** 2 + 4.0 * (x - x0) ** 2)
    return y


def lorentzian_smoothed(x_array, peaks, A, width, suavization=3):
    """Lorentzian spectrum with Savitzky-Golay smoothing (mirrors GUI output).

    Parameters
    ----------
    suavization : int, odd
        Polynomial order for the Savitzky-Golay filter (window = 51 points).
    """
    y = lorentzian(x_array, peaks, A, width)
    if len(y) >= 51:
        y = savgol_filter(y, 51, suavization)
    return y


# ---------------------------------------------------------------------------
# GIPAW output parser (Quantum ESPRESSO)
# ---------------------------------------------------------------------------

_GIPAW_PATTERN = re.compile(
    r'Atom\s*\d+\s+(\w+)\s+pos:.*?Total\s+sigma:\s*([-\d.]+)',
    re.IGNORECASE
)


def parse_gipaw_output(text, element=None):
    """Parse GIPAW (Quantum ESPRESSO) output text and return shielding tensors.

    Parameters
    ----------
    text : str
        Full content of the GIPAW output file.
    element : str or None
        If given (e.g. ``'C'``, ``'N'``), return only σ_iso values for that
        element.  If ``None``, return all entries as ``(element, sigma)``
        tuples.

    Returns
    -------
    list
        If *element* is specified: list of float σ_iso values.
        If *element* is None: list of (str, float) tuples.

    Examples
    --------
    >>> sigmas = parse_gipaw_output(open('gipaw.out').read(), element='C')
    >>> deltas = [ref - s for s in sigmas]   # chemical shift conversion
    """
    results = []
    for match in _GIPAW_PATTERN.finditer(text):
        elem = match.group(1)
        sigma = float(match.group(2))
        results.append((elem, sigma))

    if element is None:
        return results
    return [sigma for (elem, sigma) in results if elem.upper() == element.upper()]


# ---------------------------------------------------------------------------
# GIAO output parser (Gaussian 09/16)
# ---------------------------------------------------------------------------

_GIAO_PATTERN = re.compile(
    r'^\s*\d+\s+(\w+)\s+Isotropic\s*=\s*([-\d.]+)',
    re.MULTILINE
)


def parse_giao_output(text, element=None):
    """Parse Gaussian GIAO output text and return isotropic shielding values.

    Parameters
    ----------
    text : str
        Full content of the Gaussian .log output file.
    element : str or None
        If given, return only σ_iso values for that element.
        If ``None``, return all entries as ``(element, sigma)`` tuples.

    Returns
    -------
    list
        If *element* is specified: list of float σ_iso values.
        If *element* is None: list of (str, float) tuples.
    """
    results = []
    for match in _GIAO_PATTERN.finditer(text):
        elem = match.group(1)
        sigma = float(match.group(2))
        results.append((elem, sigma))

    if element is None:
        return results
    return [sigma for (elem, sigma) in results if elem.upper() == element.upper()]


# ---------------------------------------------------------------------------
# Chemical shift conversion
# ---------------------------------------------------------------------------

def sigma_to_delta(sigma_values, reference_sigma):
    """Convert isotropic shielding values to chemical shifts.

    δ = σ_ref − σ_iso

    Parameters
    ----------
    sigma_values : list of float
        Calculated isotropic shielding constants (ppm).
    reference_sigma : float
        Isotropic shielding of the reference compound (ppm).

    Returns
    -------
    list of float
        Chemical shift values in ppm.
    """
    return [reference_sigma - s for s in sigma_values]
