"""Tests for spyn_core.parse_gipaw_output and sigma_to_delta."""

import pytest
from spyn.spyn_core import parse_gipaw_output, sigma_to_delta


# Expected values from the bundled gipaw_output.out (lamivudine, QE 6.3)
# First 8 Carbon atoms in the unit cell all have sigma ≈ 13.68 ppm
EXPECTED_C_SIGMA_FIRST = [13.68, 13.68, 13.68, 13.68, 13.69, 13.69, 13.68, 13.68]


class TestParseGIPAW:

    def test_carbon_count(self, gipaw_output_text):
        """The example file has 64 Carbon atoms (8 formula units × 8 C)."""
        values = parse_gipaw_output(gipaw_output_text, element='C')
        assert len(values) == 64

    def test_carbon_first_values(self, gipaw_output_text):
        """First 8 Carbon sigma values must match known values within ±0.01 ppm."""
        values = parse_gipaw_output(gipaw_output_text, element='C')
        for got, expected in zip(values[:8], EXPECTED_C_SIGMA_FIRST):
            assert abs(got - expected) < 0.01, f"Got {got}, expected {expected}"

    def test_element_filter_sulfur(self, gipaw_output_text):
        """Filtering by 'S' must return only sulfur shielding values."""
        values = parse_gipaw_output(gipaw_output_text, element='S')
        assert len(values) > 0
        # All S sigma values in example are around 454 ppm
        for v in values:
            assert 400 < v < 500, f"Unexpected S sigma: {v}"

    def test_no_element_filter_returns_tuples(self, gipaw_output_text):
        """Without element filter, result must be list of (element, sigma) tuples."""
        results = parse_gipaw_output(gipaw_output_text, element=None)
        assert len(results) > 0
        for entry in results[:5]:
            assert isinstance(entry, tuple)
            assert len(entry) == 2
            assert isinstance(entry[0], str)
            assert isinstance(entry[1], float)

    def test_empty_text_returns_empty_list(self):
        """Empty input must return empty list without raising."""
        assert parse_gipaw_output("", element='C') == []

    def test_truncated_text_no_crash(self):
        """Truncated/partial output must return partial results without crash."""
        partial = "     Atom  1  C   pos: (  0.1  0.2  0.3)  Total sigma:         42.0\n"
        values = parse_gipaw_output(partial, element='C')
        assert values == [42.0]

    def test_case_insensitive_element(self, gipaw_output_text):
        """Element matching must be case-insensitive ('c' == 'C')."""
        upper = parse_gipaw_output(gipaw_output_text, element='C')
        lower = parse_gipaw_output(gipaw_output_text, element='c')
        assert upper == lower

    def test_sigma_to_delta_conversion(self, gipaw_output_text):
        """sigma_to_delta must correctly apply δ = σ_ref − σ_iso."""
        sigmas = parse_gipaw_output(gipaw_output_text, element='C')[:4]
        # Using glycine Cα reference sigma = 173.0 ppm (common solid-state ref)
        ref = 173.0
        deltas = sigma_to_delta(sigmas, ref)
        assert len(deltas) == len(sigmas)
        for delta, sigma in zip(deltas, sigmas):
            assert abs(delta - (ref - sigma)) < 1e-9
