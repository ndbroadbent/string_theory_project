# Cyrus Project

This repository is the home of **Cyrus**, a high-performance Rust toolkit for Calabi-Yau manifold computations focused on string landscape search and quintessence research.

## Project Goal: Focused CY/Quintessence Pipeline

**Cyrus is NOT a general-purpose math library. It's a focused tool for:**

1. **Searching the string landscape** - GA optimization over flux vacua
2. **Verifying McAllister results** - Reproduce arXiv:2107.09064 exactly
3. **Quintessence research** - Compute cosmological observables from string theory

We extract the specific algorithms we need from CYTools, PPL, SciPy, etc., and write comprehensive unit tests for each. We don't port entire libraries - we lift out exactly what's needed.

### What We Need (and Don't Need)

**NEED:**
- Polytope points, dual polytopes, convex hull
- Regular triangulations (FRST)
- Intersection numbers κ_ijk
- Kähler/Mori cone computations
- Volume formulas (with BBHL correction)
- GLSM charge matrix, divisor basis
- GV invariants, curve enumeration
- KKLT/LVS moduli stabilization
- Racetrack superpotential
- **Visualization of EVERYTHING** - PNGs, rotation animations, see every pipeline stage

**VISUALIZATION IS CRITICAL:**
- Polytopes (primal/dual) with rotation animations
- Triangulations - see the simplicial decomposition
- Kähler/Mori cones - visualize the cone structure
- Racetrack potential landscapes
- Parameter space that produces small CC
- Every intermediate result should be visualizable

The goal is to **SEE** what's happening at each stage, not just compute numbers.

**DON'T NEED:**
- Abstract toric variety theory beyond what's needed
- Features CYTools has that we won't use
- Compatibility with CYTools API

### Why Rust?

For exploring the vast string landscape (10^272,000 flux vacua), we need:

1. **Performance** - Orders of magnitude faster than Python for GA inner loops
2. **Confidence** - Type system prevents entire classes of physics errors
3. **Parallelism** - Rayon for easy multi-threading across flux configurations
4. **Formal Verification** - Critical formulas verified in Lean 4 via aeneas

### Algebraic Type Safety

Rust's type system prevents physics errors:
- `F64<Pos>` - strictly positive (volumes, moduli)
- `F64<NonZero>` - can't be zero (denominators)
- `F64<NonNeg>` - non-negative (squared quantities)
- `F64<Finite>` - no NaN, no ±∞

Invalid states are **unrepresentable**. A NaN can't corrupt downstream calculations.

### CYTools Reference Location
```
/Users/ndbroadbent/code/cyrus/reference/cytools/
```

This is the authoritative CYTools source for porting. Read it directly when implementing any functionality.

### Key CYTools Files (Reference for Algorithms)

We extract specific algorithms from these files - we don't port them wholesale:

| Python File | What We Extract |
|-------------|-----------------|
| `src/cytools/polytope.py` | Points, dual polytope, convex hull, vertices |
| `src/cytools/triangulation.py` | Regular triangulation, FRST, heights |
| `src/cytools/calabiyau.py` | Intersection numbers, GLSM, volumes, Kähler cone |
| `src/cytools/cone.py` | Cone dualization (DDM), extremal rays, tip finding |
| `src/cytools/toricvariety.py` | Divisor basis, curve classes |
| `src/cytools/utils.py` | Linear solve, GCD, LLL, nullspace |

### Algorithm Extraction Standards

1. **Identify the algorithm**: Find the specific function/method we need
2. **Understand it completely**: Read every line, understand edge cases
3. **Port to idiomatic Rust**: Not line-by-line translation, but same algorithm
4. **Dual test suites**: Run same inputs through CYTools AND Rust, compare results
5. **Add visualization**: Every major result should be visualizable
6. **High code quality**: All code must pass `cargo clippy` with pedantic warnings

### No Backward Compatibility

**This project does NOT preserve legacy interfaces or behavior.**

- Break APIs freely to match first-principles correctness
- Remove legacy code instead of shimming it
- Update all call sites and tests immediately
- Prefer a clean, consistent codebase over compatibility

### Dual Test Suites (CYTools ↔ Rust)

**Now that we're GPL-3.0, we can run identical inputs through both CYTools and our Rust code.**

```rust
// Example dual test structure
#[test]
fn test_intersection_numbers_dual() {
    let points = vec![...];  // Same input

    // Run through CYTools (via PyO3 or subprocess)
    let cytools_result = run_cytools_intersection(&points);

    // Run through our Rust implementation
    let rust_result = compute_intersection_numbers(&points);

    // Must be IDENTICAL
    assert_eq!(rust_result, cytools_result);
}
```

**Benefits:**
- Catch ANY divergence immediately
- No need to manually create fixtures
- Test on random/generated inputs
- Confidence that our code matches CYTools exactly

**Implementation options:**
1. **PyO3**: Call CYTools directly from Rust tests
2. **Subprocess**: Run Python script, compare JSON output
3. **Shared fixtures**: Generate fixtures once, test both against them

For performance-critical tests, generate fixtures once and cache them. For correctness tests, run both implementations live.

## Architecture
- **Crates**:
  - `cyrus-core`: Core CY computations (polytopes, triangulations, intersection numbers, volumes, cones).
  - `cyrus-moduli`: Moduli stabilization (KKLT, LVS, racetrack).
  - `cyrus-cosmology`: Cosmological evolution (quintessence, Friedmann equations).
  - `cyrus-ga`: Genetic algorithms for landscape search.
  - `cyrus-viz`: Visualization (polytope rendering, animations, potential landscapes).

## Documentation Index

**STOP: Before requesting documentation, CHECK if it already exists below.**

### Physics & Formulas
| Location | Topic |
|----------|-------|
| `project/project_docs/FORMULAS.md` | **Master formula reference** - READ FIRST |
| `string_theory/FORMULAS.md` | Python-specific formula notes |
| `research/PRIMAL_VS_DUAL.md` | Primal vs dual polytope usage |
| `research/COSMOLOGICAL_CONSTANT.md` | V₀ computation |
| `research/TORIC_GEOMETRY.md` | Toric geometry background |
| `research/ORIENTIFOLD_INVOLUTION.md` | Orientifold structures |

### McAllister Reproduction (Validation Target)
Location: `/Users/ndbroadbent/code/string_theory_project/research/mcallister_reproduction/`

| File | Topic |
|------|-------|
| `REPRODUCTION_OUTLINE.md` | **Full pipeline overview** |
| `CLAUDE.md` | McAllister-specific context |
| `PIPELINE_STATUS.md` | Current reproduction status |
| `BASIS_VS_KKLT_BASIS.md` | basis.dat vs kklt_basis.dat difference |
| `BASIS_INDEX_MISMATCH_V1.md` | CYTools 2021 vs 2025 basis issues |
| `LATEST_CYTOOLS_CONVERSION_CORRECTED.md` | K/M transformation rules |
| `EK0_FORMULA_DISCREPANCY_RESOLUTION.md` | e^K₀ formula issues resolved |
| `CHI_DIVISOR_INVESTIGATION.md` | χ(D) computation |
| `RACETRACK_SECTION_6.4.md` | Racetrack stabilization |
| `CURVE_DISCREPANCY.md` | Curve enumeration differences |

### Cyrus Implementation
Location: `project/project_docs/cyrus/`

| File | Topic |
|------|-------|
| `TYPE_SAFETY.md` | Typed numeric system (F64<Pos>, etc.) |
| `EXPANDED_NUMERIC_TYPES.md` | Full type algebra |
| `INVALID_BUT_USEFUL.md` | Edge cases and gotchas |

### Project Philosophy
| Location | Topic |
|----------|-------|
| `project/project_docs/PROJECT_PHILOSOPHY.md` | Core principles |
| `project/project_docs/FORMAL_VERIFICATION.md` | Verification approach |
| `project/project_docs/FORMAL_VERIFICATION_STRATEGY.md` | Strategy details |

### Test Fixture Generation
Location: `/Users/ndbroadbent/code/string_theory/`

Use Python scripts here to generate test fixtures by running CYTools and saving outputs:

| Path | Purpose |
|------|---------|
| `mcallister_2107/full_pipeline_from_data.py` | Complete working pipeline (generates validation data) |
| `mcallister_2107/full_pipeline.py` | Alternative pipeline |
| `FORMULAS.md` | Formula reference |

**Generating fixtures:**
```python
# Example: Generate intersection number fixtures
import json
from cytools import Polytope

p = Polytope([[...]])  # Your test polytope
t = p.triangulate()
cy = t.get_cy()

# Save to JSON for Rust tests
fixture = {
    "intersection_numbers": cy.intersection_numbers(in_basis=True).tolist(),
    "glsm_charge_matrix": cy.glsm_charge_matrix().tolist(),
    # ... other outputs
}
with open("fixtures/intersection_test_1.json", "w") as f:
    json.dump(fixture, f)
```

### Data Files
| Location | Contents |
|----------|----------|
| `string_theory/resources/small_cc_2107.09064_source/anc/paper_data/` | McAllister intermediate data |
| `crates/cyrus-core/tests/mcallister_e2e/inputs/` | Test inputs (polytope, heights, flux) |
| `crates/cyrus-core/tests/mcallister_e2e/assertions/` | Expected values |
| `crates/cyrus-core/tests/mcallister_e2e/overrides/` | Basis overrides for exact reproduction |

## Research Papers

All papers are at `/Users/ndbroadbent/code/string_theory_project/research/papers/`

**Primary References:**
- `small_cc_2107.09064.pdf/.tex` - McAllister paper (our validation target)
- `cytools_paper_2211.03823.pdf/.tex` - CYTools paper (algorithms we reimplement)
- `mcallister_moduli_stabilization_review_2310.20559.pdf/.tex` - McAllister review

**Toric Geometry & Polytopes:**
- `toric_geometry_telen_2203.01690.tex` - Toric geometry
- `complex_geometry_cy_toric_0702063.pdf` - CY toric geometry
- `secondary_fan_cy_pairs_2008.02299.pdf/.tex` - Secondary fan

**Moduli & Kähler:**
- `1712.04946_hodge_divisors.pdf/.tex` - Hodge divisors
- `systematic_kahler_stabilization_2005.11329.pdf` - Kähler stabilization
- `special_kahler_manifolds_freed_9712042.tex` - Special Kähler geometry
- `what_is_special_kahler_geometry_9703082.pdf` - Special Kähler intro

**Flux Vacua:**
- `all_flux_vacua_explicit_1212.4530.pdf` - Explicit flux vacua
- `coexisting_flux_vacua_2507.00615.pdf/.tex` - Coexisting vacua
- `ga_flux_vacua_1302.0529.pdf` - GA for flux vacua
- `ga_flux_vacua_1907.10072.tex` - GA for flux vacua (newer)

**Quintessence & Cosmology:**
- `quintessence_string_moduli_2112.10779.tex` - Quintessence from moduli
- `quintessence_numerically_controlled_2112.10783.pdf` - Numerical quintessence
- `inflation_to_quintessence_2407.03405.pdf/.tex` - Inflation to quintessence
- `kmix_quintessence_2511.23463.tex` - Kähler mixing quintessence
- `desi_swampland_quintessence_1808.02877.pdf/.tex` - DESI/Swampland
- `planck_2018_results_1807.06209v4.pdf/.tex` - Planck cosmology

**Algorithms:**
- `efficient_cy_algorithm_2309.10855.pdf/.tex` - Efficient CY algorithms
- `cohomcalg_algorithm_1003.5217.pdf/.tex` - Cohomology algorithm
- `gkz_short_guide_2412.14748.pdf` - GKZ systems

**Other:**
- `witten_phases_n2_9301042.pdf/.tex` - Witten N=2 phases
- `orientifold_cy_divisor_involutions_2111.03078.pdf/.tex` - Orientifolds
- `demirtas_small_W0_1912.10047.pdf` - Small W₀
- `conifold_vacua_2009.03312.pdf` - Conifold vacua
- `heavy_tails_cy_moduli_1407.0709.pdf/.tex` - Heavy tails
- `cicy_flat_flux_2201.10581.pdf/.tex` - CICY flat flux

## Development Workflow
- **Build**: `cargo build`
- **Test**: `cargo test`
- **Lint**: `cargo clippy` and `cargo fmt`
- **Coverage**: `task coverage` (Must be ≥ 98%)
  - **CRITICAL**: Code coverage MUST NOT be 'hacked' or 'worked around'. It is a fundamental benefit that ensures an AI has read ALL lines of code AT LEAST twice. It is a double-checking mechanism. It makes it easier to understand what parts of the code are used/unused and where changes break things. It is a critical philosophy.
- **Formal Verification**: See `docs/FORMAL_VERIFICATION.md` (in project repo).

## Core Principles

**Prioritize safety and correctness over speed, always.**

- Never use `unsafe` to skip bounds checks or validation
- Use `debug_assert!` to catch bugs in the type system during development
- Trust the compiler and LLVM to optimize safe code
- If profiling shows a hot path, optimize with safe abstractions first

## No Backward Compatibility

**This is not a legacy-maintenance project.**

- **Break compatibility freely** to achieve first-principles correctness.
- **Delete legacy fixtures, overrides, and shortcuts** as soon as real implementations exist.
- **Update or rewrite tests** to reflect the new first-principles pipeline, even if it invalidates old snapshots.
- **Never preserve a workaround** just to keep old tests or data files passing.

## Algorithm Sourcing Philosophy

**Rust bindings don't matter. You can reimplement entire libraries in minutes.**

When you need an algorithm (like polyhedral cone computations, linear programming, convex hull), don't waste time searching for Rust crates with bindings. Instead:

1. **Find the algorithm in ANY language** - C++, Python, Fortran, whatever
2. **Read and understand the code** - understand the algorithm, not just the API
3. **Port to idiomatic Rust** - translate the algorithm faithfully
4. **Port only what you need** - you rarely need 100% of a library

### Reference Libraries Available

These are available in `/Users/ndbroadbent/code/cyrus/reference/` for porting:

| Directory | Source | What to Port |
|-----------|--------|--------------|
| `cytools/` | CYTools Python | Primary port target - polytopes, triangulations, CalabiYau |
| `rsparse/` | Rust sparse matrices | Already a Rust crate - use directly |
| `sprs/` | Rust sparse matrices | Already a Rust crate - use directly |
| `SuiteSparse/` | C sparse solvers | Cholesky, LU decomposition algorithms |
| `scipy/` | Python scientific | Linear algebra, optimization algorithms |
| `scikit-sparse/` | Python sparse | Sparse Cholesky (wraps SuiteSparse) |
| `topcom/` | C++ triangulations | Regular triangulation algorithms |

### External Libraries to Read (not in reference/)

When porting cone.py, read these libraries for algorithm implementations:

| Library | Language | What It Has | Where to Find |
|---------|----------|-------------|---------------|
| **PPL** | C++ | Polyhedral computations, Double Description Method | https://github.com/BUGSENG/PPL |
| **cddlib** | C | Vertex/facet enumeration | https://github.com/cddlib/cddlib |
| **lrs** | C | Vertex enumeration | http://cgm.cs.mcgill.ca/~avis/C/lrs.html |
| **Normaliz** | C++ | Hilbert basis, cone computations | https://github.com/Normaliz/Normaliz |
| **OR-Tools** | C++/Python | LP/MIP solvers, constraint programming | Already used by CYTools |
| **qpsolvers** | Python | Quadratic programming | Already used by CYTools |

### Example: Porting the Double Description Method

CYTools cone.py uses PPL for the `dualize()` function (lines 2059-2107). To port this:

1. Read PPL source to understand the Double Description Method
2. Or read the simpler cddlib implementation
3. Or find an academic paper with pseudocode
4. Port the core algorithm to Rust (~100-200 lines)
5. Test against CYTools output

**Don't search for Rust bindings. Just port the algorithm.**

### What CYTools Dependencies We Must Port

| CYTools Import | What It Does | Our Approach |
|----------------|--------------|--------------|
| `ppl` | Polyhedral cones, DDM | Port DDM algorithm from PPL/cddlib |
| `ortools` | LP/MIP solving | Use `good_lp` crate or port HiGHS |
| `qpsolvers` | Quadratic programming | Port OSQP or use existing crate |
| `flint` | Arbitrary precision | Already using `malachite` |
| `scipy.optimize` | linprog, nnls | Port HiGHS LP, port NNLS |
| `scipy.sparse` | Sparse matrices | Already using `rsparse`/`sprs` |
| `numpy` | Arrays, linalg | Using `ndarray`, `faer` |
| `qhull` | Convex hull | Use `qhull` crate (exists) |
| `normaliz` | Hilbert basis | Port from Normaliz C++ |

## CYTools Reference (GPL-3.0)

**Cyrus is GPL-3.0 licensed. Read CYTools source directly and port it faithfully.**

### CYTools Source Location
```
/Users/ndbroadbent/code/cyrus/reference/cytools/
```

This is the authoritative source. Key files in `src/cytools/`:
- `polytope.py` - Polytope class (convex hull, dual, points, faces) - 144KB
- `triangulation.py` - Triangulation class (regular triangulations, FRST) - 108KB
- `calabiyau.py` - CalabiYau class (intersection numbers, Kähler cone, volumes) - 101KB
- `cone.py` - Cone class (Kähler/Mori cones, tip finding) - 85KB
- `toricvariety.py` - ToricVariety class (divisors, curves, GLSM) - 80KB
- `utils.py` - Utility functions (linear algebra, solving, GCD) - 53KB
- `polytopeface.py` - PolytopeFace class - 20KB
- `config.py` - Configuration management - 5KB
- `helpers/` - Helper modules

### Porting Process

For each CYTools class/function:

1. **Read the Python thoroughly** - understand every line, every edge case
2. **Create the Rust module** - match the structure where sensible
3. **Write unit tests FIRST** - generate test cases by running CYTools Python
4. **Port the implementation** - match behavior exactly
5. **Compare outputs** - run both Python and Rust, verify identical results
6. **Optimize later** - only after tests pass, use rayon/SIMD if needed

### Testing Strategy

**Every ported function MUST have unit tests that compare against CYTools output.**

```rust
#[test]
fn test_intersection_numbers_matches_cytools() {
    // Load fixture generated by running CYTools Python
    let expected = load_fixture("intersection_numbers_4_214.json");

    // Run our Rust implementation
    let actual = cy.intersection_numbers(in_basis=true);

    // Exact match required
    assert_eq!(actual, expected);
}
```

Generate test fixtures by running CYTools Python and saving outputs to JSON/msgpack files.

## CRITICAL: Extract What We Need, Test It Thoroughly

**We're not building a general-purpose library. Extract the specific algorithms needed for our pipeline.**

This is a focused CY/quintessence project. We lift out exactly the algorithms we need from CYTools, PPL, SciPy, etc., and write comprehensive unit tests for each.

### What This Means

1. **Extract specific algorithms** - not entire classes if we don't need everything
2. **Comprehensive unit tests** - every extracted function gets thorough testing
3. **Understand the algorithm** - read the source, understand it, port it correctly
4. **Visualize everything** - if we can't see it, we don't understand it

**Bad (what you should NEVER do):**
```
"Use McAllister's precomputed values instead of computing"
"Skip the test because it's too slow"
"This is close enough"
"I don't understand why this works but it passes"
```

**Good (what you SHOULD do):**
```
"We need intersection numbers - let me extract that algorithm from CYTools"
"I'll port just the DDM algorithm from PPL for cone dualization"
"Let me add visualization so we can see what this polytope looks like"
"The CYTools source shows exactly how this works - porting it now"
```

## CRITICAL: This is Theoretical Physics, Not Normal Software

**This is not building a SaaS. This is high energy theory physics. This is formal verification. This is launching rockets.**

The standard of correctness here is absolute. A single sign error, a single wrong index, a single misunderstood coordinate system will produce garbage that looks plausible. There are no "close enough" results - either the physics is exactly right or it's meaningless.

### No Shortcuts, No Masking Problems

**This entire process requires deep, perfect understanding. No stone left unturned.**

DO NOT mask problems or take shortcuts. DO NOT use fallbacks or cheat to get tests or scripts passing. If you do that, you will save an hour now and waste days or weeks later.

Every discrepancy must be understood completely. Every formula must be verified from first principles. If something doesn't match, STOP and figure out why - don't paper over it.

### No "Simpler Approaches" - Just Port CYTools

**When in doubt, read the CYTools source. It has the answer.**

We previously wasted enormous time trying to implement from specifications or "simpler approaches." This never worked. The CYTools source code captures subtle algorithmic details that no spec document can convey.

When you find yourself thinking:

- "We could just hardcode this for now..."
- "A simpler approach would be to..."
- "We could manually identify which indices..."
- "For now, let's just..."

STOP. Go read the CYTools source instead.

**The pattern that wasted our time:**
1. Try to implement from a spec or "understanding"
2. It works for simple test cases
3. Later, it breaks in subtle ways
4. Debugging takes days because the spec was incomplete
5. Eventually realize CYTools source had the answer all along

**The correct response:**
1. Read the CYTools Python source for the function
2. Understand what it actually does (not what you think it should do)
3. Port it faithfully to Rust
4. Test against CYTools output
5. Optimize AFTER correctness is verified

**Examples of wrong thinking:**
```
❌ "Let me implement intersection numbers from the paper's description..."
❌ "I'll write my own triangulation algorithm based on the math..."
❌ "The spec says to use SNF, so I'll implement that..."
```

**Examples of correct thinking:**
```
✓ "Let me read cytools/calabiyau.py to see exactly how intersection_numbers() works"
✓ "CYTools has a Triangulation class - let me port that directly"
✓ "The CYTools source uses this specific algorithm - I'll match it exactly"
```

CYTools is battle-tested on thousands of polytopes. Our job is to port it faithfully, not reinvent it.

### No Silent Fallbacks

**NEVER write code that silently falls back to approximations or default values when a computation fails.**

```rust
// BAD - silent fallback
let result = compute_something();
if result.is_none() {
    return Some(default_value);  // WRONG!
}

// GOOD - fail loudly
let result = compute_something()?;  // Propagate failure
```

This applies to ALL computations: volumes, gauge couplings, potentials, etc.
If any physics computation fails, the entire evaluation must fail loudly.
Silent fallbacks make debugging nearly impossible and produce garbage results.

## CRITICAL: Read FORMULAS.md First

**ALWAYS read `string_theory/FORMULAS.md` before beginning any physics-related task.** It contains the complete formula reference with warnings about common pitfalls (e.g., classical vs instanton-corrected volumes).

## End Goal: Complete String Theory Research Pipeline

**Build a complete string theory research pipeline by porting CYTools to Rust.**

CYTools already does everything we need - our job is to port it to Rust for performance and then build the GA/cosmology layers on top.

### The Production Pipeline

When we run the GA on the string landscape, we will:
1. Enumerate polytopes from Kreuzer-Skarke database
2. Walk secondary fans (all triangulations) - **CYTools `Triangulation` class**
3. Try random flux vectors (K, M)
4. Try random Kähler moduli
5. Compute intersection numbers - **CYTools `CalabiYau.intersection_numbers()`**
6. Compute volumes, Kähler cones - **CYTools `CalabiYau` methods**

We CANNOT precompute intersection numbers for all polytopes × triangulations × bases. Cyrus must compute everything on-the-fly, matching CYTools output exactly.

### Validation Target: McAllister Paper

Our end-to-end test verifies the complete pipeline against McAllister's published results (arXiv:2107.09064). When Cyrus produces identical results to CYTools for this case, we have confidence the port is correct.

## Type Safety Philosophy

**Don't fight to get 100% coverage. Lean on the type system.**

When you find yourself writing defensive runtime checks that are hard to test, step back and ask: can the type system prevent this entire class of errors?

### The Pattern

Instead of scattered runtime checks:
```rust
fn foo(points: &[Point]) {
    if points.is_empty() { return; }  // hard to test, easy to forget
    // ...
}
```

Create a type that makes invalid states unrepresentable:
```rust
struct NonEmptyPoints(Vec<Point>);

impl NonEmptyPoints {
    fn new(points: Vec<Point>) -> Option<Self> {
        if points.is_empty() { None } else { Some(Self(points)) }
    }
}

fn foo(points: &NonEmptyPoints) {
    // No check needed - type guarantees non-empty
}
```

### Why This Matters

1. **Eliminates untestable branches** - No defensive code means no coverage gaps
2. **Compile-time guarantees** - Bugs caught before runtime
3. **Self-documenting** - Function signatures express requirements
4. **Single validation point** - Check once at the boundary, trust the type everywhere else
5. **Prevents whole classes of errors** - Can't accidentally pass invalid data

### When to Apply

Use this pattern when you see:
- The same precondition checked in multiple functions
- `.expect("already validated")` with trust-me comments
- Defensive checks that are hard to trigger in tests
- Error handling for "impossible" states

See `project_docs/cyrus/TYPE_SAFETY.md` for detailed examples.

## Numeric Type Algebra

**ALL numbers are typed. No raw `f64` anywhere.**

The codebase uses phantom-typed wrappers (`F64<Tag>`, `I32<Tag>`, etc.) with compile-time algebra rules. The type system automatically tracks invariants through arithmetic.

### Available Tags

```
Pos      - strictly positive (> 0)
Neg      - strictly negative (< 0)
Zero     - exactly 0
One      - exactly 1
Two      - exactly 2
NonZero  - not zero (could be + or -)
NonNeg   - non-negative (≥ 0)
NonPos   - non-positive (≤ 0)
Finite   - any finite value (the "top" type - no NaN, no ±∞)
GTEOne   - greater than or equal to 1
```

### The Algebra is Complete

Cross-type operations work automatically via trait impls in `types/algebra.rs`:

```rust
// These compile and produce the correct output type:
let a: F64<Pos> = pos!(3.0);
let b: F64<Finite> = finite!(-2.0);
let c: F64<Finite> = a * b;     // Pos * Finite = Finite (automatic!)
let d: F64<Pos> = a * a;        // Pos * Pos = Pos
let e: F64<Neg> = a * neg;      // Pos * Neg = Neg
```

**NEVER do this:**
```rust
// WRONG - breaks type safety
let x = a.get() * b.get();  // raw f64 multiplication
```

**DO this:**
```rust
// CORRECT - type algebra handles it
let term = mult * kappa * t[i];  // types flow through automatically
```

### Widening vs Narrowing

- **Widening**: ALWAYS automatic. You NEVER widen manually.
  - `Pos + Neg = Finite` - the algebra produces the correct output type
  - `Pos * Finite = Finite` - cross-type ops just work
  - There is no `.to_finite()` method - widening happens through operations
  - If you find yourself trying to widen, you're doing something wrong

- **Narrowing**: The ONLY manual type operation. Use `try_to_*` methods.
  - Narrowing goes from weaker to stronger constraints
  - Always returns `Option<F64<Target>>` - `None` if constraint not satisfied
  - Use at boundaries or when you know the physics guarantees a property

### Available Narrowing Methods

Each type has `try_to_*` methods for all valid narrowings:

```rust
// From Finite (can be anything) - most methods available
finite.try_to_pos()      // → Option<Pos>     if > 0
finite.try_to_neg()      // → Option<Neg>     if < 0
finite.try_to_zero()     // → Option<Zero>    if = 0
finite.try_to_non_zero() // → Option<NonZero> if ≠ 0
finite.try_to_non_neg()  // → Option<NonNeg>  if ≥ 0
finite.try_to_non_pos()  // → Option<NonPos>  if ≤ 0
finite.try_to_gte_one()  // → Option<GTEOne>  if ≥ 1

// From NonNeg (≥ 0) - can narrow to Pos or Zero
non_neg.try_to_pos()     // → Option<Pos>  if > 0
non_neg.try_to_zero()    // → Option<Zero> if = 0

// From NonPos (≤ 0) - can narrow to Neg or Zero
non_pos.try_to_neg()     // → Option<Neg>  if < 0
non_pos.try_to_zero()    // → Option<Zero> if = 0

// From NonZero (≠ 0) - can narrow to Pos or Neg
non_zero.try_to_pos()    // → Option<Pos> if > 0
non_zero.try_to_neg()    // → Option<Neg> if < 0

// From Pos (> 0) - can narrow to exact values
pos.try_to_one()         // → Option<One>    if = 1
pos.try_to_gte_one()     // → Option<GTEOne> if ≥ 1

// From Neg (< 0) - can narrow to exact values
neg.try_to_minus_one()   // → Option<MinusOne> if = -1

// From GTEOne (≥ 1) - can narrow to exact values
gte_one.try_to_one()     // → Option<One> if = 1
gte_one.try_to_two()     // → Option<Two> if = 2
```

Note: Methods only exist where narrowing is possible. For example:
- `Neg` has no `try_to_pos()` - a negative can never be positive
- `Pos` has no `try_to_neg()` - a positive can never be negative

### Boundary Principle

Validate at **boundaries**, trust types everywhere else:

```rust
// BOUNDARY: raw data comes in, validate here
pub fn from_raw_moduli(raw: &[f64]) -> Option<Vec<F64<Pos>>> {
    raw.iter().map(|&x| F64::<Pos>::new(x)).collect()
}

// INTERIOR: types are trusted, no validation needed
pub fn volume(t: &[F64<Pos>]) -> F64<Pos> {
    // Every t[i] is guaranteed positive, result is guaranteed positive
    t.iter().copied().product()
}

// BOUNDARY: result might not satisfy constraint
pub fn contract(kappa: &Intersection, t: &[F64<Pos>]) -> Option<F64<Pos>> {
    let sum: F64<Finite> = /* ... */;
    sum.try_to_pos()  // Narrow at the boundary
}
```

### Key Files

- `types/algebra.rs` - All arithmetic rules (Add, Sub, Mul, Div, Neg)
- `types/f64.rs` - F64 wrapper and constructors
- `types/tags.rs` - Tag definitions and trait hierarchy
- `types/range.rs` - CheckedRange for typed iteration

### Built-in Constants

Use these instead of creating values manually:

```rust
// Exact value constants
F64::<Zero>::ZERO      // 0.0
F64::<One>::ONE        // 1.0
F64::<Two>::TWO        // 2.0
F64::<MinusOne>::MINUS_ONE  // -1.0

// Zero constants for fold operations
F64::<Finite>::ZERO    // 0.0 as Finite
F64::<NonNeg>::ZERO    // 0.0 as NonNeg
I64::<Finite>::ZERO    // 0 as Finite
I64::<Zero>::ZERO      // 0 as Zero
```

### Compile-time Macros

For literal constants, use macros (compile-time verified):

```rust
f64_pos!(3.14)         // F64<Pos>
f64_pos!(2.0 * PI)     // F64<Pos> - expressions work too
f64_finite!(-2.5)      // F64<Finite>
i64_pos!(42)           // I64<Pos>
i64_neg!(-5)           // I64<Neg>
range!(0..100)         // CheckedRange<usize> - compile-time verified start < end
```

### Type-Preserving Methods

```rust
// Absolute value - returns strongest possible type
Finite.abs()  → NonNeg
Pos.abs()     → Pos (unchanged)
Neg.abs()     → Pos
NonZero.abs() → Pos

// Square root
Pos.sqrt()    → Pos
NonNeg.sqrt() → NonNeg

// Square (x² is always non-negative)
Finite.square() → NonNeg

// Natural logarithm (ln of positive is any real)
Pos.ln() → Finite

// Reciprocal (1/positive is positive)
Pos.recip() → Pos

// Integer to float conversion (preserves tag)
I64<Pos>.to_f64()    → F64<Pos>
I64<Neg>.to_f64()    → F64<Neg>
I64<Finite>.to_f64() → F64<Finite>
```

### Typed Iteration

```rust
let steps = range!(0..100);  // CheckedRange<usize>

// Iterate yielding I64<NonNeg> (0, 1, 2, ...)
for i in steps.iter_non_neg() { ... }

// Iterate yielding I64<Pos> (1, 2, 3, ... skips 0)
for i in steps.iter_pos() { ... }

// Division of typed integers yields typed float
let alpha = m.to_f64() / n.to_f64();  // I64<Pos> / I64<Pos> = F64<Pos>
```

### Common Mistakes - DO NOT DO THESE

#### 0. Using raw ranges `0..n`

```rust
// WRONG - untyped iteration
for i in 0..dim { ... }
(0..dim).map(|i| ...).collect()

// CORRECT - use CheckedRange for typed iteration
let r = CheckedRange::new(0, dim);
for i in r.iter_non_neg() { ... }  // yields I64<NonNeg>
for i in r.iter_pos() { ... }      // yields I64<Pos> (skips 0)
```

Raw ranges produce raw `usize`. Always use `CheckedRange` for typed iteration.

#### 1. Using `.new().expect()` for compile-time constants

```rust
// WRONG - runtime validation for a literal constant
let threshold = F64::<Pos>::new(1e-10).expect("positive");
let two_pi = F64::<Pos>::new(2.0 * PI).expect("positive");

// CORRECT - compile-time verified
let threshold = f64_pos!(1e-10);
let two_pi = f64_pos!(2.0 * PI);
```

#### 2. Silently swallowing type errors with `.unwrap_or()`

```rust
// CATASTROPHICALLY WRONG - hides bugs with arbitrary fallback
let vol = vol_update.try_to_pos().unwrap_or(f64_pos!(1.0));
let tau = tau_update.try_to_pos().unwrap_or(f64_pos!(0.1));

// This is like:
// - `catch (e) {}` in JavaScript
// - Using `any` in TypeScript
// - `except: pass` in Python
// It defeats the ENTIRE PURPOSE of the type system.

// CORRECT - propagate failure honestly
let vol = vol_update.try_to_pos()?;  // Return None if invalid
let tau = tau_update.try_to_pos()?;

// Or if this truly can't fail, make that clear
let vol = vol_update.try_to_pos().expect("algorithm guarantees positive");
```

If narrowing fails, either:
1. **Propagate the failure** with `?` - let the caller handle it
2. **Panic with context** with `.expect("reason")` - if it's a bug
3. **Redesign** - maybe the type shouldn't be `Pos` in the first place

NEVER silently replace with an arbitrary value.

#### 3. Using `.new().expect()` for intermediate computations

```rust
// WRONG - verbose, noisy, unnecessary
let alpha = F64::<Finite>::new((m + 1) as f64 / n_steps as f64)
    .expect("alpha is finite");

// CORRECT - division of positive integers is always positive
let alpha = F64::<Pos>::from_ratio(m + 1, n_steps);
// Or if from_ratio doesn't exist, create a helper
```

If you KNOW a value is valid by construction, don't validate it at runtime.

#### 4. Extracting raw values and rewrapping

```rust
// WRONG - breaks the type chain
let x = a.get() * b.get();
let result = F64::<Finite>::new(x).expect("finite");

// CORRECT - keep everything typed
let result = a * b;  // types flow through
```

#### 5. Types not flowing end-to-end

```rust
// WRONG - typed at boundaries only
fn compute(raw: f64) -> f64 {
    let typed = F64::<Pos>::new(raw)?;
    typed.get() * 2.0  // back to raw!
}

// CORRECT - typed throughout
fn compute(x: F64<Pos>) -> F64<Pos> {
    x * f64_pos!(2.0)  // stays typed
}
```

### The Golden Rule

**Use the strongest type that accurately describes the value.**

- If you know it's positive, use `F64<Pos>`, not `F64<Finite>`
- If you know it's non-negative, use `F64<NonNeg>`, not `F64<Finite>`
- The algebra widens automatically through operations - never manually
- Only narrow (never widen) - use `try_to_*` methods when needed

## Critical Physics Formulas

See `string_theory/FORMULAS.md` for complete reference. Key formulas:

### Cosmological Constant (Vacuum Energy)
```
V₀ = -3 eᴷ |W|²    (in Planck units, Mpl⁴)
```
Where:
- **W** is the TOTAL superpotential at the minimum (NOT just W₀!)
- **W = W₀ + W_np** (flux + non-perturbative terms)
- At KKLT minimum, W_np partially cancels W₀, so |W| << |W₀|
- **eᴷ** is the exponential of the Kähler potential

### Volume Formulas
```
V_string = (1/6) κ_ijk t^i t^j t^k - ζ(3)χ/(4(2π)³)   (with BBHL correction!)
V_E = V_string / g_s^(3/2)     (Einstein frame from string frame)
```

**CRITICAL:** The BBHL α' correction term `-ζ(3)χ/(4(2π)³)` is NOT optional!
For h11=214, h21=4: χ = 2(h11-h21) = 420, BBHL ≈ 0.509. Without it, V is wrong by ~0.5.

### Key e^K₀ Formula (eq. 6.12)
```
e^K₀ = (4/3) × (κ̃_abc p^a p^b p^c)^(-1)
```
Where κ̃_abc are mirror (dual) intersection numbers and p is the flat direction.

### Full V₀ Formula (eq. 6.24)
```
V₀ = -3 × e^K₀ × (g_s⁷ / (4×V_string)²) × W₀²
```

### McAllister 4-214-647 Results (Section 6.4)
- g_s ≈ 0.00911134
- W₀ ≈ 2.3 × 10⁻⁹⁰
- V_string ≈ 4711.83
- e^K₀ ≈ 0.234393
- V₀ ≈ -5.5 × 10⁻²⁰³ Mpl⁴

### Pipeline Computation Flow
```
(K, M) → N_ab = κ_abc M^c → p = N⁻¹ K → e^K₀ = (4/3)(κ̃_abc p^a p^b p^c)⁻¹
                                      ↓
                               g_s, W₀ (racetrack)
                                      ↓
                               τ_i = (c_i/2π) × ln(W₀⁻¹)
                                      ↓
                               Solve T_i(t) = τ_i for t
                                      ↓
                               V_string = (1/6)κ_ijk t^i t^j t^k - BBHL
                                      ↓
                               V₀ = -3 × e^K₀ × (g_s⁷/(4V_string)²) × W₀²
```

## Key Files

### CYTools Reference (to port from)
- `reference/cytools/src/cytools/polytope.py` - Polytope class (144KB)
- `reference/cytools/src/cytools/triangulation.py` - Triangulation class (108KB)
- `reference/cytools/src/cytools/calabiyau.py` - CalabiYau class (101KB)
- `reference/cytools/src/cytools/cone.py` - Cone class (85KB)
- `reference/cytools/src/cytools/toricvariety.py` - ToricVariety class (80KB)
- `reference/cytools/src/cytools/utils.py` - Utility functions (53KB)
- `reference/cytools/src/cytools/polytopeface.py` - PolytopeFace class (20KB)
- `reference/cytools/src/cytools/config.py` - Configuration (5KB)
- `reference/cytools/src/cytools/helpers/` - Helper modules
- `reference/cytools/tests/` - CYTools tests (port these too!)

### Cyrus Implementation (what we're building)
- `crates/cyrus-core/src/lib.rs` - Entry point for core logic
- `crates/cyrus-core/src/polytope/` - Ported Polytope class
- `crates/cyrus-core/src/triangulation/` - Ported Triangulation class
- `crates/cyrus-core/src/calabiyau/` - Ported CalabiYau class
- `crates/cyrus-core/src/intersection/` - Intersection number computation

### E2E Validation Tests
- `crates/cyrus-core/tests/mcallister_e2e/` - End-to-end tests against McAllister paper

## Project Management
- **Docs**: `project/project_docs/` (symlinked)
- **Tasks**: `project/todo/cyrus_tasks.md` (symlinked)
- **Research**: `project/research/` (symlinked)

## Commands
- `cargo run --bin cyrus-validate -- mcallister`: Run validation against published results.
