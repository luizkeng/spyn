"""
SPYN — GUI platform for NMR crystallography workflows.

Provides conformational search (OpenBabel genetic algorithm), Boltzmann
distribution analysis, solid-state NMR calculations via GIPAW
(Quantum ESPRESSO), GIAO result import (Gaussian), and spectral
visualisation with Lorentzian broadening.

References
----------
DOI: 10.5281/zenodo.4019023
GitHub: https://github.com/jeffrichardchemistry/spyn
"""

__version__ = "2.0.0"
__authors__ = [
    "Jefferson Richard Dias da Silva",
    "Luiz Henrique Keng Queiroz Junior",
]
__license__ = "GPL-3.0"
__doi__ = "10.5281/zenodo.4019023"

from spyn.spyn_core import (
    boltzmann_distribution,
    lorentzian,
    lorentzian_smoothed,
    parse_gipaw_output,
    parse_giao_output,
    sigma_to_delta,
    K_KCAL,
    K_KJ,
)

__all__ = [
    "boltzmann_distribution",
    "lorentzian",
    "lorentzian_smoothed",
    "parse_gipaw_output",
    "parse_giao_output",
    "sigma_to_delta",
    "K_KCAL",
    "K_KJ",
]
