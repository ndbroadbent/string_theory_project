# Reflexive Polytope Dual Computation

Clean-room specification for computing the dual of a reflexive polytope.

## 1. Definition
A lattice polytope $\Delta$ containing the origin is **reflexive** if its dual $\Delta^\circ$ is also a lattice polytope.
$$ \Delta^\circ = \{ m \in \mathbb{R}^d \mid m \cdot x \ge -1, \forall x \in \Delta \} $$

## 2. Algorithm
1.  **Input**: Vertices $V$ of the primal polytope $\Delta$.
2.  **Convex Hull**: Compute the facet inequalities of $\Delta$.
    *   Form: $n_i \cdot x \ge -c_i$ (normalized so $c_i > 0$ if origin is interior).
3.  **Reflexive Normalization**:
    *   For a reflexive polytope, we can always normalize such that the RHS is exactly $-1$.
    *   Inequality becomes: $m_i \cdot x \ge -1$.
    *   If the computed form is $n \cdot x \ge -c$, then $m = n/c$.
4.  **Integrality Check**:
    *   If $\Delta$ is reflexive, every $m_i$ must be an integer vector.
    *   If any $m_i$ is not integral, $\Delta$ is not reflexive.
5.  **Output**: The set of vectors $\{m_i\}$ are the vertices of $\Delta^\circ$.

## 3. Implementation Note
*   If using the **Hyperplane Construction** from geometric primitives, you get $n \cdot x = c$.
*   Since origin is strictly interior, $c \neq 0$.
*   Divide by $-c$: $-\frac{n}{c} \cdot x = -1$.
*   The dual vertex is $-\frac{n}{c}$.
