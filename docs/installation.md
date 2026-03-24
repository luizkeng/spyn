# Installation Guide

Tested on **Ubuntu 20.04 LTS**, **Linux Mint 20**, and **Debian 11**.

---

## 1. System prerequisites

```bash
sudo apt update
sudo apt install -y \
    git wget curl \
    gawk gfortran \
    openmpi-bin openmpi-doc libopenmpi-dev \
    xterm openbabel jmol \
    python3-dev python3-pip
```

---

## 2. Install Miniconda (if not already installed)

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p "$HOME/miniconda"
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 3. Create the SPYN conda environment

```bash
git clone https://github.com/jeffrichardchemistry/spyn.git
cd spyn
conda env create -f environment.yml
conda activate spyn-env
```

This installs Python 3.8, PyQt5, NumPy, SciPy, Pandas, Matplotlib, and
OpenBabel from `conda-forge`.

---

## 4. Install Quantum ESPRESSO with GIPAW support

Quantum ESPRESSO is **not** included in the conda environment because it
requires Fortran compilation and MPI.

### Option A — Compile from source (recommended for full control)

```bash
# Download QE 6.3
wget https://github.com/QEF/q-e/archive/qe-6.3.tar.gz
tar -xzf qe-6.3.tar.gz
cd q-e-qe-6.3

# Configure and compile
./configure --enable-openmp
make -j$(nproc) pw

# Compile GIPAW plugin (download separately from http://www.gipaw.net)
cd ..
wget http://www.gipaw.net/gipaw-qe6.3.tar.gz
tar -xzf gipaw-qe6.3.tar.gz
cd gipaw-qe6.3
make -j$(nproc)
```

### Option B — Use distribution packages or pre-compiled binaries

Some distributions ship `quantum-espresso` via apt. Verify that `gipaw.x`
is included before using this option.

### Create symbolic links (required by SPYN)

SPYN looks for executables named `pw` and `gipaw` in the application
directory. Create symbolic links after compilation:

```bash
ln -s /path/to/qe-6.3/bin/pw.x    /path/to/spyn/code/spyn/pw
ln -s /path/to/gipaw-qe6.3/gipaw.x /path/to/spyn/code/spyn/gipaw
```

---

## 5. Download pseudopotentials

SPYN uses `pbe-tm-new-gipaw-dc` pseudopotentials for GIPAW calculations.

```bash
# Place pseudopotentials in the pp/ directory
mkdir -p /path/to/spyn/code/spyn/pp
cd /path/to/spyn/code/spyn/pp
# Download from http://www.gipaw.net — follow instructions on the website
```

---

## 6. Test the installation

```bash
conda activate spyn-env
cd examples/lamivudine
python run_example.py
ls example_spectrum.png   # should exist after ~5 seconds
```

If `example_spectrum.png` is created without errors, the Python stack is
working correctly.

To test the full GUI:

```bash
cd code/spyn
python spyn_main.py
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'PyQt5'` | conda env not activated | `conda activate spyn-env` |
| `obabel: command not found` | OpenBabel not installed | `sudo apt install openbabel` or `conda install -c conda-forge openbabel` |
| `FileNotFoundError: pw` | Missing symlink | Create symlink as described in Step 4 |
| `xterm: command not found` | xterm not installed | `sudo apt install xterm` |
| GIPAW calculation hangs | MPI not configured | Verify `mpirun -np 1 pw < /dev/null` exits cleanly |
| `jmol: command not found` | Jmol not installed | `sudo apt install jmol` (optional — only needed for 3D visualisation) |
