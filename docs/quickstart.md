# Quickstart Tutorial

This tutorial walks through the four tabs of the SPYN GUI using the
bundled lamivudine example files in `code/spyn/examples/`.

Start the application:

```bash
conda activate spyn-env
cd code/spyn
python spyn_main.py
```

---

## Tab 1 — Conformational Searching

This tab uses OpenBabel's genetic algorithm to generate a conformer
ensemble from a molecular file.

**Steps:**

1. Click **Open File** → select `examples/great.mol` (or any CIF/MOL/SDF).
2. Set **Number of conformers** (e.g. `50`) and **Steps** (e.g. `1000`).
3. Select the force field: `MMFF94` is recommended for drug-like molecules.
4. Click **Run GA** — an xterm window shows OpenBabel progress.
5. When finished, the conformer list is populated in the table.
6. Optionally click **Visualise** to open Jmol with the ensemble.
7. Click **Export SDF** to save the ensemble for further analysis.

**Note:** The conformer SDF is automatically passed to the Boltzmann tab
when you click **Next →**.

---

## Tab 2 — Boltzmann Distribution

Calculates the thermal population of each conformer.

**Automatic mode (after conformational search):**

1. Set **Temperature (K)** (e.g. `298.15`).
2. Set **Number of conformers** to analyse (e.g. `10`).
3. Select energy unit: `kcal/mol` or `kj/mol`.
4. Click **Calculate (automatic)** — populations appear in the table.

**Manual mode (custom energies):**

1. Enter the number of conformers in the field.
2. Click **Set table** — a table with editable energy cells appears.
3. Type each conformer energy in the first column.
4. Click **Calculate** — the `%Ci` column fills with populations.

---

## Tab 3 — ss-NMR (GIPAW)

Generates Quantum ESPRESSO input files from a CIF, runs SCF + GIPAW, and
displays the output.

**Steps:**

1. **Import CIF**: File → Import CIF → select `examples/alglycine.cif`.
2. **Configure k-points**: choose *Automatic* (e.g. `2 2 2 0 0 0`) or
   *Manual* (paste a custom k-point block).
3. **Set parameters**: plane-wave cutoff (default 60 Ry), number of MPI
   processes, convergence threshold.
4. Click **Calculate SCF** — xterm opens running `mpirun ... pw.x`.
5. Monitor convergence in the **Output** sub-tab (filter: *Iterations* or
   *Total energy*).
6. Click **Calculate GIPAW** — xterm runs `mpirun ... gipaw.x`.
7. In the **GIPAW Output** sub-tab, select element (e.g. `C`) and click
   **Filter** to display the σ_iso values.

**Importing pre-computed output** (if QE is not installed):

- File → Import GIPAW output → select `examples/gipaw_output.out`.

---

## Tab 4 — Spectro-NMR

Plots the theoretical NMR spectrum with Lorentzian broadening and allows
overlay with experimental data.

**After a GIPAW calculation or import:**

1. Select the **element** (e.g. `C`) in the combo box.
2. Click **Load from GIPAW** — σ_iso values fill the tensors field.
3. Enter the **reference σ_iso** (e.g. `173.0` ppm for glycine Cα).
4. Set **x-axis range** (min/max ppm), **amplitude**, **width** (FWHM), and
   **smoothing** (integer, polynomial order for Savitzky-Golay).
5. Select **Lorentzian** or **Sticks** in the combo box.
6. Click **Plot** — spectrum appears in the canvas.

**Manual entry (no GIPAW output):**

- Type comma-separated σ_iso values in the *Tensors* field and click
  **Plot (manual)**.

**Overlay experimental spectrum:**

- File → Import CSV → select `examples/LFII.csv` → click **Plot experimental**.

**Export:**

- Right-click the matplotlib toolbar → **Save figure** (PNG, PDF, SVG).
