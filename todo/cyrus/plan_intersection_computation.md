# Implementation Plan: Intersection Computation

This document outlines the "Clean Room" implementation plan for computing intersection numbers in `cyrus-core`.

## Overview
Intersection numbers $\kappa_{ijk}$ are computed by solving a linear system derived from the triangulation's topology and the toric variety's linear relations.

## Algorithm (Clean Room)

### 1. Basic Intersection Numbers (from Simplices)
For each simplex $\sigma$ in the triangulation:
- A "distinct" intersection exists for the indices of its vertices.
- Value $v = 1 / |\det(V)|$, where $V$ is the matrix of vertex coordinates (extended with 1s).
- These are the only non-self intersections that are non-zero by default.

### 2. Linear Equivalence Relations
From the GLSM charge matrix $Q$:
- Each row $q$ represents a relation $\sum q_i D_i = 0$.
- We generate equations by taking the product of this relation with all possible $(dim-1)$-tuples of divisors.
- Example (3-fold): $( \sum q_i D_i ) \cdot D_j \cdot D_k = 0 \implies \sum q_i (D_i \cdot D_j \cdot D_k) = 0$.

### 3. Linear System Construction
- **Variables**: All possible intersection numbers $\kappa_{ijk}$ (symmetric, so $i \le j \le k$).
- **Constants**: The values from Step 1.
- **Equations**: The relations from Step 2.
- **System**: $Mx = C$ where $x$ are the unknown self-intersections.

### 4. Solving
- Use a sparse linear solver (e.g., `nalgebra` with sparse features or a dedicated crate).
- For smooth varieties, enforce/verify integer results.

### 5. CY Hypersurface Reduction
- $\kappa_{ijk}^{CY} = -\kappa_{0ijk}^{Ambient}$, where index 0 is the canonical divisor.

## Tasks
- [ ] Implement `Triangulation::distinct_intersections()`.
- [ ] Implement `Polytope::glsm_relations()`.
- [ ] Implement linear system builder.
- [ ] Integrate sparse solver.
- [ ] Implement CY reduction logic.
