# Formal Verification Strategy: Cyrus

This document outlines the strategy for formally verifying the Cyrus physics engine using Aeneas and Lean 4.

## Core Philosophy
We do not verify everything. We verify the **High-Risk / High-Value** mathematical kernels where bugs produce silent, plausible-looking errors.

## Verification Targets

### 1. Intersection Tensor (Layer 1)
- **Code**: `cyrus-core/src/intersection.rs`
- **Risk**: Index permutation errors corrupt physics silently.
- **Theorems**:
  - `kappa_symmetry`: $\kappa_{ijk} = \kappa_{\sigma(i)\sigma(j)\sigma(k)}$ for any permutation $\sigma$.
  - `contract_triple_correctness`: Optimized contraction matches explicit sum.

### 2. Volume & Gradients (Layer 2)
- **Code**: `cyrus-core/src/volume.rs`, `divisor.rs`
- **Risk**: Sign errors or factor-of-2 errors in derivatives diverge the KKLT solver.
- **Theorems**:
  - `volume_gradient_consistency`: $\nabla_t V_{classical} = \tau$ (Divisor volumes).
  - `jacobian_consistency`: $\nabla_t \tau = \partial^2 V$.
  - `bbhl_sign`: $V_{string} = V_{classical} - V_{bbhl}$ (Verify sign convention).

### 3. Linear Algebra (Layer 3)
- **Code**: `cyrus-core/src/flat_direction.rs`
- **Risk**: Gaussian elimination pivoting errors.
- **Theorems**:
  - `solve_correctness`: $Ax = b \implies x$ is a solution.
  - `pivoting_stability`: Pivoting choice does not alter solution.

## Proof Architecture
We follow the layered architecture from `lean_experiment`:

### Layer 0: Foundation
- **File**: `Cyrus/Foundation.lean`
- **Content**: Basic lemmas about `U32`, `F64` (axiomatized), and `List`/`Array`.

### Layer 1: Primitive Specs
- **File**: `Cyrus/IntersectionSpec.lean`
- **Content**: Pure math definitions of intersection numbers and symmetry.

### Layer 2: Implementation Proofs
- **File**: `Cyrus/IntersectionProofs.lean`
- **Content**: Refinement proofs showing Rust implementation matches Primitive Specs.

### Layer 3: Physics Theorems
- **File**: `Cyrus/PhysicsTheorems.lean`
- **Content**: Higher-level properties (Gradient consistency, etc.) derived from Specs.

## Workflow
1.  **Extract**: Run `charon` on `cyrus-core`.
2.  **Translate**: Run `aeneas` to generate `Cyrus/Generated/`.
3.  **Prove**: Write proofs in `Cyrus/ Proofs/` importing Generated code.
4.  **CI**: Run `lake build` in CI to ensure proofs stay valid.

## Tooling
- **Aeneas**: For Rust -> Lean translation.
- **Mathlib**: For background mathematics (Group theory for permutations, Analysis for gradients).
