# Divisor Basis Selection

We need a linearly independent basis of divisors $D_1, \dots, D_{h^{1,1}}$ to express the Kähler form $J = \sum t^a D_a$ (Demirtas et al. 2022, Sec. 3.1).

### Algorithm
1.  **Input**: Set of prime toric divisors (points on the boundary of the polytope).
2.  **Independence Check**:
    *   Use the GLSM charge matrix $Q$.
    *   Columns of $Q$ correspond to relations.
    *   We want to pick a subset of columns of indices $I$ such that the remaining columns can be expressed as integer linear combinations of $I$ modulo the relations.
3.  **Procedure**:
    *   Often involves computing the Smith Normal Form (SNF) of the charge matrix or points matrix.
    *   Select indices that form a basis for the free part of the group of divisors modulo linear equivalence.
