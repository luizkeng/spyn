# Contributing to SPYN

Thank you for your interest in contributing to SPYN.

## How to report a bug

Open an issue at https://github.com/jeffrichardchemistry/spyn/issues and include:

- OS and Python version
- Steps to reproduce the issue
- Expected vs actual behaviour
- Relevant error messages or screenshots

## How to submit a patch

1. Fork the repository and create a branch:
   ```bash
   git checkout -b fix/my-bugfix
   ```
2. Make your changes. If they touch `spyn_core.py`, add or update tests in
   `tests/`.
3. Verify the test suite passes locally:
   ```bash
   pip install -e .
   pytest tests/ -v
   ```
4. Open a pull request against `master` with a clear description of the
   change and its motivation.

## Development environment

```bash
git clone https://github.com/jeffrichardchemistry/spyn.git
cd spyn
conda env create -f environment.yml
conda activate spyn-env
pip install -e .
pytest tests/ -v --cov=spyn
```

## Code style

- PEP 8 for all new code.
- Keep GUI modules (`spyn_main.py`, `boltz.py`, etc.) free of new
  business logic — place pure functions in `spyn_core.py`.
- All public functions in `spyn_core.py` must have a docstring and a
  corresponding test.

## Scope

SPYN is targeted at Linux users with Quantum ESPRESSO installed.
Cross-platform portability and QE version upgrades are welcome
contributions but are out of scope for the core maintainers.
