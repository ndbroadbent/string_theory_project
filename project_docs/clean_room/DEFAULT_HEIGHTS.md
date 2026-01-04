# Default Triangulation Heights

When no specific triangulation is requested, CYTools produces a "canonical" Fine Regular Star Triangulation (FRST) using a deterministic height function (Demirtas et al. 2022, Sec. 3.2).

### Algorithm
1.  **Initial Heights**: Assign the squared Euclidean norm (Delaunay heights) to each point $p$:
    $$ h(p) = |p|^2 = p \cdot p $$
2.  **Regular Triangulation**: Compute the regular triangulation induced by these heights (projection of the lower convex hull of lifted points).
3.  **Star Property Check**: Verify if the origin is a vertex of every simplex in the resulting triangulation.
4.  **Star Adjustment (if needed)**:
    If the origin is not in every simplex (i.e., not Star), decrease the height of the origin significantly to force it to be "lower" than all other points in the lifted space.
    $$ h(0) \leftarrow h(0) - (\max(h) - \min(h) + 10) $$
    Repeat the triangulation and check until the Star property is satisfied.
