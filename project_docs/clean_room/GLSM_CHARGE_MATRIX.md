# GLSM Charge Matrix ($Q$)

The GLSM charge matrix describes the linear relations among the toric divisors (Demirtas et al. 2022, Sec. 3.1, Sec. 5.3).

### Algorithm Description
1.  **Inputs**:
    *   **Points**: The lattice points $v_i \in \mathbb{Z}^d$ defining the polytope (columns of matrix $P$).
    *   **Homogeneity**: Include a row of 1s to enforce the Calabi-Yau condition (sum of charges = 0) if treating as a projective variety. Let $\tilde{P}$ be the augmented matrix.

2.  **Kernel Computation**:
    The charge matrix $Q$ is a basis for the left null space (kernel) of $\tilde{P}$:
    $$ Q \cdot \tilde{P}^T = 0 $$
    Dimension of $Q$: $(N - d - 1) \times N$, where $N$ is the number of points and $d$ is the lattice dimension.

3.  **Integral Basis**:
    To ensure integer charges, compute the Smith Normal Form (SNF) or Hermite Normal Form (HNF) of $\tilde{P}$ or use LLL reduction on the kernel basis to find a primitive integral basis.

