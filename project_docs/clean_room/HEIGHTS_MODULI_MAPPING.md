# Mapping: Heights ↔ Kähler Moduli

This document provides the clean-room specification for mapping between triangulation height vectors and Kähler moduli (Kähler parameters). This mapping is essential for traversing the secondary fan and identifying the geometric phase of a physics vacuum.

## 1. Context: The Secondary Fan
*   **Heights** $h 
in \mathbb{R}^n$ (one per lattice point) parametrize the Secondary Fan of a polytope.
*   The **Secondary Cone** of a triangulation $T$ is the region in height space where the induced triangulation remains $T$.
*   **Kähler Moduli** $t 
in \mathbb{R}^{h^{1,1}}$ parametrize the Kähler cone, which is a projection of the secondary cone.

## 2. Algorithm: Heights → Kähler Moduli ($h \to t$)

Given a height vector $h$ (including the origin) and a choice of $h^{1,1}$ basis divisors:

1.  **Normalization**:
    Subtract the height of the origin $h_0$ from all other heights:
    $$ \bar{h}_i = h_i - h_0 $$
    (This removes the overall scaling/translation redundancy in height space).

2.  **Projection**:
    The Kähler parameters $t^a$ are obtained by projecting the normalized heights onto the basis.
    For a divisor basis defined by indices $B = \{b_1, \dots, b_{h^{1,1}}\}$:
    *   The heights of the basis divisors $\bar{h}_{b_a}$ are the initial candidates.
    *   **Linear Relations**:
        Use the GLSM charge matrix $Q$ (or linear relations matrix $L$) to account for the dependencies of non-basis points.
    *   Formula (Demirtas et al. 2022):
        $$ t^a = \bar{h}_{b_a} + \sum_{j \notin B} c_j^a \bar{h}_j $$
        where $c_j^a$ are coefficients derived from the linear relations such that the mapping is consistent with the volume of curves.

3.  **Physical Interpretation**:
    The Kähler parameters $t$ correspond to the volumes of the 2-cycles (curves) dual to the basis divisors. The heights $h$ act as a "potential" for these volumes.

## 3. Algorithm: Kähler Moduli → Heights ($t \to h$)

This mapping is used to find a representative point in the secondary fan for a given set of Kähler moduli.

1.  **Input**: Kähler parameters $t^a$.
2.  **Basis Heights**: Set the heights of the basis divisors to $t^a$:
    $$ \bar{h}_{b_a} = t^a $$
3.  **Origin**: Set $h_0 = 0$.
4.  **Dependent Heights**: Compute the heights of all other points using the linear relations:
    $$ \bar{h}_j = \sum_a R_{ja} t^a $$
    where $R$ is the matrix of linear relations expressing dependent divisors in terms of the basis.
5.  **Result**: The resulting vector $h$ is a point in the secondary fan that projects exactly to $t$.

## 4. Usage in Physics Pipeline

### 4.1 Branch Discovery
*   When searching for vacua, we may find multiple solutions for $t$ such that $\tau(t) = \tau_{\text{target}}$.
*   Each solution $t$ corresponds to a set of heights $h = \text{Map}(t)$.
*   By computing the triangulation induced by $h$, we determine which **geometric phase** (triangulation) the solution belongs to.

### 4.2 Random Sampling
*   Instead of sampling $t$ directly (which might be outside the Kähler cone), sample **heights** $h$ near the Delaunay heights ($|p|^2$).
*   Any valid regular triangulation corresponds to a non-empty Kähler cone.
*   Project $h \to t$ to get a valid starting point for moduli stabilization.

## 5. Implementation Notes (Rust)
*   The mapping is a **linear transformation** (matrix multiplication).
*   The projection matrix should be computed once per basis selection and cached.
*   Use `malachite::Rational` if exact mapping is required, or `f64` for numerical exploration.
