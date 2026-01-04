# GV Invariant Computation (HKTY Procedure)

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
