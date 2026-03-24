"""Tests for spyn_core.lorentzian."""

import math
import pytest
import numpy as np
from spyn.spyn_core import lorentzian


class TestLorentzian:

    def test_maximum_value(self):
        """At the peak centre x = x0, y must equal A."""
        x = np.array([5.0])
        y = lorentzian(x, peaks=[5.0], A=1.0, width=1.0)
        assert abs(y[0] - 1.0) < 1e-10

    def test_fwhm_half_maximum(self):
        """At x = x0 ± width/2, y must equal A/2 (definition of FWHM)."""
        x0, A, w = 10.0, 2.0, 4.0
        for x_half in [x0 + w / 2, x0 - w / 2]:
            y = lorentzian(np.array([x_half]), peaks=[x0], A=A, width=w)
            assert abs(y[0] - A / 2) < 1e-6

    def test_symmetry(self):
        """The curve must be symmetric around each peak centre."""
        x0, A, w = 50.0, 1.5, 2.0
        offsets = np.linspace(0.1, 10.0, 50)
        x_left  = np.array([x0 - d for d in offsets])
        x_right = np.array([x0 + d for d in offsets])
        y_left  = lorentzian(x_left,  peaks=[x0], A=A, width=w)
        y_right = lorentzian(x_right, peaks=[x0], A=A, width=w)
        np.testing.assert_allclose(y_left, y_right, rtol=1e-10)

    def test_analytical_integral(self):
        """Numerical integral must approximate π * A * width / 2."""
        x0, A, w = 100.0, 1.0, 5.0
        x = np.linspace(x0 - 500 * w, x0 + 500 * w, 200_000)
        y = lorentzian(x, peaks=[x0], A=A, width=w)
        numerical = np.trapezoid(y, x)
        analytical = math.pi * A * w / 2
        assert abs(numerical - analytical) / analytical < 1e-3

    def test_superposition_linearity(self):
        """Superposition of two peaks must equal the sum of individual peaks."""
        x = np.linspace(0, 300, 10_000)
        A, w = 1.0, 2.0
        y_sum  = lorentzian(x, peaks=[80.0, 160.0], A=A, width=w)
        y_p1   = lorentzian(x, peaks=[80.0],         A=A, width=w)
        y_p2   = lorentzian(x, peaks=[160.0],        A=A, width=w)
        np.testing.assert_allclose(y_sum, y_p1 + y_p2, rtol=1e-10)

    def test_width_zero_raises(self):
        """width = 0 must raise ValueError."""
        with pytest.raises(ValueError):
            lorentzian(np.array([1.0, 2.0]), peaks=[1.5], A=1.0, width=0)

    def test_multiple_peaks_count(self):
        """Output length must equal input x_array length regardless of peak count."""
        x = np.linspace(0, 200, 500)
        y = lorentzian(x, peaks=[50.0, 100.0, 150.0], A=1.0, width=2.0)
        assert len(y) == len(x)
