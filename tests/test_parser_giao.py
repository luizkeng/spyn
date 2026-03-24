"""Tests for spyn_core.parse_giao_output."""

import pytest
from spyn.spyn_core import parse_giao_output, sigma_to_delta


# Expected isotropic shielding for C atoms in the bundled Gaussian log
# (lamivudine, B3LYP/cc-pVTZ GIAO, Gaussian 09)
EXPECTED_C_ISOTROPIC = [70.5223, 95.2817, 100.1274, 30.6488,
                         96.9030, 147.0682, 135.3597, 88.1825]


class TestParseGIAO:

    def test_carbon_count(self, giao_output_text):
        """The example log must have exactly 8 Carbon isotropic values."""
        values = parse_giao_output(giao_output_text, element='C')
        assert len(values) == 8

    def test_carbon_values(self, giao_output_text):
        """All 8 Carbon σ_iso values must match expected within ±0.001 ppm."""
        values = parse_giao_output(giao_output_text, element='C')
        for got, expected in zip(values, EXPECTED_C_ISOTROPIC):
            assert abs(got - expected) < 0.001, f"Got {got}, expected {expected}"

    def test_element_filter_nitrogen(self, giao_output_text):
        """Filtering by 'N' must return only nitrogen shielding values."""
        values = parse_giao_output(giao_output_text, element='N')
        assert len(values) > 0

    def test_element_filter_oxygen(self, giao_output_text):
        """Filtering by 'O' must return only oxygen shielding values."""
        values = parse_giao_output(giao_output_text, element='O')
        assert len(values) > 0

    def test_no_element_filter_returns_tuples(self, giao_output_text):
        """Without element filter, result must be list of (element, sigma) tuples."""
        results = parse_giao_output(giao_output_text, element=None)
        assert len(results) > 0
        for entry in results[:5]:
            assert isinstance(entry, tuple)
            assert len(entry) == 2
            assert isinstance(entry[0], str)
            assert isinstance(entry[1], float)

    def test_empty_text_returns_empty_list(self):
        """Empty input must return empty list without raising."""
        assert parse_giao_output("", element='C') == []

    def test_truncated_text_no_crash(self):
        """A single valid line must be parsed correctly."""
        line = "  8  C    Isotropic =    70.5223   Anisotropy =    86.1999\n"
        values = parse_giao_output(line, element='C')
        assert len(values) == 1
        assert abs(values[0] - 70.5223) < 0.001

    def test_case_insensitive_element(self, giao_output_text):
        """Element matching must be case-insensitive ('c' == 'C')."""
        upper = parse_giao_output(giao_output_text, element='C')
        lower = parse_giao_output(giao_output_text, element='c')
        assert upper == lower

    def test_sigma_to_delta(self, giao_output_text):
        """sigma_to_delta must correctly convert σ_iso to δ for GIAO values."""
        sigmas = parse_giao_output(giao_output_text, element='C')
        ref = 189.7   # TMS reference sigma at B3LYP/cc-pVTZ (approximate)
        deltas = sigma_to_delta(sigmas, ref)
        assert len(deltas) == len(sigmas)
        # All delta values must be positive for organic carbons relative to TMS
        for delta in deltas:
            assert delta > 0, f"Unexpected negative chemical shift: {delta}"
