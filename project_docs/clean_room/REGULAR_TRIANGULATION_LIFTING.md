# Regular Triangulation (Lifting Method)

Clean-room specification for computing a Regular Triangulation (Weighted Delaunay Triangulation) via the lifting map.

## 1. Concept
A regular triangulation of points $S \subset \mathbb{R}^d$ with weights (heights) $h$ is equivalent to the projection of the **lower convex hull** of the lifted points in $\mathbb{R}^{d+1}$.

## 2. Algorithm
1.  **Input**:
    *   Points $p_1, \dots, p_n \in \mathbb{Z}^d$.
    *   Heights $h_1, \dots, h_n \in \mathbb{R}$ (or $\mathbb{Z}$).
2.  **Lifting**:
    *   Construct lifted points $\hat{p}_i = (p_i, h_i) \in \mathbb{R}^{d+1}$.
3.  **Convex Hull**:
    *   Compute the convex hull of {\`\hat{p}_i\`} in $d+1$ dimensions.
    *   Use the algorithm from [[project_docs/clean_room/CONVEX_HULL_D.md|CONVEX_HULL_D.md]].
4.  **Lower Hull Identification**:
    *   Iterate over facets of the $(d+1)$-hull.
    *   A facet with normal $n = (n_1, \dots, n_d, n_{d+1})$ is on the **lower hull** if $n_{d+1} < 0$ (assuming normals point outwards).
        *   *Note*: Verify the sign convention based on whether "outward" means away from the bulk. If the bulk is "above", outward is down. Standard convention: outward normals point away from the polytope interior. For "lower" hull (visible from $-\infty$), the outward normal has a negative last component.
5.  **Projection**:
    *   The vertices of the lower facets, projected back to $\mathbb{R}^d$ (dropping the last coordinate), form the simplices of the triangulation.

## 3. Star Property Check
1.  Identify the index of the origin $O$.
2.  Iterate over all simplices $S$.
3.  Check if $O \in S$.
4.  If for any simplex $O \notin S$, the triangulation is **not star**.

## 4. Star Adjustment
See [[project_docs/clean_room/DEFAULT_HEIGHTS.md|Default Triangulation Heights]] for the algorithm to force the star property.
