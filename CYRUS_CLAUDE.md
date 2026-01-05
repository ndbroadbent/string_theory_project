# Cyrus Project

This repository is the home of **Cyrus**, a high-performance Rust toolkit for Calabi-Yau manifold computations.

## Architecture
- **Crates**:
  - `cyrus-core`: Fundamental mathematics (polytopes, intersection numbers, volumes).
  - `cyrus-moduli`: Moduli stabilization algorithms (KKLT, LVS).
  - `cyrus-cosmology`: Cosmological evolution (quintessence, Friedmann equations).
  - `cyrus-ga`: Genetic algorithms for landscape search.

## Documentation Index

**STOP: Before requesting documentation, CHECK if it already exists below.**

### Clean Room Implementation Specs
Location: `project/project_docs/clean_room/` (symlinked from string_theory_project)

| File | Topic |
|------|-------|
| `DIVISOR_BASIS.md` | How to compute divisor basis from GLSM (SNF/HNF algorithm) |
| `INTERSECTION_NUMBERS.md` | κ_ijk computation (sparse linear system, Cholesky) |
| `GLSM_CHARGE_MATRIX.md` | GLSM charge matrix construction |
| `TRIANGULATION.md` | Regular triangulation algorithm |
| `REGULAR_TRIANGULATION_LIFTING.md` | Lifting method for triangulations |
| `DEFAULT_HEIGHTS.md` | FRST heights computation |
| `DUAL_POLYTOPE.md` | Dual/polar polytope computation |
| `REFLEXIVE_POLYTOPE_DUAL.md` | Reflexive polytope duality |
| `CONVEX_HULL_VERTICES.md` | Convex hull algorithms |
| `CONVEX_HULL_D.md` | D-dimensional convex hull |
| `KAHLER_CONE.md` | Kähler cone computation |
| `GV_INVARIANTS.md` | Gopakumar-Vafa invariants |
| `HEIGHTS_MODULI_MAPPING.md` | Heights to moduli mapping |
| `GEOMETRIC_PRIMITIVES.md` | Basic geometric operations |

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

### Python Prototype Reference
Location: `/Users/ndbroadbent/code/string_theory/`

| Path | Purpose |
|------|---------|
| `mcallister_2107/full_pipeline_from_data.py` | Complete working pipeline |
| `mcallister_2107/full_pipeline.py` | Alternative pipeline |
| `mcallister_2107/CLAUDE.md` | McAllister context |
| `FORMULAS.md` | Formula reference |

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

## Clean Room Implementation Policy

**When you need to implement functionality that exists in CYTools (GPL 3.0), request technical documentation from the user.**

CYTools is GPL-licensed. To keep Cyrus legally clean:
1. You NEVER read the CYTools source code directly
2. When you need to implement something (e.g., dual polytope computation, triangulation heights), ASK the user for technical documentation
3. The user passes your request to another agent that reads the GPL source and writes a technical specification
4. You implement from the specification only

**How to request:**
Simply ask: "I need technical documentation for clean room implementation of [X]"

Examples:
- "I need technical documentation for clean room implementation of dual polytope computation"
- "I need technical documentation for clean room implementation of default triangulation heights"
- "I need technical documentation for clean room implementation of GLSM charge matrix construction"
- "I need technical documentation for how CYTools optimizes intersection number computation"

The user will provide a specification document. Implement from that.

**When something is slow or unclear:**
If a computation is slow or you don't understand how to optimize it:
1. **DO NOT** suggest using CYTools or external code
2. **DO NOT** suggest skipping the test
3. **DO** request technical documentation explaining the algorithm
4. **DO** profile and implement optimizations in Rust

Example of what to say:
```
"The intersection computation is taking too long. I need technical documentation
for clean room implementation of optimized intersection number algorithms -
specifically what algorithmic optimizations CYTools uses (sparse matrices,
parallelization, caching, etc.)"
```

The other agent will read CYTools, understand its optimizations, and provide you
with a specification you can implement in Rust.

## CRITICAL: We Reimplement EVERYTHING in Rust

**Cyrus is a complete reimplementation of CYTools in Rust. We do NOT use CYTools or any external C++ code.**

When a computation is slow:
1. **Profile it** - find the bottleneck
2. **Request technical documentation** - ask how CYTools optimizes it (see Clean Room Policy above)
3. **Implement the optimization in Rust** - from the specification provided
4. **NEVER suggest "just use CYTools"** - that defeats the entire purpose

When a test takes a long time:
1. **Run it anyway** - correctness over speed
2. **Profile and optimize** - make it faster
3. **Request documentation** - if you need to understand the algorithm better
4. **NEVER suggest "skip this test"** - we need to know it works

The Python code in `string_theory/` calls `cy.intersection_numbers()` - that's CYTools doing the work.
Our Rust code must compute intersection numbers from first principles, and it must be fast enough for production.

**Bad (what you should NEVER suggest):**
```
"CYTools has optimized C++ code for this"
"We could skip this slow test"
"Use McAllister's precomputed values"
"Run in release mode or skip for now"
```

**Good (what you SHOULD do):**
```
"The intersection computation is O(n³). Let me profile it."
"I need technical documentation for clean room implementation of intersection optimizations"
"I'll parallelize this with rayon once I understand the algorithm."
"Let me check if we can use sparse matrices here."
```

## CRITICAL: This is Theoretical Physics, Not Normal Software

**This is not building a SaaS. This is high energy theory physics. This is formal verification. This is launching rockets.**

The standard of correctness here is absolute. A single sign error, a single wrong index, a single misunderstood coordinate system will produce garbage that looks plausible. There are no "close enough" results - either the physics is exactly right or it's meaningless.

### No Shortcuts, No Masking Problems

**This entire process requires deep, perfect understanding. No stone left unturned.**

DO NOT mask problems or take shortcuts. DO NOT use fallbacks or cheat to get tests or scripts passing. If you do that, you will save an hour now and waste days or weeks later.

Every discrepancy must be understood completely. Every formula must be verified from first principles. If something doesn't match, STOP and figure out why - don't paper over it.

### No "Simpler Approaches"

**There is no such thing as a "simpler approach". There is only the RIGHT approach.**

In this project, a "simpler approach" has NEVER been correct. The right approach is usually very complicated because the physics is complicated. When you find yourself thinking:

- "We could just hardcode this for now..."
- "A simpler approach would be to..."
- "We could manually identify which indices..."
- "For now, let's just..."

STOP. You are about to create technical debt that will cost days or weeks to fix later.

**The pattern:**
1. You suggest a "simpler approach"
2. It works for the immediate test case
3. Later, it breaks in subtle ways
4. Debugging takes 10x longer than doing it right the first time

**The correct response:**
1. Identify what CYTools (or the physics) actually does
2. Request clean room documentation if needed
3. Implement the full, correct algorithm
4. Optimize for performance AFTER correctness is verified

**Examples of wrong "simpler" thinking:**
```
❌ "For the dual with only 4 basis vectors, we could manually identify..."
❌ "We could skip the divisor basis computation and just use point indices..."
❌ "A simpler approach would be to project after computing..."
```

**Examples of correct thinking:**
```
✓ "I need technical documentation for clean room implementation of divisor basis computation"
✓ "CYTools computes intersection_numbers(in_basis=True) - we need the same capability"
✓ "The h11-dimensional basis is fundamental to the physics, not an optimization"
```

The "complicated" approach is complicated because the mathematics requires it. Simplifying means getting wrong answers.

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

## Project Goal

**Build a complete string theory research pipeline from first principles.**

This is NOT about loading precomputed values and validating they match. This is about computing EVERYTHING from the raw polytope data, exactly as we will need to when running the full GA search across the string landscape.

### The Production Pipeline

When we run the GA on the string landscape, we will:
1. Enumerate polytopes from Kreuzer-Skarke database
2. Walk secondary fans (all triangulations)
3. Try random flux vectors (K, M)
4. Try random Kähler moduli

We CANNOT precompute intersection numbers for all polytopes × triangulations × bases. We MUST compute everything on-the-fly from first principles.

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
- `crates/cyrus-core/src/lib.rs`: Entry point for core logic.
- `crates/cyrus-core/src/intersection.rs`: Intersection tensor logic (verification target).
- `crates/cyrus-core/src/divisor.rs`: Divisor volume logic (verification target).

## Project Management
- **Docs**: `project/project_docs/` (symlinked)
- **Tasks**: `project/todo/cyrus_tasks.md` (symlinked)
- **Research**: `project/research/` (symlinked)

## Commands
- `cargo run --bin cyrus-validate -- mcallister`: Run validation against published results.
