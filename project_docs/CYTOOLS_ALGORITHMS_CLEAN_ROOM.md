# Clean Room Implementation Specifications

This document provides high-level mathematical and algorithmic descriptions of the core functionality required for Calabi-Yau geometry computations. These descriptions are derived from general mathematical principles and public literature (toric geometry, mirror symmetry, HKTY procedure) to serve as a specification for a clean-room implementation.

## 1. Intersection Number Computation (\kappa_{ijk})

The intersection numbers of a Calabi-Yau hypersurface $X$ in a toric variety $V$ are topological invariants defined by the triple intersection of divisors.

### Mathematical Definition
For a basis of divisors {D_a}, the intersection numbers are:
$$ \kappa_{abc} = \int_X D_a \wedge D_b \wedge D_c $$
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
The divisors satisfy linear equivalence relations given by the GLSM charge matrix $Q$:
    $$ \sum_{i} Q_i^a D_i \sim 0 \quad \text{for each } a = 1, \dots, h^{1,1} $$
    where indices $i$ run over all rays/points.

4.  **Constructing the Linear System**:
    We want to find all intersection numbers, including self-intersections (e.g., $D_1^3$).
    We can generate a system of linear equations $M x = C$:
    *   **Variables ($x$)**: The unknown intersection numbers.
    *   **Relations**: Multiply the linear relation $\sum Q_i^a D_i = 0$ by any product of $n-1$ divisors $P = D_{j_1} \dots D_{j_{n-1}}$:
        $$ \sum_i Q_i^a (D_i \cdot P) = 0 $$
        This gives a linear equation relating different intersection numbers.
    *   **System Construction**:
        Iterate over all possible combinations of $n-1$ divisors to form the "probes" $P$.
        Use the "Distinct Intersection" rule (Step 2) to fill in the known values (constant term $C$).
        The remaining terms are the unknowns ($x$).

5.  **Solving**:
The system is typically overdetermined. It can be solved using least squares or sparse linear algebra (e.g., Cholesky decomposition if formulated as $M^T M x = M^T C$).
    For exact arithmetic, use a rational number solver.

## 2. GLSM Charge Matrix ($Q$)

The GLSM charge matrix describes the linear relations among the toric divisors.

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

## 3. GV Invariant Computation (HKTY Procedure)

Gopakumar-Vafa (GV) invariants $n_q$ count BPS states (curves) of degree $q$. They are computed from the A-model topological string partition function, often via Mirror Symmetry.

### Algorithm (HKTY via Mirror Symmetry)
1.  **Mirror Map**:
    *   Compute the periods $\varpi_k(z)$ of the mirror manifold near the Large Complex Structure (LCS) point.
    *   Identify the fundamental period $\varpi_0(z)$ and the single-logarithmic periods $\varpi_a(z)$.
    *   Define mirror coordinates $t^a(z) = \varpi_a(z) / \varpi_0(z)$.
    *   Invert this map to find $z(q)$, where $q_a = \exp(2\pi i t^a)$.

2.  **Prepotential and Yukawa Couplings**:
    *   Compute the Yukawa couplings on the mirror side (dependence on $z$).
    *   Transform to $t$-coordinates using the Jacobian of the mirror map:
        $$ \mathcal{K}_{abc}(q) = \int_X \Omega \wedge \partial_a \partial_b \partial_c \Omega $$
    *   This gives the A-model Yukawa couplings:
        $$ \kappa_{abc} + \sum_{q} n_q d_a d_b d_c \frac{q^d}{1-q^d} $$
        (structure simplified for exposition; exact formula involves Lambert series).

3.  **Extraction**:
    *   Expand the computed Yukawa couplings as a power series in $q$.
    *   Subtract the classical intersection numbers $\kappa_{abc}$.
    *   Iteratively solve for the integer invariants $n_q$ (GV invariants) using the multicover formula:
        $$ F_{\text{inst}}(t) = \sum_{q \in H_2(X,\mathbb{Z}) \setminus \{0\}} n_q \sum_{k=1}^\infty \frac{1}{k^3} q^{k} $$
        (or equivalent relation for Yukawa couplings).

## 4. Triangulation (FRST)

A Fine, Regular, Star Triangulation (FRST) of a reflexive polytope defines a smooth Calabi-Yau hypersurface.

### Definitions
*   **Fine**: Uses all relevant lattice points (all points not interior to facets, or all points in the polytope). No lattice points lie in the interior of simplices.
*   **Star**: The origin is a vertex of every simplex. (Implies the fan is defined over the faces of the reflexive polytope).
*   **Regular**: The triangulation comes from the projection of the lower convex hull of a "lifted" polytope.
    *   Assign a height $h_i$ to each point $v_i$.
    *   Lift points to $(v_i, h_i) \in \mathbb{R}^{d+1}$.
    *   Compute the convex hull.
    *   Project the lower faces back to $\mathbb{R}^d$.

### Algorithm
1.  **Input**: Lattice points $S$.
2.  **Height Assignment**:
    *   Choose a vector of heights $H = \{h_p \mid p \in S\}$.
    *   For **FRST**, $h_{\text{origin}}$ should be very low (e.g., $-\infty$ or sufficiently large negative) to ensure Star property.
    *   Random heights often work generic regular triangulations.
3.  **Convex Hull**:
    *   Compute Convex Hull of $\{(p, h_p)\}$.
    *   Extract lower faces (normals have negative last component).
4.  **Validation**:
    *   Check if all points in $S$ are vertices (Fine).
    *   Check if origin is in every simplex (Star).

## 5. Kähler Cone / Secondary Cone

The Kähler cone of the Calabi-Yau $X$ is the dual of the Mori cone (cone of effective curves). In the context of GLSM/Toric geometry, it is identified with the phase of the Secondary Fan containing the triangulation.

### Algorithm
1.  **Secondary Cone Definition**:
The region in height space $\mathbb{R}^{|S|}$ where the induced triangulation remains unchanged.
    Defined by hyperplanes corresponding to "flips" or "walls" between adjacent triangulations.

2.  **Wall Computation (BKK Algorithm / Native)**:
    *   Iterate over all pairs of adjacent simplices $(s_1, s_2)$ in the triangulation (sharing a facet).
    *   Form the set $U = s_1 \cup s_2$.
    *   Compute the linear dependence among points in $U$:
        $$ \sum_{p \in U} c_p p = 0 \quad (\text{with } \sum c_p = 0 \text{ for affine}) $$
        This relation vector $c$ is the normal to the hyperplane in height space.
        $$ \sum_{p \in U} c_p h_p \ge 0 $$
    *   Collect all such inequality vectors.

3.  **Kähler Cone**:
    *   The Secondary Cone is in height space.
    *   The Kähler cone parameters $t$ are related to heights (roughly dual/linear transform).
    *   For practical purposes in CYTools, the **Mori Cone** is computed first, then dualized.

4.  **Mori Cone via Intersection Numbers**:
    *   Alternatively, the Mori cone generators (curves) can be found by intersecting divisors.
    *   Use the Wall criterion: The generators of the Mori cone are the curves $C = D_i \cdot D_j$ that correspond to the 1D cones in the fan (edges of the triangulation) which are "minimal" generators.

## 6. Divisor Basis Selection

We need a linearly independent basis of divisors $D_1, \dots, D_{h^{1,1}}$ to express the Kähler form $J = \sum t^a D_a$.

### Algorithm
1.  **Input**: Set of prime toric divisors (points on the boundary of the polytope).
2.  **Independence Check**:
    *   Use the GLSM charge matrix $Q$.
    *   Columns of $Q$ correspond to relations.
    *   We want to pick a subset of columns of indices $I$ such that the remaining columns can be expressed as integer linear combinations of $I$ modulo the relations.
3.  **Procedure**:
    *   Often involves computing the Smith Normal Form (SNF) of the charge matrix or points matrix.
    *   Select indices that form a basis for the free part of the group of divisors modulo linear equivalence.
