# Convex Hull Facet Enumeration (d-Dimensions)

Clean-room specification for computing the facets of a convex hull in arbitrary dimensions $d$ (specifically $d=4$ or $5$ for Calabi-Yau threefolds).

## 1. Problem Statement
**Input**: A set of $n$ points $S = \{p_1, \dots, p_n\} \subset \mathbb{Z}^d$.
**Output**: A list of facets, where each facet is defined by:
*   $d$ vertices (indices into $S$).
*   An outward normal vector $n$ and constant $c$ such that $n \cdot x \le c$ for all $x \in S$, and $n \cdot v = c$ for vertices $v$ on the facet.

## 2. Algorithm: Incremental Construction (Beneath-Beyond)
While "Gift Wrapping" is $O(F \cdot n)$, the "Beneath-Beyond" or randomized incremental algorithm is often preferred for general dimension $d$ (used by `qhull` and often `CGAL`).

### 2.1 Initialization
1.  Select $d+1$ affinely independent points to form an initial simplex (polytope with $d+1$ vertices and $d+1$ facets).
2.  Compute the hyperplane equation for each facet.
3.  Ensure normals point outward (orient so that the remaining centroid is on the negative side).

### 2.2 Incremental Step
For each remaining point $p_{new}$:
1.  **Visibility Check**: Identify which existing facets are "visible" to $p_{new}$.
    *   A facet $F$ defined by $(n, c)$ is visible if $n \cdot p_{new} > c$.
2.  **Horizon Identification**: Find the "horizon" ridges.
    *   A ridge (codimension-2 face) is on the horizon if it is shared by exactly one visible facet and one invisible facet.
3.  **Update Hull**:
    *   Remove all visible facets.
    *   For each horizon ridge, construct a new facet connecting the ridge to $p_{new}$.
    *   Compute the normal for the new facet.

### 2.3 Degeneracy Handling
*   **Coplanar Points**: If $n \cdot p_{new} = c$ (within tolerance or exact), the point lies on the plane of the facet. It can be merged into the facet or ignored if interior.
*   **Precision**: Use exact integer arithmetic for the visibility check ($n \cdot p - c > 0$) to avoid topology errors.

## 3. Algorithm: Gift Wrapping (Chandrjit & Kapur)
Alternative, strictly output-sensitive.

1.  **Initial Facet**: Find a point with min coordinate (vertex). Find a supporting hyperplane. Pivot to find the first facet.
2.  **Queue**: Maintain a queue of "open" ridges (ridges of found facets that haven't been processed).
3.  **Pivot**:
    *   Pop a ridge $R$.
    *   Iterate over all points $p$ to find the one that forms the "most convex" new facet with $R$.
    *   This minimizes the angle with the previous facet.
4.  **Repeat** until queue is empty.

## 4. Implementation Requirements
*   **Ridge Tracking**: A hash map `Map<Ridge, Facet>` to identify shared ridges.
*   **Exact Arithmetic**: Use `malachite` or `rug` for determinants to ensure the "most convex" choice is correct.
