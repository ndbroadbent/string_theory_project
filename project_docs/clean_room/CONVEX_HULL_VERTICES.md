# Convex Hull Vertex Enumeration

Clean-room specification for identifying the subset of points that are vertices (extreme points) of the convex hull.

## 1. Problem Statement
**Input**: A set of $n$ points $S \subset \mathbb{Z}^d$.
**Output**: A list of indices $I$ such that $S_I$ are the vertices of $\text{Conv}(S)$.

## 2. Naive Algorithm (Linear Programming)
For each point $p \in S$:
1.  Check if $p$ is redundant.
2.  Formulate an LP: Is $p$ a convex combination of $S \setminus \{p\}$?
    *   Maximize $0$ subject to:
        *   $\sum_{j \neq i} \lambda_j p_j = p_i$
        *   $\sum \lambda_j = 1$
        *   $\lambda_j \ge 0$
3.  If no solution, $p$ is a vertex.

## 3. Algorithm via Facet Enumeration
If the full Convex Hull (facets) is already computed:
1.  Initialize a set of vertices $V = \emptyset$.
2.  Iterate over all facets $F$.
3.  Add all vertices of $F$ to $V$.
4.  Result is $V$.

## 4. Pre-filtering (Performance)
Before running expensive hull algorithms:
1.  Compute axis-aligned bounding box (AABB).
2.  Points strictly inside the AABB cannot be vertices (unless the hull *is* the AABB).
3.  **Extreme Points**: Find points with min/max coordinates in each dimension. These are guaranteed vertices.
