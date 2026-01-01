# Cyrus Tasks

## Current Status (Jan 2025)

We have a **partial** end-to-end test that validates:
- κ + (K, M) → p → e^{K₀} (fully computed in Rust)
- e^{K₀} + (g_s, W₀, V_string) → V₀ (just arithmetic)

But **g_s, W₀, V_string are loaded from McAllister's precomputed files**, not computed.

---

## Input/Output Clarification

### TRUE INPUTS (must be chosen/found)
| Input | Source | Notes |
|-------|--------|-------|
| Polytope | Kreuzer-Skarke database | Discrete choice |
| Triangulation | Heights in secondary fan | Affects κ_ijk |
| K, M flux vectors | Integer lattice, tadpole-constrained | h²¹ integers each |
| Orientifold involution | Coordinate negation pattern | Determines c_i values |
| t_init | Starting point in Kähler cone | Selects solution branch |

### COMPUTED VALUES (deterministic from inputs)
| Value | Formula | What Computes It |
|-------|---------|------------------|
| κ_ijk | From triangulation + GLSM | CYTools (need to port) |
| N_ab | κ_abc M^c | ✅ cyrus-core |
| p | N^{-1} K | ✅ cyrus-core |
| e^{K₀} | (4/3 × κ_ppp)^{-1} | ✅ cyrus-core |
| GV invariants N_q | Mirror symmetry / localization | CYTools (cygv) |
| Racetrack terms | (M·q)(p·q)N_q | Need to implement |
| g_s | Racetrack stabilization | Need to implement |
| W₀ | ζ × Li₂ sum at stabilized τ | Need to implement |
| c_τ | 2π / (g_s × ln(W₀⁻¹)) | ✅ cyrus-core |
| τ_target | c_i / c_τ | ✅ cyrus-core |
| t (Kähler moduli) | KKLT path-following: τ(t) = τ_target | ✅ cyrus-core (solver exists) |
| V_string | (1/6)κt³ - BBHL | ✅ cyrus-core |
| V₀ | -3 e^{K₀} (g_s⁷/(4V)²) W₀² | ✅ cyrus-core |

---

## Phase 1: McAllister Validation ✅ COMPLETE

Tests that validate our formulas against McAllister's published values.

- [x] Fixture extractor script (`scripts/extract_cyrus_fixtures.py`)
- [x] Flat direction: p = N^{-1} K
- [x] Kähler potential factor: e^{K₀} = (4/3 × κ_ppp)^{-1}
- [x] Vacuum energy: V₀ = -3 e^{K₀} (g_s⁷/(4V)²) W₀²
- [x] c_τ relationship
- [x] KKLT divisor volume formula: τ_i = (1/2) κ_ijk t^j t^k
- [x] KKLT Jacobian: J_ik = κ_ijk t^j
- [x] KKLT path-following solver structure

**50 tests passing** (37 unit + 13 integration)

---

## Phase 2: Racetrack Stabilization (NEXT)

Compute g_s and W₀ from GV invariants, instead of loading from files.

### 2.1 GV Invariant Loading
- [ ] Load GV invariants from fixtures (curves + values)
- [ ] Transform curve classes to divisor basis

### 2.2 Racetrack Term Computation
- [ ] Compute q·p for each curve class q
- [ ] Compute M·q coefficients
- [ ] Build RacetrackTerm list sorted by exponent

### 2.3 Racetrack Solver (exists but untested with real data)
- [ ] Test `solve_racetrack()` with McAllister's GV data
- [ ] Validate g_s matches McAllister's g_s.dat
- [ ] Compute W₀ from Li₂ sum at stabilized τ

### 2.4 Integration Test
- [ ] Full test: κ + (K, M) + GV → g_s, W₀ (no loading from files)

---

## Phase 3: KKLT Path-Following

Compute V_string from κ and τ_target, instead of loading from files.

### 3.1 Target Divisor Volumes
- [ ] Load c_i from fixtures (target_volumes.dat = dual Coxeter numbers)
- [ ] Compute τ_target = c_i / c_τ

### 3.2 Path-Following Solver (exists but needs testing)
- [ ] Test `solve_path_following()` with McAllister's κ and τ_target
- [ ] Validate t matches McAllister's corrected_kahler_param.dat
- [ ] Handle branch selection (t_init matters!)

### 3.3 Volume Computation
- [ ] Compute V_string from solved t
- [ ] Validate matches McAllister's cy_vol.dat

### 3.4 Integration Test
- [ ] Full test: κ + c_i + g_s → t → V_string (no loading t from files)

---

## Phase 4: True End-to-End

Compute V₀ from polytope + fluxes only.

### 4.1 Full Pipeline
- [ ] Input: κ, K, M, c_i, GV invariants
- [ ] Output: V₀
- [ ] No intermediate values loaded from files

### 4.2 Validation
- [ ] Test all 5 McAllister examples end-to-end
- [ ] V₀ within 1 order of magnitude of expected

---

## Phase 5: Intersection Number Computation

Compute κ_ijk from polytope (currently loaded from CYTools).

See `plan_intersection_computation.md` and `project_docs/CYTOOLS_ALGORITHMS_CLEAN_ROOM.md`.

### 5.1 GLSM Charge Matrix
- [ ] Augment point matrix with row of 1s (CY condition)
- [ ] Compute left null space (kernel) of augmented matrix
- [ ] Use HNF/LLL for integral basis

### 5.2 Distinct Intersections (from triangulation)
- [ ] For each n-simplex in triangulation, compute 1/|det(vertices)|
- [ ] Store as known intersection values for distinct indices

### 5.3 Linear System Construction
- [ ] Generate all (n-1)-tuples of divisors as "probes" P
- [ ] For each GLSM relation Σ Q_i D_i = 0, create equation: Σ Q_i (D_i · P) = 0
- [ ] Separate knowns (from step 5.2) from unknowns (self-intersections)

### 5.4 Solve and Reduce
- [ ] Solve overdetermined system (sparse least squares or exact rational)
- [ ] Apply CY hypersurface reduction: κ_ijk^CY = -κ_0ijk^ambient

---

## Phase 6: Triangulation

Compute triangulation from polytope + heights.

See `project_docs/CYTOOLS_ALGORITHMS_CLEAN_ROOM.md` §4.

### 6.1 Height-Induced Triangulation
- [ ] Lift points to (v_i, h_i) in R^{d+1}
- [ ] Compute convex hull (use existing Rust crate: `convex_hull` or `delaunay`)
- [ ] Extract lower faces (normal has negative last component)
- [ ] Project back to R^d

### 6.2 FRST Validation
- [ ] Check Fine: all points are vertices of some simplex
- [ ] Check Star: origin is vertex of every simplex
- [ ] Check Regular: comes from height function (automatic if using heights)

### 6.3 Random Triangulation Sampling
- [ ] Generate random heights with origin at -∞ (ensures Star)
- [ ] Validate FRST properties

---

## Phase 7: Kähler Cone

See `project_docs/CYTOOLS_ALGORITHMS_CLEAN_ROOM.md` §5.

### 7.1 Secondary Cone (Wall Computation)
- [ ] For each pair of adjacent simplices, compute wall normal
- [ ] Collect all inequality constraints

### 7.2 Mori Cone
- [ ] Compute curve classes from divisor intersections
- [ ] Find minimal generators

### 7.3 Kähler Cone
- [ ] Dualize Mori cone
- [ ] Implement point-in-cone test

---

## Phase 8: GV Invariants (HKTY Procedure)

This is the hardest part. See `project_docs/CYTOOLS_ALGORITHMS_CLEAN_ROOM.md` §3.

### 8.1 Mirror Map
- [ ] Compute periods of mirror manifold near LCS point
- [ ] This requires solving Picard-Fuchs equations
- [ ] Define mirror coordinates t^a(z) = ϖ_a(z) / ϖ_0(z)

### 8.2 Yukawa Couplings
- [ ] Compute B-model Yukawa couplings (z-dependence)
- [ ] Transform to t-coordinates via mirror map Jacobian

### 8.3 GV Extraction
- [ ] Expand Yukawa as power series in q = exp(2πit)
- [ ] Subtract classical κ_abc
- [ ] Solve for integer n_q using multicover formula

**Note:** This is a significant undertaking. May want to:
- Use precomputed GV invariants from fixtures initially
- Implement simplified cases (1-parameter models) first
- Consider numerical period computation as alternative

---

## Formal Verification (Longer Term)

- [ ] **Intersection Tensor** (`intersection.rs`)
    - [ ] Prove `canonical_key` is idempotent and symmetric
    - [ ] Prove `symmetry_multiplicity` counts permutations correctly
    - [ ] Prove `contract_triple` sum correctness
- [ ] **Divisor Volumes** (`divisor.rs`)
    - [ ] Prove gradients match Jacobian
- [ ] **Flat Direction** (`flat_direction.rs`)
    - [ ] Prove linear system solution correctness

---

## Notes

### Branch Selection Problem
The KKLT equation τ(t) = τ_target has **multiple valid solutions**.
Different t_init values lead to different branches with different V_string.
For 5-81-3213, we found 16 branches with V_string ranging 143-1538.

McAllister's t_init comes from their triangulation heights, which we
don't know how to compute from first principles yet.

### What "End-to-End" Really Means
True end-to-end would be:
```
Polytope vertices → Triangulation → κ_ijk → (with K,M) → p, e^{K₀}
                                         → (with GV) → g_s, W₀
                                         → (with c_i) → t, V_string
                                         → V₀
```

We're currently at:
```
κ_ijk (from CYTools) → p, e^{K₀} ✅
g_s, W₀, V_string (from files) → V₀ ✅ (just arithmetic)
```
