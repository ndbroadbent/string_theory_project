# CYTools Algorithm Specifications (Clean Room)

This index lists the high-level mathematical and algorithmic descriptions of the core functionality required for Calabi-Yau geometry computations. These descriptions are derived from general mathematical principles and public literature (toric geometry, mirror symmetry, HKTY procedure) to serve as a specification for a clean-room implementation.

## Core Algorithms

### Geometry & Topology
- [[project_docs/clean_room/INTERSECTION_NUMBERS.md|Intersection Number Computation (\kappa_{ijk})]]
- [[project_docs/clean_room/GLSM_CHARGE_MATRIX.md|GLSM Charge Matrix ($Q$)]]
- [[project_docs/clean_room/TRIANGULATION.md|Triangulation (FRST)]]
- [[project_docs/clean_room/DEFAULT_HEIGHTS.md|Default Triangulation Heights]]
- [[project_docs/clean_room/DUAL_POLYTOPE.md|Dual Polytope Computation]]

### Invariants & Moduli
- [[project_docs/clean_room/GV_INVARIANTS.md|GV Invariant Computation (HKTY Procedure)]]
- [[project_docs/clean_room/KAHLER_CONE.md|Kähler Cone / Secondary Cone]]
- [[project_docs/clean_room/DIVISOR_BASIS.md|Divisor Basis Selection]]

## References
All algorithms are cross-referenced with the CYTools paper:
- **Demirtas et al. 2022**: *CYTools: A Software Package for Analyzing Calabi-Yau Manifolds* ([[research/papers/cytools_paper_2211.03823.pdf|PDF]])