# Formal Verification Strategy for Cyrus

## Overview
The cyrus Rust toolkit for Calabi-Yau manifold computations is a prime candidate for formal verification using Aeneas. Unlike typical software where bugs cause crashes, **physics code bugs produce plausible-looking wrong answers**.

Formal verification provides mathematical certainty that our implementation matches the physics formulas.

## Why Formal Verification Matters Here

### The Problem with Physics Code
Physics code often lacks a "ground truth" to compare against, especially for new Calabi-Yau manifolds. Small errors in symmetry handling or sign conventions can lead to:
- Incorrect cosmological constants.
- Divergent KKLT solvers.
- Corrupted downstream physics that still looks "reasonable" but is fundamentally wrong.

### Bugs Already Caught
- **2× Jacobian factor**: Caught only by numerical finite-difference tests.
- **BBHL sign/formula errors**: Found in early Python versions.
- **Basis transformation matrix transpose errors**.

## High-Value Verification Targets

### 1. Intersection Tensor Symmetry (`intersection.rs`)
The symmetry handling is subtle and bug-prone.
- **Prove**: `kappa.get(i,j,k) == kappa.get(permutation(i,j,k))` for all 6 permutations.
- **Goal**: Ensure no silent corruption of downstream physics.

### 2. Divisor Volume / Jacobian Consistency (`divisor.rs`)
- **Prove**: `∀ t, kappa: ∂(compute_divisor_volumes)/∂t == compute_divisor_jacobian`.
- **Goal**: Ensure the chain rule holds for the KKLT solver.

### 3. Flat Direction Linear Algebra (`flat_direction.rs`)
- **Prove**: If `solve_linear_system(N, K) = Some(p)`, then `N @ p == K`.
- **Prove**: Pivoting doesn't change the solution.

### 4. Volume Formula Consistency
- **Prove**: `compute_divisor_volumes` is indeed the gradient of `volume_classical`.
- `V = (1/6) κ_ijk t^i t^j t^k`
- `τ_i = (1/2) κ_ijk t^j t^k = ∂V/∂t^i`

### 5. BBHL Correction Sign
- **Formula**: `BBHL = ζ(3) * χ / (4 * (2π)³)` where `χ = 2(h11 - h21)`.
- **Prove**: `V_string = V_classical - BBHL` (minus, not plus!).

## Suggested Approach
Start with `intersection.rs` as it's the foundation:
1. Prove `canonical_key` is idempotent and symmetric.
2. Prove `symmetry_multiplicity` correctly counts permutations.
3. Prove `contract_triple` equals the explicit sum over all (i,j,k).
