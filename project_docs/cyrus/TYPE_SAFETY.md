# Type Safety Philosophy in Cyrus

## Core Principle: The Compiler is the Physics Validator

String theory physics is **insanely hard to understand** and **incredibly easy to make mistakes**. One wrong sign, one invalid intermediate, one unvalidated constant - and you get nonsense results that look plausible.

Our solution: **if it compiles, the physics constraints are satisfied.**

The type system encodes physics constraints. Type errors = physics errors, caught at compile time, not runtime.

## The Rules

### 1. Everything is Typed

Every value has a type that encodes what we know about it:

```rust
// Constants
const ZETA_3 = f64_pos!(1.202_056_903_159_594);
const FOUR_TWO_PI_CUBED = f64_pos!(32.0 * 31.006_276_680_299_816); // π³ ≈ 31.006...

// Function signatures encode physics
pub fn bbhl_correction(h11: I32<Pos>, h21: I32<NonNeg>) -> F64<Finite>

// Even literals in formulas
let chi = I32::<Two>::TWO.get() * diff;
```

Not just inputs and outputs - **constants, intermediates, everything**.

### 2. Compile-Time Validation via Macros

Use `f64_pos!`, `f64_neg!`, `f64_finite!` for all literal values:

```rust
// Good - compile-time checked
const ZETA_3 = f64_pos!(1.202_056_903_159_594);
let coefficient = f64_pos!(4.0 / 3.0);

// These won't compile:
// f64_pos!(-1.0);       // Error: not positive
// f64_pos!(f64::NAN);   // Error: not finite
```

The macro validates at compile time. Zero runtime cost. Zero possibility of invalid values.

### 3. `from_raw` is Banned

`from_raw` bypasses validation. It exists only for the trusted core (macro implementations). Application code never uses it.

```rust
// BANNED - bypasses all checks
let x = F64::<Pos>::from_raw(some_value);

// REQUIRED - validated
let x = F64::<Pos>::new(some_value)?;  // Runtime value
let x = f64_pos!(1.5);                  // Compile-time literal
```

### 4. Formulas Stay Readable

Show the math, not magic numbers:

```rust
// Good - shows the derivation
const FOUR_TWO_PI_CUBED = f64_pos!(32.0 * 31.006_276_680_299_816); // π³ ≈ 31.006...

// Bad - magic number, no context
const FOUR_TWO_PI_CUBED = f64_pos!(992.200_658_169_593_3);
```

The reader should understand *why* the value is what it is.

### 5. The Trusted Core is Tiny

Only mathematically sound conversions are allowed without validation:

```rust
// Allowed - I32<Pos> is positive by definition, so F64<Pos> is guaranteed
impl From<I32<Pos>> for F64<Pos> { ... }

// Allowed - Pos implies NonZero implies Finite
impl IsFinite for F64<Pos> { ... }
impl IsNonZero for F64<Pos> { ... }
```

Everything else requires explicit validation at the boundary.

## Tag Hierarchy

```
IsFinite (base - no NaN, no ±∞)
   ├── IsNonZero (≠ 0) - critical for safe division
   │      ├── IsPositive (> 0) → IsOne, IsTwo
   │      └── IsNegative (< 0) → IsMinusOne
   ├── IsNonNeg (≥ 0)
   ├── IsNonPos (≤ 0)
   └── IsZero (= 0)
```

Key insight: `NonZero.abs() = Pos` (not just `NonNeg`).

## Arithmetic Rules

The type system encodes sign algebra:

| Operation | Result |
|-----------|--------|
| `Pos + Pos` | `Pos` |
| `Neg + Neg` | `Neg` |
| `Pos + Neg` | `Finite` (unknown sign) |
| `Pos * Pos` | `Pos` |
| `Neg * Neg` | `Pos` |
| `Pos * Neg` | `Neg` |
| `Pos / Pos` | `Pos` |
| `NonZero.abs()` | `Pos` |
| `Finite.abs()` | `NonNeg` |

Division by `Zero` is **impossible** - no `Div<Zero>` impl exists.

## Physics Validation Pattern

### Validate at the Boundary

```rust
// Geometry computation produces raw f64
let computed_kappa = /* ... complex calculation ... */;

// Boundary: validate and convert to typed
let kappa = F64::<Pos>::new(computed_kappa)
    .ok_or(Error::InvalidPhysics("κ_ijk must be positive"))?;

// Everything downstream uses typed values - zero runtime checks
let volume = contract_triple(&kappa, &t);  // Guaranteed Pos
let v0 = compute_v0(ek0, g_s, volume, w0);  // Guaranteed Neg
```

### Push Validation Upstream

The boundary should be as early as possible:

```
GA proposes candidate
      ↓
Compute κ_ijk from geometry
      ↓
κ_ijk <= 0? ──→ ABORT (zero wasted cycles)
      ↓
κ_ijk: F64<Pos> ✓
      ↓
All downstream guaranteed by types
```

## Newtype Wrappers

For collection invariants, use newtype wrappers:

```rust
struct NonEmptyIntersection(Intersection);

impl NonEmptyIntersection {
    fn new(inner: Intersection) -> Option<Self> {
        (!inner.is_empty()).then(|| Self(inner))
    }
}

// Functions that require non-empty take the wrapper
fn volume_classical(kappa: &NonEmptyIntersection, t: &Moduli) -> F64<Pos>
```

Check once at construction, trust the type everywhere else.

## Policy Types for Physics Boundaries

Some computations produce values that are "invalid but useful" during GA exploration:

```rust
pub trait VolumePolicy {
    type Output;
    fn apply(v: F64<Finite>) -> Self::Output;
}

// Strict: fail if non-positive (for validated pipelines)
impl VolumePolicy for Strict {
    type Output = Option<F64<Pos>>;
}

// ForGA: keep signed value (for fitness computation)
impl VolumePolicy for ForGA {
    type Output = F64<Finite>;
}

// Usage
let v = volume_string_with_policy::<Strict>(&kappa, &t, h11, h21);  // Option<F64<Pos>>
let v = volume_string_with_policy::<ForGA>(&kappa, &t, h11, h21);   // F64<Finite>
```

## Summary

1. **Every value is typed** according to what we know about it
2. **Compile-time macros** validate literals (`f64_pos!`, etc.)
3. **`from_raw` is banned** outside the trusted core
4. **Formulas stay readable** - show the math
5. **The compiler catches physics errors** - if it compiles, constraints are satisfied
6. **Trusted core is tiny** - only mathematically sound conversions
7. **Validate at the boundary** - push checks upstream
8. **Policy types** handle "invalid but useful" GA exploration

The goal: make it **impossible** to express invalid physics in the type system.
