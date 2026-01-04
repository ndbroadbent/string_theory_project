# Intersection Number Transformation and Origin Handling

This document specifies how to transform the raw intersection tensor (computed for all divisors) into the basis-dependent form used for physics computations, and how to handle the special "origin" divisor (canonical divisor).

## 1. Origin Handling (Canonical Divisor)

The intersection numbers computed via the linear system (see [[project_docs/clean_room/INTERSECTION_NUMBERS.md|INTERSECTION_NUMBERS.md]]) typically exclude the origin (index 0) or treat it implicitly.

### The Problem
The linear system method computes $\kappa_{ijk}$ for $i,j,k ∈ \{1, \dots, N\}$.
However, we often need intersection numbers involving the canonical divisor $D_0$ (corresponding to the origin point in the polytope).

### Algorithm
1.  **Linear Equivalence**:
The sum of all toric divisors is linearly equivalent to the zero divisor (if working in the anticanonical bundle convention) or the anticanonical class.
    $$ \sum_{i=0}^N D_i \sim 0 $$
    Therefore:
    $$ D_0 \sim - \sum_{i=1}^N D_i $$

2.  **Recursive Computation**:
To compute an intersection number involving $D_0$, expand it using the relation above:
    $$ \kappa_{0jk} = D_0 \cdot D_j \cdot D_k = - \sum_{i=1}^N (D_i \cdot D_j \cdot D_k) = - \sum_{i=1}^N \kappa_{ijk} $$
    $$ \kappa_{00k} = - \sum_{i=1}^N \kappa_{i0k} $$
    $$ \kappa_{000} = - \sum_{i=1}^N \kappa_{i00} $$

3.  **Order of Operations**:
    *   Compute all $\kappa_{ijk}$ for $i,j,k \in \{1, \dots, N\}$.
    *   Compute $\kappa_{0jk}$ for $j,k \in \{1, \dots, N\}$ using the sum.
    *   Compute $\kappa_{00k}$ for $k \in \{1, \dots, N\}$ using the new $\kappa_{0jk}$ values.
    *   Compute $\kappa_{000}$.

## 2. Basis Transformation

Physics quantities (like the $N$-matrix and $e^{K_{cs}}$) are defined in terms of a basis of $h^{1,1}$ linearly independent divisors.

### Case A: Basis is a Subset of Divisors
If the basis is specified as a list of indices $B = \{b_1, \dots, b_{h^{1,1}}\ \}$: 
*   **Transformation**: Simply extract the subtensor.
    $$ \kappa^{\text{basis}}_{xyz} = \kappa^{\text{full}}_{b_x b_y b_z} $$
*   **Validity**: This assumes that the full intersection tensor $\kappa^{\text{full}}$ is correct and that the chosen basis $B$ spans the cohomology such that all relevant physics is captured.

### Case B: Basis is a Linear Combination (Matrix)
If the basis is specified as a matrix $T$ of shape $(h^{1,1}, N+1)$, where the rows are basis vectors expressed in terms of the original divisors:
$$ D^{\text{basis}}_a = \sum_{i=0}^N T_{ai} D_i $$

*   **Transformation**: Full tensor contraction.
    $$ \kappa^{\text{basis}}_{abc} = \sum_{i,j,k} T_{ai} T_{bj} T_{ck} \kappa^{\text{full}}_{ijk} $$
*   **Implementation**: Use `tensordot` or equivalent.
    *   Contract axis 0 of $\kappa$ with axis 1 of $T^T$.
    *   Repeat for axes 1 and 2.

### 3. Debugging McAllister's 4-214-647
If the basis $[3,4,5,8]$ yields a singular $N$-matrix:
1.  **Check Origin Handling**: Ensure $\kappa$ involving index 0 is computed correctly if the basis uses it (though $[3,4,5,8]$ does not).
2.  **Check Full Tensor**: If $\kappa^{\text{basis}}$ is sparse/zero, likely the *full* tensor contains zeros where it shouldn't. This points to an error in the linear system solver or variable enumeration in `INTERSECTION_NUMBERS.md`.
    *   *Verify*: Are variables pruned too aggressively?
    *   *Verify*: Is the GLSM matrix correct (including the origin column)?
