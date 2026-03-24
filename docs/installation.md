# Installation Guide

SPYN comes with a graphical installer that handles all dependencies
automatically — including downloading, compiling, and configuring
Quantum ESPRESSO 6.3 with GIPAW support.

---

## Automated installation (recommended)

Tested on **Debian 10/11**, **Ubuntu 18.04/20.04 LTS**,
**Linux Mint 19/20**, and **Elementary OS 5**.

### Step 1 — Download and unzip

Download the latest release from
https://github.com/jeffrichardchemistry/spyn/releases and unzip, or clone:

```bash
git clone https://github.com/jeffrichardchemistry/spyn.git
```

### Step 2 — Run the graphical installer

```bash
cd spyn/Spyn_1.0_alpha
python3 install_ui.py
```

A window opens asking for the installation directory.

### Step 3 — Choose directory and click Install

1. Click **...** to browse and select the destination folder.
2. Click **Install**.
3. A terminal window opens and runs the full installation automatically.
   When prompted, enter your **root password** to install system packages.

### What the installer does automatically

| Step | Action |
|------|--------|
| System packages | Installs `gawk`, `gfortran`, `openmpi-bin`, `libopenmpi-dev`, `xterm`, `openbabel`, `jmol` via `apt-get` |
| Python packages | Installs `PyQt5`, `matplotlib`, `pandas`, `scipy`, `numpy` via `pip3` |
| Quantum ESPRESSO | Extracts `qe-6.3.tar.gz`, runs `./configure --enable-parallel --enable-shared`, compiles `pw.x` and `gipaw.x` using all available CPU cores |
| GIPAW module | Configures and compiles the GIPAW module against the QE 6.3 source |
| System links | Copies `pw.x` → `/usr/bin/pw` and `gipaw.x` → `/usr/bin/gipaw` |
| Desktop entry | Creates a SPYN application icon in the system applications menu |

After the terminal closes, SPYN is ready to use.

### Step 4 — Launch SPYN

Either click the SPYN icon in the applications menu, or:

```bash
cd /your/chosen/directory/spyn
python3 spyn_main.py
```

---

## Manual installation (non-Debian systems)

For RPM-based distributions (openSUSE, Fedora, CentOS) or systems
where the automated installer does not work, install dependencies manually.

### System packages

**Debian/Ubuntu:**
```bash
sudo apt-get install gawk gfortran openmpi-bin openmpi-doc libopenmpi-dev \
                     xterm openbabel jmol python3-dev python3-pip
```

**openSUSE:**
```bash
sudo zypper install gawk gcc-fortran openblas-devel lapack fftw3-devel lam xterm openbabel
```

### Python packages

```bash
pip3 install PyQt5 matplotlib pandas scipy numpy
```

### Quantum ESPRESSO + GIPAW

```bash
# Extract and compile QE 6.3
cd spyn/code/spyn/qe
tar -xzf qe-6.3.tar.gz
cd qe-6.3
./configure --enable-parallel --enable-shared
make -j$(nproc) pw

# Compile GIPAW module
cd qe-gipaw-6.3
./configure --with-qe-source=$PWD/..
make -j$(nproc)

# Create system links
sudo cp ../bin/pw.x /usr/bin/pw
sudo cp bin/gipaw.x /usr/bin/gipaw
```

### Pseudopotentials

Place `pbe-tm-new-gipaw-dc` pseudopotentials in `code/spyn/pp/`.
Download from http://www.gipaw.net.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'PyQt5'` | PyQt5 not installed | `pip3 install PyQt5` |
| `obabel: command not found` | OpenBabel not installed | `sudo apt install openbabel` |
| `pw: command not found` | System link missing | Run `simbolic.sh` manually or re-run installer |
| `gipaw: command not found` | System link missing | Same as above |
| `xterm: command not found` | xterm not installed | `sudo apt install xterm` |
| Compilation fails with MPI error | MPI libraries missing | `sudo apt install openmpi-bin libopenmpi-dev` |
| GIPAW configure error | QE source path wrong | Check that `--with-qe-source` points to the QE 6.3 root |
