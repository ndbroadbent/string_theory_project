# Intersection Number Computation (\kappa_{ijk})

The intersection numbers of a Calabi-Yau hypersurface $X$ in a toric variety $V$ are topological invariants defined by the triple intersection of divisors.

### Mathematical Definition
For a basis of divisors {D_a}, the intersection numbers are (Demirtas et al. 2022, Eq. 3.1):
$$ \kappa_{abc} = \int_X D_a \wedge D_b \wedge D_c = \# D^a \cap D^b \cap D^c $$
In the ambient toric variety $V$, this relates to intersection numbers involving the anti-canonical divisor $-K_V = [X]$:
$$ \kappa_{abc} = \int_V D_a \wedge D_b \wedge D_c \wedge [X] $$

### Algorithm Description
The computation leverages the linear relations among divisors in the toric variety and the known intersection numbers of the triangulation simplices.

1.  **Inputs**:
    *   **Triangulation**: A set of simplices, where each simplex corresponds to a cone in the fan.
    *   **Points**: The lattice points generating the fan rays.
    *   **GLSM Charges**: The linear relations among the divisors (generators of the fan rays).

2.  **Known Intersections (Distinct Indices)**:
    For a simplical toric variety, the intersection of $n$ distinct divisors $D_{i_1}, \dots, D_{i_n}$ (where $n = \dim(V)$) is non-zero if and only if the corresponding rays generate a cone in the fan (i.e., form a simplex in the triangulation).
    The value is:
    $$ D_{i_1} \cdot \dots \cdot D_{i_n} = \frac{1}{|\det(v_{i_1}, \dots, v_{i_n})|} $$
    where $v_i$ are the primitive lattice vectors of the rays. If the variety is smooth, this determinant is 1.

3.  **Linear Relations**:
    The divisors satisfy linear equivalence relations given by the GLSM charge matrix $Q$ (Demirtas et al. 2022, Sec. 3.1):
    $$ \sum_{i} Q_i^a D_i \sim 0 \quad \text{for each } a = 1, \dots, h^{1,1} $$
    where indices $i$ run over all rays/points.

4.  **Constructing the Linear System**:
    We want to find all intersection numbers, including self-intersections (e.g., $D_1^3$).
    We can generate a system of linear equations $M x = C$:
    *   **Variables ($x$)**: The unknown intersection numbers.
        *   **Optimization (Variable Pruning)**: Do NOT enumerate all possible tuples. Only enumerate intersection numbers corresponding to:
            1.  Faces of simplices in the triangulation (dimension $\ge 2$).
            2.  Self-intersections required for consistency.
            Most intersection numbers are trivially zero if the divisors do not share a cone in the fan.
    *   **Relations**: Multiply the linear relation $\sum Q_i^a D_i = 0$ by any product of $n-1$ divisors $P = D_{j_1} \dots D_{j_{n-1}}$:
        $$ \sum_i Q_i^a (D_i \cdot P) = 0 $$
        This gives a linear equation relating different intersection numbers.
    *   **System Construction**:
        Iterate over all possible combinations of $n-1$ divisors (from the pruned set) to form the "probes" $P$.
        Use the "Distinct Intersection" rule (Step 2) to fill in the known values (constant term $C$).
        The remaining terms are the unknowns ($x$).
        **CRITICAL**: The matrix $M$ is extremely sparse. It must be constructed using a sparse format (e.g., CSR).

5.  **Solving**:
    The system is typically overdetermined ($M x = -C$).
    *   **Method**: Solve the normal equations $M^T M x = M^T (-C)$.
    *   **Algorithm**: Use a sparse linear solver. Cholesky decomposition of $M^T M$ (which is symmetric positive definite) is the standard high-performance approach.
    *   **Rust Recommendation**: Use the **`faer`** crate (specifically `faer::sparse`). It provides high-performance sparse LU and Cholesky solvers and is already included in the project dependencies.
    *   **Exactness**: For the final result, rational reconstruction can be used, or perform the solve in exact rational arithmetic if the sparse solver supports it (though performance will suffer). CYTools uses float64 with Cholesky for speed, then rounds/reconstructs.
