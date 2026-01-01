# Architecture: String Theory Landscape Explorer

## Overview
This system searches the string theory landscape (Calabi-Yau compactifications) for configurations that match Standard Model physics.

It consists of three main components:
1.  **String Theory Search**: The meta-genetic algorithm (Rust).
2.  **Cyrus**: The physics engine (Rust).
3.  **Formal Verification**: Correctness proofs (Aeneas/Lean).

## Current Architecture (Hybrid)
Currently, `string_theory_search` drives the GA in Rust but calls out to Python (`physics_bridge.py`) for all heavy lifting.

```mermaid
graph TD
    A[String Theory Search (Rust)] -->|PyO3| B[physics_bridge.py]
    B -->|Import| C[CYTools (Python/C++)]
    B -->|Import| D[cymyc (JAX)]
    B -->|Import| E[PALP (C)]
```

### Limitations
- **Performance**: Python Global Interpreter Lock (GIL) limits parallelism.
- **Complexity**: Managing Python venvs and dependencies in a Rust binary is fragile.
- **Correctness**: "Silent failures" in Python libraries are hard to catch.

## Target Architecture (Pure Rust)
The goal is to move all physics logic into `cyrus` (Rust), removing the Python dependency entirely.

```mermaid
graph TD
    A[String Theory Search (Rust)] -->|Crate Dep| B[Cyrus (Rust)]
    B -->|Module| C[cyrus-core (Polytopes, Intersection)]
    B -->|Module| D[cyrus-moduli (KKLT, Stabilization)]
    B -->|Module| E[cyrus-cosmology (Evolution)]
    B -->|Verified| F[cyrus-verify (Aeneas Proofs)]
```

### Migration Strategy
1.  **Port Logic**: Move logic from `physics_bridge.py` to `cyrus` crates.
2.  **Verify**: Prove core algorithms in `cyrus-verify` with Aeneas.
3.  **Switch**: Update `string_theory_search` to call `cyrus` directly.

## Component Details

### Cyrus Core (`cyrus-core`)
- **Polytopes**: Lattice point enumeration, reflexivity checks.
- **Triangulation**: FRST triangulations (ported from CYTools/CGAL).
- **Intersection**: Computing $\kappa_{ijk}$ (High priority verification target).
- **Geometry**: Kähler cone, volume formulas.

### Cyrus Moduli (`cyrus-moduli`)
- **Stabilization**: Solving $D_i W = 0$ for Kähler moduli.
- **Fluxes**: Computing $W_{flux}$ and $N_{flux}$.
- **Potential**: Computing $V_{AdS}$ and $V_{uplift}$.

### Physics Bridge (Legacy)
See `project_docs/PYTHON_BRIDGE.md` for details on the current implementation.

## Related Documentation
- [[project_docs/PYTHON_BRIDGE.md|Python Bridge Implementation]]
- [[project_docs/FORMAL_VERIFICATION.md|Formal Verification Strategy]]
- [[project_docs/PROJECT_PHILOSOPHY.md|Project Philosophy and Directives]]
