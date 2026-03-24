"""Tests for spyn_core.boltzmann_distribution."""

import math
import pytest
import numpy as np
from spyn.spyn_core import boltzmann_distribution, K_KCAL


class TestBoltzmannDistribution:

    def test_sum_to_one(self):
        """Population fractions must sum to exactly 1.0."""
        energies = [0.0, 1.0, 2.0, 5.0]
        pops = boltzmann_distribution(energies, T=298.15)
        assert abs(sum(pops) - 1.0) < 1e-10

    def test_lowest_energy_most_populated(self):
        """The conformer with the lowest energy must have the highest population."""
        energies = [0.0, 2.0, 5.0]
        pops = boltzmann_distribution(energies, T=298.15)
        assert pops[0] == max(pops)

    def test_energy_shift_invariance(self):
        """Adding a constant to all energies must not change populations."""
        energies = [0.0, 1.0, 3.0]
        shifted = [e + 100.0 for e in energies]
        pops1 = boltzmann_distribution(energies, T=298.15)
        pops2 = boltzmann_distribution(shifted, T=298.15)
        np.testing.assert_allclose(pops1, pops2, rtol=1e-8)

    def test_single_conformer(self):
        """A single conformer must have population = 1.0."""
        pops = boltzmann_distribution([0.0], T=298.15)
        assert len(pops) == 1
        assert abs(pops[0] - 1.0) < 1e-10

    def test_known_result_kcal(self):
        """Two conformers separated by exactly kT must have ratio ≈ e ≈ 2.718."""
        T = 298.15
        dE = K_KCAL * T          # ΔE = 1 kT  (kcal/mol)
        pops = boltzmann_distribution([0.0, dE], T=T, unit='kcal/mol')
        ratio = pops[0] / pops[1]
        assert abs(ratio - math.e) < 0.01

    def test_kj_unit(self):
        """kj/mol unit must give the same relative populations as kcal/mol."""
        energies_kcal = [0.0, 1.0, 3.0]
        energies_kj = [e * 4.184 for e in energies_kcal]   # 1 kcal = 4.184 kJ
        pops_kcal = boltzmann_distribution(energies_kcal, T=298.15, unit='kcal/mol')
        pops_kj   = boltzmann_distribution(energies_kj,   T=298.15, unit='kj/mol')
        np.testing.assert_allclose(pops_kcal, pops_kj, rtol=1e-6)

    def test_negative_energies(self):
        """Negative energies (kcal/mol) must be handled without error."""
        energies = [-5.0, -3.0, -1.0]
        pops = boltzmann_distribution(energies, T=298.15)
        assert abs(sum(pops) - 1.0) < 1e-10
        assert pops[0] == max(pops)   # most negative = lowest energy = most populated

    def test_high_temperature_equal_populations(self):
        """At very high T all populations should converge to equal fractions."""
        energies = [0.0, 1.0, 2.0]
        pops = boltzmann_distribution(energies, T=1e7)
        expected = 1.0 / len(energies)
        for p in pops:
            assert abs(p - expected) < 1e-4

    def test_invalid_temperature(self):
        """T <= 0 must raise ValueError."""
        with pytest.raises(ValueError):
            boltzmann_distribution([0.0, 1.0], T=0)
        with pytest.raises(ValueError):
            boltzmann_distribution([0.0, 1.0], T=-100)

    def test_non_numeric_input_raises(self):
        """Non-numeric energies must raise TypeError."""
        with pytest.raises((TypeError, ValueError)):
            boltzmann_distribution(["a", "b"], T=298.15)
