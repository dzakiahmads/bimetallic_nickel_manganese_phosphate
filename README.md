# Self-Templated Bimetallic Nickel-Manganese Phosphate with Rose-Like Nanoarchitecture Enabling Improved Supercapacitor Performance

## Overview
This repository contains the complete dataset for Density Functional Theory (DFT) calculations of Bimetallic Nickel Manganese Phosphate (NiMnPO) with various Ni:Mn atomic ratios. The data includes optimized crystallographic structures, OH* adsorption configurations, and Zero-Point Energy (ZPE) raw data. 

All calculations were performed using `Quantum ESPRESSO`.

## Investigated Ratios
The structural models and calculation data are categorized by their Ni:Mn atomic ratios:
*   **1:0** - Pure Nickel Phosphate (Baseline)
*   **11:1** - Ni-Mn Phosphate (11:1 ratio)
*   **5:1** - Ni-Mn Phosphate (5:1 ratio)
*   **3:1** - Ni-Mn Phosphate (3:1 ratio)

## Repository Structure
The data for each ratio is organized systematically. Below is an example of the directory structure for the `Ni3Mn1-PO` system:

```text
├── Ni3Mn1-PO/
│   └── 01top_surface/
│       ├── clean_surface/          # Clean surface calculations
│       │   ├── Ni3Mn1PO.cif        # Relaxed structure in CIF format
│       │   ├── Ni3Mn1PO.vasp       # Relaxed structure in VASP/POSCAR format
│       │   ├── PW.in               # Quantum ESPRESSO input file
│       │   └── PW.out              # Quantum ESPRESSO output file
│       │
│       └── OH_ads/                 # OH adsorption on various active sites
│           ├── Mn1/                # Adsorption on Ni-1 site
│           │   ├── ZPE/            # Raw data for Zero-Point Energy calculations
│           │   ├── OH-Mn1-site.cif
│           │   ├── OH-Mn1-site.vasp
│           │   ├── PW.in           # QE input for OH adsorption relaxation
│           │   └── PW.out          # QE output containing final energies
│           ├── Ni1/                # Adsorption on Ni-1 site
│           ├── Ni2/
│           └── Ni3/
```
(This same structure applies to the other ratio folders).

## File Descriptions
* **`*.cif` & `*.vasp`:** Structural files containing lattice vectors and atomic coordinates for the optimized systems.
* **`PW.in`:** Quantum ESPRESSO input files containing the pseudopotentials, k-points, cutoff energies, and calculation parameters used.
* **`PW.out`:** Quantum ESPRESSO output files detailing the SCF convergence, forces, and total energies of the relaxed systems.
* **`ZPE/`:** Directory containing raw data for the vibrational frequency calculations.
