# PRD: Cyrus Verification Pipeline

## Overview
Cyrus must prove its correctness to the physics community by reproducing the results of seminal papers, specifically McAllister et al. (arXiv:2107.09064). We will implement a rigorous end-to-end test suite using data extracted from `cytools` as "gold standard" fixtures.

## Goals
1.  **Reproducibility**: `cargo test` runs the full McAllister pipeline and outputs $V_0 ≈ -10^{-203}$ exactly.
2.  **Modularity**: Isolate the "Hard Math" (Geometry) from the "Physics" (Moduli Stabilization).
3.  **Performance**: Run these checks in seconds, not minutes.

## Test Fixture Structure
We will store validation data in `crates/cyrus-core/tests/fixtures/`:

```
mcallister_4-214-647/
├── polytope.json       # vertices
├── triangulation.json  # heights (for reproducibility)
├── flux.json           # K, M, c_i vectors
├── intersection.json   # κ_ijk (Precomputed from CYTools)
├── gv_invariants.json  # N_q (Precomputed from CYTools)
└── expected.json       # Targets: g_s, W_0, V_string, V_0
```

## Phased Implementation

### Phase 1: The Physics Pipeline (Priority)
We assume the geometry ($κ_{ijk}$, $N_q$) is correct (loaded from fixtures) and verify the physics logic.

- **Inputs**: κ_{ijk}, N_q, K, M.
- **Compute**:
    1.  Flat direction $p$ and $e^{K_0}$.
    2.  Racetrack minimum $W_0, g_s$.
    3.  KKLT path-following $t_{init} 	o t_{final}$.
    4.  Volume $V_{string}$ and Vacuum Energy $V_0$.
- **Verify**: Matches `expected.json`.

### Phase 2: The Geometry Pipeline
We move intersection number computation into Rust.

- **Inputs**: Triangulation/Simplices.
- **Compute**: κ_{ijk}.
- **Verify**: Matches `intersection.json`.

## Required Modules

| Concept | Python Script (Legacy) | Cyrus Module (Rust) |
| :--- | :--- | :--- |
| **Racetrack** | `compute_derived_racetrack.py` | `cyrus-core/src/racetrack.rs` |
| **KKLT Solver** | `compute_kklt_iterative.py` | `cyrus-core/src/kklt.rs` |
| **GV Invariants** | `compute_gv_invariants.py` | (Keep as JSON fixture for now) |

## Implementation Plan
1.  **Fixture Extractor**: A Python script to run CYTools once and dump the JSONs.
2.  **Cyrus Loaders**: `serde` structs to load these JSONs in `#[test]`.
3.  **Logic Port**: Translate the Python solver logic to Rust.
