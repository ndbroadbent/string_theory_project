# Divisor Basis Selection

We need a linearly independent basis of divisors $D_1, \dots, D_{h^{1,1}}$ to express the Kähler form $J = \sum t^a D_a$ (Demirtas et al. 2022, Sec. 3.1).

### Algorithm
The basis is selected by finding a subset of the prime toric divisors (rays of the fan) that form an integral basis for the group of divisors modulo linear equivalence.

1.  **Input**:
    *   Set of prime toric divisors (points $v_i$ on the boundary of the polytope).
    *   Construct the **Linear Relations Matrix** $L$: Columns are the vectors $(1, v_i)$. This enforces the Calabi-Yau condition (sum of charges = 0).

2.  **Sublattice Index**:
    *   Compute the Smith Normal Form (SNF) of $L$.
    *   The determinant of the non-zero diagonal elements gives the "sublattice index" (volume of the unit cell spanned by the points).

3.  **Search for Basis Columns**:
    *   The goal is to find a subset of $h^{1,1}$ indices $B$ such that the submatrix $L_B$ has the same determinant (up to sign) as the full system's sublattice index.
    *   **Strategy**:
        1.  Sort indices by various heuristics (L1 norm of points, LLL-reduced norms, random shuffle).
        2.  Iterate through heuristics. For each sorted list, pick the first $h^{1,1}$ columns that are linearly independent.
        3.  Check if this submatrix $L_B$ is an integral basis (i.e., its HNF determinant matches the sublattice index).
    *   **Determinism**: The default heuristic sorts by L1 norm. However, ties or different sorting stability can lead to different bases across versions (e.g., CYTools 2021 vs 2025).

4.  **Result**:
    *   Returns the list of indices $B = \{b_1, \dots, b_{h^{1,1}}\}$.

5.  **Intersection Number Transformation**:
    *   The intersection numbers for the basis are simply the subset of the full tensor:
        $$ \kappa^{\text{basis}}_{ijk} = \kappa^{\text{full}}_{b_i b_j b_k} $$
    *   This is valid because we express the Kähler form $J$ only in terms of these basis divisors.