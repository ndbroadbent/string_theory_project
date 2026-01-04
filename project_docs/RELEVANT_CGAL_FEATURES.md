# Relevant CGAL Features for String Theory Project

This document outlines the specific features and components of the Computational Geometry Algorithms Library (CGAL) that are relevant to the **String Theory Project** and the **Cyrus** toolkit. This serves as a reference for clean-room implementation and potential Rust porting efforts.

## 1. Core Modules

### 1.1 `Triangulation`
*   **Purpose**: Provides algorithms and data structures for triangulations in arbitrary dimensions.
*   **Key Class**: `Regular_triangulation`
    *   This is the direct analog to the "Regular" part of FRST (Fine, Regular, Star Triangulation).
    *   It handles weighted points (points with "heights").
    *   It generalizes the Delaunay triangulation (where weights are related to squared norms).
*   **Relevance**: Critical for computing the secondary fan and triangulation of the reflexive polytope. The "lifting" method used in FRST is mathematically equivalent to a regular triangulation.

### 1.2 `Convex_hull_d`
*   **Purpose**: Computes convex hulls in arbitrary dimensions ($d$).
*   **Key Functionality**:
    *   Incremental construction of hulls.
    *   Maintenance of the hull as a simplicial complex.
    *   Facet and simplex iterators.
*   **Relevance**:
    *   Computing the dual polytope (polar).
    *   Determining the secondary cone (related to the hull of the secondary fan).
    *   The "lifting" algorithm for triangulation involves computing the lower convex hull of points lifted to $d+1$ dimensions.

### 1.3 `Kernel_d` (and `Kernel_23`)
*   **Purpose**: Defines geometric objects (Points, Vectors, Hyperplanes) and predicates (Orientation, Side-of-sphere).
*   **Key Concept**: **Exact Geometric Predicates**.
    *   CGAL emphasizes robustness against floating-point errors.
    *   Predicates like `orientation(p1, p2, ..., pd)` return exact signs (+1, -1, 0) even with floating-point inputs, using techniques like interval arithmetic and exact expansion fallback.
*   **Relevance**:
    *   **Crucial for correctness**. A single wrong orientation sign can invalidate a triangulation or result in a non-convex "convex" hull.
    *   Any clean-room implementation must either use exact arithmetic (Rational/Integer) or robust predicates.

### 1.4 `Number_types`
*   **Purpose**: Wrapper classes for number types (GMP, MPFR, internal exact types).
*   **Relevance**: Supports the "Exactness at Decision Boundaries" philosophy.

## 2. Mapping to Project Needs

### 2.1 FRST (Fine, Regular, Star Triangulation)
*   **Fine**: Uses all relevant points.
    *   CGAL's `Regular_triangulation` inserts points. If a point is "hidden" (not part of the triangulation), it's tracked. A "Fine" triangulation corresponds to one where no points are hidden (or only irrelevant ones).
*   **Regular**:
    *   CGAL's `Regular_triangulation` *is* this by definition.
    *   It uses "Power cells" and "Weighted points".
*   **Star**:
    *   This is a topological property (origin is connected to all vertices).
    *   In CGAL, this can be checked by verifying if the `Infinite_vertex` (or a specific vertex representing the origin) is incident to all cells, or by post-processing the triangulation graph.

### 2.2 Polytope Duality
*   Can be implemented via `Convex_hull_d`.
*   The facets of the primal polytope (computed by convex hull) define the vertices of the dual.

## 3. Implementation Notes for Rust (Cyrus)

*   **Do not port C++ code directly**. The goal is to implement the *algorithms*, not the code.
*   **Data Structures**:
    *   We need a `SimplicialComplex` or `Triangulation` struct in Rust.
    *   It needs to handle adjacency (neighbors) efficiently.
*   **Algorithms**:
    *   **Incremental Insertion**: A common strategy for Delaunay/Regular triangulations. Insert points one by one and "flip" edges/faces to restore the regular property.
    *   **Bowyer-Watson Algorithm**: A standard algorithm for generating Delaunay triangulations in any dimension.
*   **Robustness**:
    *   Use `malachite` or `rug` for exact arithmetic.
    *   Or implement Robust Predicates (Shewchuk's algorithms) if using `f64`.

## 4. Key Files to Reference (for logic/math)

*   `Triangulation/include/CGAL/Regular_triangulation.h`: Definition of the regular triangulation class and typedefs.
*   `Convex_hull_d/include/CGAL/Convex_hull_d.h`: Interface for d-dimensional convex hulls.
*   `Kernel_d/include/CGAL/Kernel_d/Point_d.h`: How high-dimensional points are represented.
