# Python Physics Bridge (Legacy)

This document describes the current `physics_bridge.py` implementation, which serves as the reference for the Rust port.

## Responsibilities
The bridge currently handles:
1.  **CYTools Interface**: Polytope analysis, triangulation, intersection numbers.
2.  **Volume Computation**: $V = \frac{1}{6} \kappa_{ijk} t^i t^j t^k$.
3.  **Gauge Couplings**: $\alpha^{-1} = \text{Vol}(D) / g_s$.
4.  **Moduli Stabilization**: KKLT potential $V = e^K (|DW|^2 - 3|W|^2)$.
5.  **Running Couplings**: RG flow from string scale to Z scale.

## Key Classes

### `CYToolsBridge`
- Wraps `cytools.Polytope` and `cytools.CalabiYau`.
- Caches analysis results to avoid re-triangulation.
- **Port Status**: `cyrus-core` needs to implement `triangulate()` and `intersection_numbers()`.

### `GaugeCouplingComputer`
- Computes $\alpha_3, \alpha_2, \alpha_1$ at string scale.
- Runs RG flow using 1-loop beta coefficients ($b_1=41/10, b_2=-19/6, b_3=-7$).
- **Port Status**: Needs to be ported to `cyrus-moduli`.

### `ModuliStabilizer`
- Computes $W_{flux}$ and $W_{np}$.
- Solves for $V_{min}$.
- **Port Status**: `cyrus-moduli` has initial KKLT support, needs verification.

## Data Flow
1.  **Input**: Genome (vertices, moduli, fluxes).
2.  **Analysis**: `CYToolsBridge` computes topology ($h^{1,1}, \chi$).
3.  **Geometry**: `CYToolsBridge` computes volumes.
4.  **Physics**: `GaugeCouplingComputer` and `ModuliStabilizer` compute observables.
5.  **Output**: `PhysicsOutput` struct (JSON).
