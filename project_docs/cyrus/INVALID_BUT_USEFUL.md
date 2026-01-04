# Invalid But Useful: Physics Boundaries vs Type Boundaries

## The Problem

In genetic algorithm optimization, we often explore regions of parameter space that violate physics constraints. The key insight is that **"less invalid" is better than "more invalid"** - a configuration with `V_string = -0.001` is closer to valid than one with `V_string = -100`.

But our type system is designed to make invalid states unrepresentable. How do we reconcile these?

## The Distinction

There are two kinds of "invalid":

### 1. Bug / Garbage (Type Boundary)

These indicate a bug in the code or corrupted input:

| Condition | Why It's a Bug |
|-----------|----------------|
| `κ_ijk < 0` | Intersection numbers are positive for valid CY geometry |
| `t^i < 0` | Kähler moduli must be in the Kähler cone |
| `NaN` or `±∞` | Numerical error, division by zero, etc. |
| Dimension mismatch | Wrong tensor contracted with wrong vector |

**These should be caught by the type system.** If they occur, it's a bug - crash immediately.

### 2. Invalid Physics (Runtime Boundary)

These are valid explorations that happen to violate physics constraints:

| Condition | Why It's Valid Exploration |
|-----------|---------------------------|
| `V_string < 0` | BBHL correction > classical volume |
| `V₀ > 0` | Vacuum energy should be negative (AdS) |
| Outside Kähler cone | GA exploring boundary |
| Tadpole exceeded | Flux configuration too large |

**These should be checked at runtime.** The GA uses the "how invalid" information for fitness.

## The Pattern: Dual Function Variants

For each physics computation, provide two variants:

### Strict Variant (for validated pipelines)

Returns `Option<PositiveF64>` or similar - enforces physics constraints:

```rust
/// Compute string frame volume.
/// Returns `None` if volume is non-positive (invalid physics).
#[must_use]
pub fn volume_string(
    kappa: &NonEmptyIntersection,
    t: &Moduli<'_>,
    h11: i32,
    h21: i32,
) -> Option<PositiveF64> {
    let classical = volume_classical(kappa, t);
    let bbhl = bbhl_correction(h11, h21);
    PositiveF64::new(classical.get() - bbhl)
}
```

Use this when:
- Computing final results for valid configurations
- In code paths that require valid physics
- After GA has found a valid candidate

### GA Variant (for optimization)

Returns `Scalar<Finite>` - allows negative values for fitness calculation:

```rust
/// Compute string frame volume for GA fitness.
/// Can return negative values (invalid physics but useful for optimization).
#[must_use]
pub fn volume_string_ga(
    kappa: &NonEmptyIntersection,
    t: &Moduli<'_>,
    h11: i32,
    h21: i32,
) -> Scalar<Finite> {
    let classical = volume_classical(kappa, t);
    let bbhl = bbhl_correction(h11, h21);
    // Unwrap is safe: finite - finite = finite
    Scalar::<Finite>::new(classical.get() - bbhl).unwrap()
}
```

Use this when:
- Computing GA fitness scores
- Exploring parameter space
- Need gradient information from constraint violations

## Fitness Function Pattern

```rust
fn compute_fitness(candidate: &Candidate) -> f64 {
    // Use GA variants that allow invalid physics
    let v_string = volume_string_ga(&kappa, &t, h11, h21);
    let v0 = vacuum_energy_ga(&kappa, &t, &racetrack);

    // Check physics constraints and compute penalty/reward
    let volume_score = if v_string.get() > 0.0 {
        // Valid: reward larger volumes (better for LVS)
        v_string.get().ln()
    } else {
        // Invalid: penalty proportional to violation
        // Less negative = closer to valid = better
        VOLUME_PENALTY + v_string.get() * PENALTY_SCALE
    };

    let v0_score = if v0.get() < 0.0 {
        // Valid: reward more negative (deeper AdS)
        -v0.get().abs().ln()
    } else {
        // Invalid: should be negative
        V0_PENALTY - v0.get() * PENALTY_SCALE
    };

    volume_score + v0_score + other_terms
}
```

## Naming Convention

| Suffix | Meaning | Return Type |
|--------|---------|-------------|
| (none) | Strict, physics-valid only | `Option<PositiveF64>` or `Result<...>` |
| `_ga` | GA-friendly, allows invalid | `Scalar<Finite>` or `f64` |
| `_raw` | Raw computation, no type wrapper | `f64` |

## Examples

### Volume Functions

```rust
// Strict: returns None if non-positive
pub fn volume_string(...) -> Option<PositiveF64>

// GA: returns Finite, can be negative
pub fn volume_string_ga(...) -> Scalar<Finite>

// Raw: for internal use, benchmarks
pub fn volume_string_raw(...) -> f64
```

### Vacuum Energy Functions

```rust
// Strict: returns None if non-negative (should be AdS)
pub fn vacuum_energy(...) -> Option<NegativeF64>

// GA: returns Finite, can be positive
pub fn vacuum_energy_ga(...) -> Scalar<Finite>
```

### Kähler Cone Check

```rust
// Strict: returns bool
pub fn is_in_kahler_cone(...) -> bool

// GA: returns margin (positive = inside, negative = outside)
pub fn kahler_cone_margin(...) -> Scalar<Finite>
```

## Better Pattern: Policy Types

Instead of writing two functions, write the math once and let a **policy type** determine what happens with the result:

```rust
use crate::types::scalar::{Scalar, Finite, Pos};

/// Policy for handling physics boundaries
pub trait VolumePolicy {
    type Out;
    fn on_value(v: Scalar<Finite>) -> Self::Out;
}

/// Strict physics: fail if non-positive
pub enum Strict {}
impl VolumePolicy for Strict {
    type Out = Option<Scalar<Pos>>;

    #[inline(always)]
    fn on_value(v: Scalar<Finite>) -> Self::Out {
        Scalar::<Pos>::new(v.get())
    }
}

/// GA fitness: keep signed value (negatives are useful)
pub enum ForGA {}
impl VolumePolicy for ForGA {
    type Out = Scalar<Finite>;

    #[inline(always)]
    fn on_value(v: Scalar<Finite>) -> Self::Out {
        v
    }
}

/// Debug/batch mode: panic on invalid
pub enum Abort {}
impl VolumePolicy for Abort {
    type Out = Scalar<Pos>;

    #[inline(always)]
    fn on_value(v: Scalar<Finite>) -> Self::Out {
        Scalar::<Pos>::new(v.get()).expect("non-positive string volume")
    }
}
```

### Single Implementation, Multiple Behaviors

```rust
/// Internal: compute the raw value (always finite)
#[inline(always)]
fn volume_string_raw(
    kappa: &NonEmptyIntersection,
    t: &Moduli<'_>,
    h11: i32,
    h21: i32,
) -> Scalar<Finite> {
    let classical = volume_classical(kappa, t);  // PositiveF64
    let bbhl = bbhl_correction(h11, h21);
    // finite - finite = finite
    Scalar::<Finite>::new(classical.get() - bbhl).unwrap()
}

/// Compute string volume with policy-determined handling
#[inline(always)]
pub fn volume_string<P: VolumePolicy>(
    kappa: &NonEmptyIntersection,
    t: &Moduli<'_>,
    h11: i32,
    h21: i32,
) -> P::Out {
    P::on_value(volume_string_raw(kappa, t, h11, h21))
}
```

### Usage

```rust
// Strict: returns None if non-positive
let v_strict: Option<Scalar<Pos>> = volume_string::<Strict>(kappa, t, h11, h21);

// GA: returns Finite, can be negative
let v_ga: Scalar<Finite> = volume_string::<ForGA>(kappa, t, h11, h21);

// Debug: panics if non-positive
let v_abort: Scalar<Pos> = volume_string::<Abort>(kappa, t, h11, h21);
```

### Why Policy on Output, Not Input

The "invalid but useful" boundary is created by the **computation** (`classical - bbhl`), not inherent in the inputs. The inputs are always valid (positive κ, positive t). The output can become invalid due to physics (BBHL > classical).

Policy-on-output is the right axis.

### Keep Strict Where Possible

Only use policy switching where physics can invalidate:

```rust
// Always strict: inputs guarantee positive output
pub fn volume_classical(...) -> Scalar<Pos> { ... }

// Policy-switched: computation can produce negative
pub fn volume_string<P: VolumePolicy>(...) -> P::Out { ... }
pub fn vacuum_energy<P: VolumePolicy>(...) -> P::Out { ... }
```

## Summary

| Boundary Type | Enforced By | Failure Mode | Use Case |
|--------------|-------------|--------------|----------|
| Type (bugs) | Type system | Won't compile / panic | Always |
| Physics (exploration) | Policy type | `Strict` → None, `ForGA` → keep value | Depends on context |

The type system catches **bugs**. Policy types handle **physics boundaries** - write the math once, choose the behavior at the call site.

**Rule of thumb:** If a computation can produce "invalid but useful" values, use a policy type. If invalid means something is fundamentally broken, use strict types that prevent it entirely.
