# Computational Geometry Algorithm Specifications

This index lists the clean-room specifications for the fundamental computational geometry algorithms required to implement the Cyrus toolkit (Convex Hulls, Triangulations, Polytope Duality).

## Core Algorithms

### Convex Hulls
- [[project_docs/clean_room/CONVEX_HULL_D.md|Convex Hull Facet Enumeration (d-Dimensions)]]
    - Algorithms: Randomized Incremental (Beneath-Beyond), Gift Wrapping.
    - Output: Facets and normals.
- [[project_docs/clean_room/CONVEX_HULL_VERTICES.md|Convex Hull Vertex Enumeration]]
    - Identification of extreme points.

### Triangulation
- [[project_docs/clean_room/REGULAR_TRIANGULATION_LIFTING.md|Regular Triangulation (Lifting Method)]]
    - The core algorithm for FRST.
- [[project_docs/clean_room/DEFAULT_HEIGHTS.md|Default Triangulation Heights]] (from CYTools spec)

### Polytope Geometry
- [[project_docs/clean_room/REFLEXIVE_POLYTOPE_DUAL.md|Reflexive Polytope Dual Computation]]
    - Normalizing facet equations to find dual vertices.
- [[project_docs/clean_room/DUAL_POLYTOPE.md|Dual Polytope (General Spec)]] (legacy link)

### Primitives
- [[project_docs/clean_room/GEOMETRIC_PRIMITIVES.md|Geometric Primitives & Robust Predicates]]
    - Orientation, Determinants, Hyperplanes.
    - **CRITICAL**: Requires [[research/NUMERIC_PRECISION.md|Exact Arithmetic]].

## Relationships
- **FRST**: Uses `REGULAR_TRIANGULATION_LIFTING` with heights from `DEFAULT_HEIGHTS`, relying on `CONVEX_HULL_D` (in d+1 dims) and `GEOMETRIC_PRIMITIVES` for correctness.
- **Dual**: Uses `CONVEX_HULL_D` to get facets, then `REFLEXIVE_POLYTOPE_DUAL` to normalize them.
