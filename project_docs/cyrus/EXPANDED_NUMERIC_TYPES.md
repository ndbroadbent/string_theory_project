# Expanded Numeric Type System

This document describes the comprehensive type-safe numeric system for Cyrus, building on the patterns in `TYPE_SAFETY.md`.

## Goals

1. **Ban NaN and infinity** at the type level - `FiniteF64` as the base
2. **Trait lattice** for ergonomic function signatures - accept `PositiveF64` OR `OneF64`
3. **Dimension branding** with HRTB - unforgeable brands that tie vectors to their dimensions
4. **Branded indices** - `Index<'id>` that can only be created via safe paths
5. **Compile-time proofs** via `trybuild` - prove invariants hold

## Part 1: Scalar Type Lattice

### The Hierarchy

```
                    f64 (raw, untrusted)
                     │
                  Finite (no NaN, no ±∞)
                 /   │   \
          Positive  Zero  Negative
              │             │
             One        MinusOne
```

### Single Generic Wrapper

Instead of separate structs, use one `#[repr(transparent)]` wrapper with phantom tags:

```rust
#[derive(Clone, Copy, Debug)]
#[repr(transparent)]
pub struct Scalar<Tag>(f64, PhantomData<Tag>);

// Tags (zero-sized types)
pub struct Finite;
pub struct Pos;
pub struct Neg;
pub struct Zero;
pub struct One;
pub struct MinusOne;
```

### Trait Lattice

Traits express "is at least this constrained":

```rust
/// Guaranteed finite (no NaN, no ±∞)
pub trait IsFinite: Copy {
    fn finite(self) -> Scalar<Finite>;
    fn get(self) -> f64;
}

/// Guaranteed > 0
pub trait IsPositive: IsFinite {
    fn positive(self) -> Scalar<Pos>;
}

/// Guaranteed < 0
pub trait IsNegative: IsFinite {
    fn negative(self) -> Scalar<Neg>;
}

/// Guaranteed == 0
pub trait IsZero: IsFinite {
    fn zero(self) -> Scalar<Zero>;
}

/// Guaranteed == 1.0
pub trait IsOne: IsPositive {}

/// Guaranteed == -1.0
pub trait IsMinusOne: IsNegative {}
```

### Impl Hierarchy

```rust
// Everything implements IsFinite
impl IsFinite for Scalar<Finite> { ... }
impl IsFinite for Scalar<Pos> { ... }
impl IsFinite for Scalar<Neg> { ... }
impl IsFinite for Scalar<Zero> { ... }
impl IsFinite for Scalar<One> { ... }
impl IsFinite for Scalar<MinusOne> { ... }

// Positive types implement IsPositive
impl IsPositive for Scalar<Pos> { ... }
impl IsPositive for Scalar<One> { ... }

// Negative types implement IsNegative
impl IsNegative for Scalar<Neg> { ... }
impl IsNegative for Scalar<MinusOne> { ... }

// Zero implements IsZero
impl IsZero for Scalar<Zero> { ... }

// One implements IsOne
impl IsOne for Scalar<One> {}

// MinusOne implements IsMinusOne
impl IsMinusOne for Scalar<MinusOne> {}
```

### Function Signatures

Accept any type that satisfies the constraint:

```rust
// Accepts Scalar<Pos>, Scalar<One>, etc.
fn sqrt<T: IsPositive>(x: T) -> Scalar<Pos> {
    Scalar::new_pos_unchecked(x.get().sqrt())
}

// Accepts Scalar<Finite>, Scalar<Pos>, Scalar<Neg>, etc.
fn add<T: IsFinite, U: IsFinite>(a: T, b: U) -> Scalar<Finite> {
    Scalar::new_finite(a.get() + b.get()).unwrap()
}

// Accepts Scalar<One> specifically (for optimizations)
fn mul_by_one<T: IsFinite>(x: T, _one: Scalar<One>) -> T {
    x  // No-op! Compiler can eliminate
}
```

### Operator Semantics

Operations return the strongest provable type:

| Operation | Result |
|-----------|--------|
| `Pos + Pos` | `Pos` |
| `Neg + Neg` | `Neg` |
| `Pos + Neg` | `Finite` (sign unknown) |
| `Pos + Zero` | `Pos` |
| `Pos * Pos` | `Pos` |
| `Neg * Neg` | `Pos` |
| `Pos * Neg` | `Neg` |
| `Pos * Zero` | `Zero` |
| `One * T` | `T` (identity) |
| `Pos / Pos` | `Pos` |
| `Finite / Zero` | **Does not compile** |
| `-Pos` | `Neg` |
| `-Neg` | `Pos` |
| `-Zero` | `Zero` |

### Constructors (The Boundary)

```rust
impl Scalar<Finite> {
    pub fn new(x: f64) -> Option<Self> {
        x.is_finite().then(|| Self(x, PhantomData))
    }
}

impl Scalar<Pos> {
    pub fn new(x: f64) -> Option<Self> {
        (x.is_finite() && x > 0.0).then(|| Self(x, PhantomData))
    }
}

impl Scalar<Zero> {
    pub const ZERO: Self = Self(0.0, PhantomData);
}

impl Scalar<One> {
    pub const ONE: Self = Self(1.0, PhantomData);
}

impl Scalar<MinusOne> {
    pub const MINUS_ONE: Self = Self(-1.0, PhantomData);
}
```

### Compile-Time Literals

```rust
/// Compile-time verified positive literal
macro_rules! pos {
    ($val:expr) => {{
        const V: f64 = $val;
        const _: () = assert!(V > 0.0, "pos! requires positive value");
        Scalar::<Pos>::new_unchecked(V)
    }};
}

/// Compile-time verified finite literal
macro_rules! finite {
    ($val:expr) => {{
        const V: f64 = $val;
        const _: () = assert!(V.is_finite(), "finite! requires finite value");
        Scalar::<Finite>::new_unchecked(V)
    }};
}
```

---

## Part 2: Dimension Branding

### The Problem

```rust
fn dot(a: &[f64], b: &[f64]) -> f64 {
    assert_eq!(a.len(), b.len());  // Runtime check - can we eliminate?
    a.iter().zip(b).map(|(x, y)| x * y).sum()
}
```

### The Solution: HRTB Branding

Use higher-ranked trait bounds to create unforgeable brand lifetimes:

```rust
pub struct Dim {
    n: usize,
}

/// Invariant brand - cannot be forged or escape
pub struct Brand<'id>(PhantomData<*mut &'id ()>);

// Brand is invariant, not Copy, not Clone
// The *mut makes it invariant in 'id

impl Dim {
    pub fn new(n: usize) -> Self {
        Self { n }
    }

    /// Enter a branded context. The brand cannot escape.
    pub fn with_brand<R, F>(&self, f: F) -> R
    where
        F: for<'id> FnOnce(Brand<'id>) -> R,
    {
        // Brand is created here and cannot outlive the closure
        f(Brand(PhantomData))
    }

    pub fn n(&self) -> usize {
        self.n
    }
}
```

### Branded Vectors

```rust
pub struct BVec<'id, T> {
    data: Vec<T>,
    _brand: PhantomData<Brand<'id>>,
}

impl<'id, T> BVec<'id, T> {
    /// Create a branded vector. Panics if wrong length.
    pub fn new(dim: &Dim, _brand: Brand<'id>, data: Vec<T>) -> Self {
        assert_eq!(data.len(), dim.n(), "dimension mismatch");
        Self {
            data,
            _brand: PhantomData,
        }
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    /// Safe indexing with branded index
    pub fn get(&self, idx: Index<'id>) -> &T {
        // SAFETY: Index<'id> can only be created for valid indices
        debug_assert!(idx.0 < self.data.len());
        unsafe { self.data.get_unchecked(idx.0) }
    }

    pub fn get_mut(&mut self, idx: Index<'id>) -> &mut T {
        debug_assert!(idx.0 < self.data.len());
        unsafe { self.data.get_unchecked_mut(idx.0) }
    }
}
```

### Branded Indices

```rust
#[derive(Clone, Copy, Debug)]
pub struct Index<'id> {
    i: usize,
    _brand: PhantomData<Brand<'id>>,
}

impl Dim {
    /// Iterate over valid indices for this dimension
    pub fn indices<'id>(&self, _brand: Brand<'id>) -> impl Iterator<Item = Index<'id>> {
        (0..self.n).map(|i| Index {
            i,
            _brand: PhantomData,
        })
    }

    /// Try to create an index, checking bounds
    pub fn index<'id>(&self, _brand: Brand<'id>, i: usize) -> Option<Index<'id>> {
        (i < self.n).then(|| Index {
            i,
            _brand: PhantomData,
        })
    }
}
```

### Usage

```rust
let dim = Dim::new(3);

dim.with_brand(|brand| {
    let a = BVec::new(&dim, brand, vec![1.0, 2.0, 3.0]);
    let b = BVec::new(&dim, brand, vec![4.0, 5.0, 6.0]);

    // This is statically safe - no bounds checks in release
    for i in dim.indices(brand) {
        let sum = a.get(i) + b.get(i);
        println!("{sum}");
    }
});
```

### What This Guarantees

- `BVec<'id, T>` and `BVec<'id, U>` have the same length (same brand)
- `Index<'id>` is always valid for `BVec<'id, T>` (same brand)
- Cannot mix vectors from different `with_brand` calls
- Cannot forge an index from raw `usize`

### What This Does NOT Guarantee

- The length is some specific number (use const generics for that)
- An arbitrary `usize` is in bounds (must go through `dim.index()`)

---

## Part 3: Multi-Dimensional (Matrices)

For matrices, we need separate row and column brands:

```rust
pub struct BMat<'row, 'col, T> {
    data: Vec<T>,  // row-major: data[row * ncols + col]
    nrows: usize,
    ncols: usize,
    _row_brand: PhantomData<Brand<'row>>,
    _col_brand: PhantomData<Brand<'col>>,
}

#[derive(Clone, Copy)]
pub struct RowIdx<'row>(usize, PhantomData<Brand<'row>>);

#[derive(Clone, Copy)]
pub struct ColIdx<'col>(usize, PhantomData<Brand<'col>>);

impl<'row, 'col, T> BMat<'row, 'col, T> {
    pub fn get(&self, row: RowIdx<'row>, col: ColIdx<'col>) -> &T {
        debug_assert!(row.0 < self.nrows && col.0 < self.ncols);
        unsafe { self.data.get_unchecked(row.0 * self.ncols + col.0) }
    }
}
```

### Square Matrices

For square matrices, use the same brand for both:

```rust
pub type BSquareMat<'id, T> = BMat<'id, 'id, T>;

// Now RowIdx<'id> and ColIdx<'id> are interchangeable
```

### Matrix-Vector Multiplication

```rust
fn mat_vec_mul<'row, 'col, T>(
    mat: &BMat<'row, 'col, T>,
    vec: &BVec<'col, T>,  // Must match matrix columns
) -> BVec<'row, T>        // Result matches matrix rows
where
    T: std::ops::Mul<Output = T> + std::ops::Add<Output = T> + Copy + Default,
{
    // Type system guarantees vec.len() == mat.ncols
    // ...
}
```

---

## Part 4: Checked Ranges (Compile-Time)

For compile-time range validation:

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct CheckedRange<T> {
    pub start: T,
    pub end: T,
}

impl<T> CheckedRange<T> {
    pub const fn new(start: T, end: T) -> Self {
        Self { start, end }
    }
}

#[macro_export]
macro_rules! range {
    ($start:expr .. $end:expr) => {{
        const S: usize = $start;
        const E: usize = $end;
        const _: () = {
            if !(S < E) {
                panic!("range! requires start < end");
            }
        };
        $crate::CheckedRange::new(S, E)
    }};
}

// Usage:
const R: CheckedRange<usize> = range!(3..10);  // OK
// const BAD: CheckedRange<usize> = range!(10..3);  // Compile error!
```

---

## Part 5: Compile-Fail Tests with trybuild

### Setup

```toml
# Cargo.toml
[dev-dependencies]
trybuild = "1"
```

### Test Harness

```rust
// tests/trybuild.rs
#[test]
fn ui() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/ui/*.rs");
}
```

### Test Cases

**tests/ui/mix_brands.rs** - Prove brands can't be mixed:
```rust
use cyrus_core::dimension::{Dim, BVec};

fn main() {
    let d1 = Dim::new(3);
    let d2 = Dim::new(3);

    d1.with_brand(|b1| {
        d2.with_brand(|b2| {
            let a = BVec::new(&d1, b1, vec![1, 2, 3]);
            let b = BVec::new(&d2, b2, vec![4, 5, 6]);

            // ERROR: different brands
            for i in d1.indices(b1) {
                let _ = b.get(i);  // Should not compile!
            }
        })
    });
}
```

**tests/ui/forge_index.rs** - Prove indices can't be forged:
```rust
use cyrus_core::dimension::{Dim, BVec, Index};

fn main() {
    let dim = Dim::new(3);

    dim.with_brand(|brand| {
        let v = BVec::new(&dim, brand, vec![1, 2, 3]);

        // ERROR: can't create Index from raw usize
        let fake_idx: Index<'_> = Index { i: 0, _brand: std::marker::PhantomData };
        let _ = v.get(fake_idx);
    });
}
```

**tests/ui/escape_brand.rs** - Prove brands can't escape:
```rust
use cyrus_core::dimension::{Dim, Brand};

fn main() {
    let dim = Dim::new(3);

    // ERROR: brand cannot escape the closure
    let escaped: Brand<'_> = dim.with_brand(|brand| brand);
}
```

**tests/ui/nan_scalar.rs** - Prove NaN is rejected:
```rust
use cyrus_core::scalar::Scalar;

fn main() {
    // ERROR: NaN not allowed
    let _ = Scalar::<Finite>::new(f64::NAN).unwrap();  // Panics at runtime

    // But this is the real test - compile-time literals
    // const BAD: Scalar<Pos> = pos!(f64::NAN);  // Should not compile
}
```

### Running Tests

```bash
cargo test

# Update expected error output after intentional changes:
TRYBUILD=overwrite cargo test
```

---

## Part 6: Integration with Existing Code

### Migration Path

1. **Phase 1**: Implement `scalar.rs` with `Scalar<Tag>` and trait lattice
2. **Phase 2**: Implement `dimension.rs` with HRTB branding
3. **Phase 3**: Add trybuild tests
4. **Phase 4**: Migrate existing `Positive<T>`, `Negative<T>` to new system
5. **Phase 5**: Migrate `Dim<'a>`, `Moduli<'a>` to branded system

### Type Aliases for Compatibility

```rust
// Backwards compatibility during migration
pub type PositiveF64 = Scalar<Pos>;
pub type NegativeF64 = Scalar<Neg>;
pub type FiniteF64 = Scalar<Finite>;
```

### File Structure

```
crates/cyrus-core/src/types/
├── mod.rs
├── scalar.rs       # Scalar<Tag>, tags, trait lattice, ops
├── dimension.rs    # Dim, Brand, BVec, BMat, Index, RowIdx, ColIdx
├── range.rs        # CheckedRange, range! macro
└── ...

crates/cyrus-core/tests/
├── trybuild.rs     # Harness
└── ui/             # Compile-fail cases
    ├── mix_brands.rs
    ├── forge_index.rs
    ├── escape_brand.rs
    └── nan_scalar.rs
```

---

## Part 7: Number Classes (Research/Future)

Beyond basic sign tracking, there are richer "classes" of numbers that appear throughout CY/flux/moduli computations. These enable:
- **Formula selection** - pick numerically stable algorithms
- **Early pruning** - reject candidates before expensive computation
- **Representation choice** - use fast paths when possible

### 7.1 Discreteness Classes (Exact Arithmetic)

Most CY/flux work involves integer lattice data:

| Class | Values | Use Cases |
|-------|--------|-----------|
| `Bool01` | `{0, 1}` | Incidence, adjacency, selection vectors |
| `Sign` | `{-1, 0, +1}` | Cone generators, charge vectors |
| `IntSmall` | `\|x\| ≤ 2^31` | Machine ints, fast arithmetic |
| `IntBig` | arbitrary | Malachite path, triggers caching |
| `Primitive` | `gcd(vec) = 1` | Rays, lattice points, cache keys |

```rust
pub struct Bool01;      // {0, 1}
pub struct Sign;        // {-1, 0, +1}
pub struct IntSmall;    // fits in i64
pub struct IntBig;      // arbitrary precision
pub struct Primitive;   // gcd-normalized vector
```

### 7.2 Positivity/Cone Classes

Critical for pruning invalid physics:

| Class | Constraint | Use Cases |
|-------|------------|-----------|
| `Pos` | `x > 0` | Volumes, norms, moduli |
| `NonNeg` | `x ≥ 0` | Kähler parameters, slack |
| `UnitInterval` | `0 ≤ x ≤ 1` | Barycentric, convex combos |
| `CosRange` | `-1 ≤ x ≤ 1` | Trig domains (rare in CY) |

```rust
pub struct UnitInterval;  // [0, 1]
pub struct CosRange;      // [-1, 1]

pub trait IsUnitInterval: IsNonNeg {
    fn unit(self) -> Scalar<UnitInterval>;
}
```

### 7.3 Magnitude Classes (Numerical Stability)

Aligned to `f64` behavior, not human intuition:

| Class | Range | Meaning |
|-------|-------|---------|
| `Tiny` | `0 < \|x\| < 1e-300` | Subnormal, underflow risk |
| `Small` | `\|x\| < 1e-12` | "Treat as zero" threshold |
| `Normal` | `1e-6 ≤ \|x\| ≤ 1e6` | Numerically comfortable |
| `Large` | `\|x\| > 1e12` | Conditioning concerns |
| `Huge` | `\|x\| > 1e300` | Near overflow |

```rust
pub struct MagnitudeTiny;
pub struct MagnitudeSmall;
pub struct MagnitudeNormal;  // O(1)
pub struct MagnitudeLarge;
pub struct MagnitudeHuge;

// Threshold constants
pub const EPS_TINY: f64 = 1e-300;
pub const EPS_SMALL: f64 = 1e-12;
pub const LARGE_THRESHOLD: f64 = 1e12;
```

### 7.4 Boundary Classes (Cone Constraints)

Extremely useful for "circuit breaker" staging:

| Class | Meaning | Action |
|-------|---------|--------|
| `Interior` | `Ax ≥ ε` for all constraints | Safe with floats |
| `NearBoundary` | Some constraint in `[0, ε)` | Need exact fallback |
| `Outside` | Violates a constraint | Prune immediately |

```rust
pub struct Interior<const EPS: usize>;    // margin class
pub struct NearBoundary;
pub struct Outside;

// This drives the float-first, exact-near-boundary staging
pub enum ConePosition {
    Interior { min_margin: f64 },
    NearBoundary { constraint_idx: usize, value: f64 },
    Outside { constraint_idx: usize, value: f64 },
}
```

### 7.5 Ultra-Small Classes (Cosmological Constant Territory)

For quantities like `Λ ~ 10^-122`:

| Class | Meaning | Note |
|-------|---------|------|
| `TargetSmall` | `\|x\| ≤ Λ_max` | Symbolic threshold |
| `CertifiedSmall` | Passed exact arithmetic | High confidence |
| `ApproxSmall` | Float check only | May have cancellation error |
| `CancellationDerived` | Small due to subtraction | Stability concern |

```rust
/// Small due to being literally tiny
pub struct LiterallySmall;

/// Small due to cancellation (subtraction of similar values)
/// This is where stability and exact checks matter most
pub struct CancellationSmall;

pub trait SmallnessSource {
    fn is_from_cancellation(&self) -> bool;
}
```

### 7.6 Minimal High-Leverage Class Set

For CY/flux/moduli scanning, start with these tags:

```rust
// Core (implement first)
pub struct Finite;
pub struct Pos;
pub struct Neg;
pub struct Zero;
pub struct One;

// Extended sign
pub struct NonNeg;      // x ≥ 0
pub struct NonPos;      // x ≤ 0

// Intervals
pub struct UnitInterval;  // [0, 1]
pub struct OpenUnit;      // (0, 1)

// Discreteness
pub struct Bool01;
pub struct Sign3;         // {-1, 0, +1}

// Magnitude (add only if profiling demands)
pub struct NearZero;      // |x| < ε
pub struct MarginPos<const EPS_CLASS: u8>;  // x > ε
```

### 7.7 Trait Relationships

```
                    IsFinite
                   /    |    \
           IsPositive  IsZero  IsNegative
              |                    |
          IsNonNeg              IsNonPos
              |    \          /    |
        IsUnitInterval    IsCosRange
              |
          IsOpenUnit
              |
            IsOne
```

### 7.8 Research Questions

1. **Moduli representation**: integers/rationals or floats?
2. **Primary operations**: inequality checks (`Ax ≥ 0`) or solving (`Rλ = x, λ ≥ 0`)?
3. **Cancellation sensitivity**: how often do you compute near-zero from differences?

The answers determine which classes provide the most value.

---

## Summary

| Feature | Guarantee | Mechanism |
|---------|-----------|-----------|
| No NaN/∞ | All scalars are finite | `Scalar<Finite>` constructor checks |
| Sign tracking | Pos/Neg/Zero known | Tag types + operator impls |
| Identity optimization | `One * x = x` | Type-specialized impl |
| Same-length vectors | `a.len() == b.len()` | Same brand `'id` |
| Valid indices | `i < len` | `Index<'id>` only via `dim.indices()` |
| Dimension mismatch | Compile error | Different brand lifetimes |
| Magnitude awareness | Pick stable formulas | Magnitude class tags |
| Boundary staging | Float-first, exact when needed | `Interior`/`NearBoundary` |
| Cancellation tracking | Know when precision lost | `CancellationSmall` tag |

The trusted core is small:
- `Scalar::new()` constructors
- `BVec::new()` length check
- `dim.indices()` index generation

Everything else is provably correct by construction.
