# Octahedron-Comparison-Test-Solver-Using-Description-by-QODV
Python implementation of the Qualitative Object Descriptor by Vertices (QODV) and the Octahedron Comparison Test (OCT). Emulates human spatial reasoning to solve 3D mental rotation tasks using qualitative topological descriptors.


# A Qualitative Representation of the Octahedron for Spatial Rotations

This repository contains the implementation of the **Octahedron Comparison Test (OCT)** solver as described in the paper: 
> *E. González-Yu, Z. Falomir, and V. Costa (2026). "A Qualitative Representation of the Octahedron for Spatial Rotations".*

## Overview
This project introduces a **Qualitative Object Descriptor by Vertices (QODV)** to represent 3D octahedrons and model their transformations under spatial rotations. The implementation includes an analytical solver capable of determining if two octahedrons are identical but rotated.

## Model Description

The model is built on the principle that any regular polyhedron can be qualitatively defined by the specific relationship between its vertices and faces, differentiating itself from a purely quantitative coordinate description.

### The Two-Part Descriptor (QODV)
The qualitative description of an octahedron $O$ is composed of two primary sets of data: $QODV(O) = \langle QODV_V(V), QODV_F(F) \rangle$.

#### 1. $QODV_V$ (Vertex Descriptor)
The descriptor for a vertex $v$ is defined as $QODV_V(v) = (Adj_f(v), l(v))$.
* **Adjacent Features** $Adj_f(v)$: This lists the features (symbols) on the faces surrounding a vertex, ordered in a clockwise manner.
* **Location** $l(v)$: This tracks the vertex's current position relative to a fixed observer using the set $\{front(f), right(r), up(u), down(d), back(b), left(l)\}$.
* **Rotation Logic:** The adjacent features are rotationally invariant and intrinsic to the vertex, while the location updates whenever a rotation occurs.

#### 2. $QODV_F$ (Face Descriptor)
The descriptor for a face $f$ is defined as $QODV_F(f) = (Adj_v(f), Feature(f), E(f))$.
* **Connectivity $Adj_v(f)$:** This lists the three specific vertices that form the triangular face, ordered clockwise.
* **Feature Identity $Feature(f)$:** This identifies the unique symbol or variable present on that specific face.
* **Relative Orientation $E(f)$:** This describes the orientation of the symbol relative to a specific edge (formed by two adjacent vertices) and a qualitative angle $\alpha$.


## Usage
* `OCT_solver.py` Python module that provides the logic to solve a case for the OCT, both analytically (using the algorithm described in the paper) and by brute force.
* `comps_solved.py` Solves different ilustrative examples of octahedron comparisons. The visuals of the examples are provided in the comps file, and the output text is provided in `output.txt`.
* `octahedrons_visual.py` Python file to visualize how an octahedron with features rotates. Used to create the different cases.

## Installation
It is recommended to use a virtual environment to avoid system conflicts.

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
