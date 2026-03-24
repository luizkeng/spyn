"""Shared pytest fixtures pointing to the example files shipped with SPYN."""

import pathlib
import pytest

EXAMPLES = pathlib.Path(__file__).parent.parent / "code" / "spyn" / "examples"


@pytest.fixture(scope="session")
def gipaw_output_text():
    """Full text of the bundled GIPAW example output (lamivudine, QE 6.3)."""
    return (EXAMPLES / "gipaw_output.out").read_text(encoding="utf-8", errors="replace")


@pytest.fixture(scope="session")
def giao_output_text():
    """Full text of the bundled Gaussian GIAO example output (lamivudine)."""
    return (EXAMPLES / "giao_output.log").read_text(encoding="utf-8", errors="replace")
