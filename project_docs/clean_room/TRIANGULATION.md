# Triangulation (FRST)

A Fine, Regular, Star Triangulation (FRST) of a reflexive polytope defines a smooth Calabi-Yau hypersurface (Demirtas et al. 2022, Sec. 3.2).

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
