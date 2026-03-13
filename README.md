# 3DCSQ: 3D Cell Shape Quantification

[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**An Effective Method for Quantification, Visualization and Analysis of 3D Cell Shape During Early Embryogenesis**

Zelin Li*, Jianfeng Cao, Guoye Guan*, Chao Tang, Zhongying Zhao, and Hong Yan

*Corresponding author

---

## Table of Contents

- [Introduction](#introduction)
- [Abstract](#abstract)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Core Functions](#core-functions)
- [Scientific Concepts](#scientific-concepts)
- [Usage Examples](#usage-examples)
- [Citation](#citation)

---

## Introduction

This repository contains the official implementation of our research paper on 3D cell shape quantification. We developed three novel shape features to quantify cell morphology and conducted comprehensive experiments and evaluations on living *C. elegans* embryos.

The 3DCSQ method uniquely combines:
- **Spherical Grids** - for surface sampling
- **Spherical Harmonics (SPHARM)** - for shape transformation
- **Principal Component Analysis (PCA)** - for dimensionality reduction

This comprehensive approach enables robust cell shape quantification, analysis, and visualization.

---

## Abstract

Embryogenesis, inherently three-dimensional, poses significant challenges in quantification when approached through 3D fluorescence imaging. Traditional descriptors such as volume, surface area, and mean curvature often fall short, providing only a global view and lacking in local detail and reconstruction capability.

Addressing this, we introduce **3DCSQ (3D Cell Shape Quantification)**, an effective integrated method for transforming digitized 3D cell shapes into analytical feature vectors. Key capabilities include:

- **Shape Recognition**: Identifying cellular morphological phenotypes
- **Cell Clustering**: Grouping cells based on shape similarity
- **Pattern Detection**: Identifying biologically reproducible cellular patterns

Applied to *Caenorhabditis elegans* embryos from 4- to 350-cell stages, 3DCSQ reliably identifies and quantifies biologically reproducible cellular patterns, including distinct skin cell deformations.

**Keywords**: Spherical harmonics (SPHARM), Cell shape quantification, Morphological reproducibility, Lineage analysis, *C. elegans*

---

## Features

- ✅ 3D cell surface extraction from segmentation data
- ✅ Spherical harmonics transformation for shape representation
- ✅ PCA-based shape feature extraction
- ✅ K-means clustering for cell shape classification
- ✅ Cell lineage tree visualization
- ✅ Volume and surface area calculation
- ✅ Contact detection between cells

---

## Installation

### Prerequisites

- Python 3.9+
- Conda (recommended)

### Environment Setup

```bash
# Update conda
conda update -n base -c defaults conda

# Create environment from requirements
conda env create -f requirements.txt

# Activate environment
conda activate CellShapeAnalysis
```

### Key Dependencies

| Package | Version |
|---------|---------|
| numpy | ~1.22.4 |
| scipy | ~1.8.1 |
| pandas | ~1.4.2 |
| matplotlib | ~3.5.2 |
| scikit-learn | ~1.1.1 |
| pyshtools | latest |
| open3d | ~0.15.2 |
| nibabel | latest |
| treelib | latest |

---

## Quick Start

```python
import utils.cell_func as cell_f
import transformation.SH_represention as sh_represent

# Load segmentation data
img = cell_f.nii_get_cell_surface('path/to/segmentation.nii.gz')

# Calculate spherical harmonics coefficients
sh_coefficient = sh_represent.sample_and_SHc_with_surface(
    surface_points, 
    sample_N=30, 
    lmax=14
)

# Perform PCA analysis
from analysis.SH_analyses import analysis_SHcPCA_One_embryo
analysis_SHcPCA_One_embryo(embryo_path, used_degree=16, l_degree=25)
```

---

## Project Structure

```
cell_shape_quantification/
├── analysis/                    # Analysis module (3rd layer)
│   ├── SH_analyses.py          # Spherical harmonics analysis functions
│   └── curvature.py            # Curvature calculations
│
├── transformation/              # Feature transformation (2nd layer)
│   ├── SH_represention.py      # Spherical harmonics transformation
│   ├── R_matrix_represention.py # Surface sampling methods
│   └── PCA.py                  # PCA analysis utilities
│
├── lineage_stat/               # Lineage analysis (2nd layer)
│   ├── data_structure.py       # Cell lineage tree construction
│   ├── lineage_tree.py         # Lineage tree visualization
│   └── generate_life_span.py   # Lifespan data generation
│
├── utils/                      # Utility functions (1st layer)
│   ├── cell_func.py           # Cell operations (volume, surface, contacts)
│   ├── general_func.py        # Coordinate transformations
│   ├── spherical_func.py      # Spherical sampling functions
│   ├── sh_cooperation.py      # SPHARM array utilities
│   ├── shape_preprocess.py    # Surface extraction
│   └── draw_func.py           # Visualization utilities
│
├── experiment/                 # Experimental scripts (4th layer)
│   ├── cluster.py             # Clustering experiments
│   └── geometry.py            # Geometric analysis
│
├── static/                     # Configuration
│   ├── config.py              # Path configurations
│   └── dict.py                # Cell fate dictionaries
│
├── DATA/                       # Data directory (not in repo)
│   └── my_data_csv/           # Output CSV files
│
├── main.py                     # Main entry point
├── test1.py                    # Core analysis functions
└── requirements.txt            # Dependencies
```

---

## Core Functions

### Spherical Harmonics Transformation

```python
# Calculate SPHARM coefficients for one embryo (3D+T data)
test1.py/calculate_SPHARM_embryo_for_cells()
test1.py/SPHARM_eigenharmonic()  # Eigenharmonic Weight Vector
```

### Spherical Grid Representation

```python
# Calculate spherical grid coefficients (Eigengrid)
test1.py/Map2D_grid_csv()
test1.py/Map_2D_eigengrid()  # Eigengrid Weight Vector
```

### Surface Sampling

```python
# Sample cell surfaces with interval
transformation/test1.py/do_sampling_with_interval()
```

### Lineage Tree

```python
# Draw cell fate lineage tree
lineage_stat/draw_test.py -> draw_cell_fate_lineage_tree_01paper()
```

---

## Scientific Concepts

### Cell Curvature

#### Gaussian Curvature (using libigl)

Reference: [libigl Python Tutorials](https://libigl.github.io/libigl-python-bindings/tut-chapter1/)

**Principal Curvatures**: The maximum and minimum curvature radii at surface points.

- [Principal Curvature (Wikipedia)](https://en.wikipedia.org/wiki/Principal_curvature)
- [Gaussian Curvature (Wikipedia)](https://en.wikipedia.org/wiki/Gaussian_curvature)

### Coordinate Systems

The code uses standard spherical coordinate transformations:

- **Cartesian to Spherical**: Convert (x, y, z) to (r, θ, φ)
- **Spherical to Cartesian**: Convert (r, θ, φ) to (x, y, z)

Reference: [Spherical Coordinate System (Wikipedia)](https://en.wikipedia.org/wiki/Spherical_coordinate_system)

---

## Usage Examples

### 1. Generate Lineage Tree

```bash
cd lineage_stat
python generate_life_span.py
```

This command:
1. Builds a tree structure based on CD files
2. Adds cell frame information to the trees
3. Generates lineage tree files

### 2. Draw Average Lineage Tree

The process involves:
1. Constructing an average lineage tree across all embryos
2. Extracting frame cell values based on time resolution
3. Calculating average values at each time point
4. Interpolating for missing cells

### 3. Shape Analysis Pipeline

```python
# Step 1: Extract cell surfaces
from utils.cell_func import nii_get_cell_surface

# Step 2: Calculate SPHARM coefficients
from transformation.SH_represention import get_SH_coefficient_of_embryo

# Step 3: Perform PCA
from analysis.SH_analyses import analysis_SHcPCA_One_embryo

# Step 4: Clustering
from analysis.SH_analyses import analysis_SHc_Kmeans_One_embryo
```

---

## Data Format

### Input Data
- **Segmentation Files**: NIfTI format (.nii.gz)
- **Name Dictionary**: CSV file mapping cell labels to names

### Output Data
- **SPHARM Coefficients**: CSV files with shape descriptors
- **PCA Results**: Principal components and explained variance
- **Clustering Results**: Cell cluster assignments

---

## Citation

If you use this code in your research, please cite:

```bibtex
@article{3dcsq2024,
  title={3DCSQ: An effective method for quantification, visualization and analysis of 3D cell shape during early embryogenesis},
  author={Li, Zelin and Cao, Jianfeng and Guan, Guoye and Tang, Chao and Zhao, Zhongying and Yan, Hong},
  journal={...},
  year={2024}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- City University of Hong Kong
- The research teams contributing to *C. elegans* imaging and analysis

---

## Contact

For questions and support, please contact the corresponding authors.