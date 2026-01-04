# Dual Polytope Computation

The dual (polar) polytope $\Delta^\circ$ of a reflexive polytope $\Delta$ is defined by the set of inequalities derived from the vertices of $\Delta$.

### Algorithm
1.  **Input**: Lattice points of the primal polytope $P$.
2.  **Convex Hull**: Compute the H-representation (inequalities) of the convex hull of $P$.
    The inequalities are of the form $m \cdot x + c \ge 0$.
3.  **Normalization**: For a reflexive polytope, the constant term $c$ can always be normalized to 1 (Demirtas et al. 2022, Sec. 3.1).
    $$ m \cdot x \ge -1 $$
4.  **Dual Vertices**: The vectors $m$ from the normalized inequalities form the vertices of the dual polytope $P^*$.
