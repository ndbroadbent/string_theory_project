# Geometric Primitives & Robust Predicates

Clean-room specification for the fundamental geometric operations required by convex hull and triangulation algorithms.

## 1. Orientation Predicate
Does a point $p$ lie above, below, or on a hyperplane defined by points $v_1, \dots, v_d$? 

*   **Input**: $d+1$ points $v_1, \dots, v_d, p$ in $\mathbb{R}^d$.
*   **Computation**:
    $$ \text{Orient}(v_1, \dots, v_d, p) = \text{sign}(\det(\Lambda)) $$ 
    where $\Lambda$ is the $(d+1) \times (d+1)$ matrix:
    $$ \Lambda = \begin{pmatrix} 1 & v_{1,1} & \dots & v_{1,d} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & v_{d,1} & \dots & v_{d,d} \\ 1 & p_1 & \dots & p_d \end{pmatrix} $$ 
*   **Precision**: MUST be computed exactly (Integers or Rationals).

## 2. Hyperplane Construction
Given $d$ points $v_1, \dots, v_d$, find the normal $n$ and constant $c$ such that $n \cdot x = c$.

*   **Normal**: Generalized cross product.
    $$ n_i = (-1)^{i+1} \det(M_i) $$ 
    where $M_i$ is the $d \times d$ matrix of the vectors $(v_2-v_1), \dots, (v_d-v_1)$ with the $i$-th column removed.
    *   *Alternative*: Cofactors of the orientation matrix.
*   **Constant**: $c = n \cdot v_1$.

## 3. Point-in-Simplex
Does point $p$ lie inside simplex $S = \{v_0, \dots, v_d\}$?

*   Check $\text{Orient}(v_0, \dots, \hat{v}_i, \dots, v_d, p)$ for each face $i$ (removing vertex $i$).
*   If all signs match the orientation of the simplex itself, $p$ is inside.

## 4. Point-in-Polytope (Convex)
Given a convex polytope defined by inequalities $A x \le b$:
*   Check if $A p \le b$ holds for all rows.
*   This is $O(\text{facets})$.
