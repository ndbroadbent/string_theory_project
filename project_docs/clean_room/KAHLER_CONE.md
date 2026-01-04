# Kähler Cone / Secondary Cone

The Kähler cone of the Calabi-Yau $X$ is the dual of the Mori cone (cone of effective curves). In the context of GLSM/Toric geometry, it is identified with the phase of the Secondary Fan containing the triangulation (Demirtas et al. 2022, Sec. 5.4.1).

### Algorithm
1.  **Secondary Cone Definition**:
    The region in height space $\mathbb{R}^{|S|}$ where the induced triangulation remains unchanged.
    Defined by hyperplanes corresponding to "flips" or "walls" between adjacent triangulations (Demirtas et al. 2022, Sec. 5.4.1).

2.  **Wall Computation (BKK Algorithm / Native)**:
    *   Iterate over all pairs of adjacent simplices $(s_1, s_2)$ in the triangulation (sharing a facet).
    *   Form the set $U = s_1 \cup s_2$.
    *   Compute the linear dependence among points in $U$:
        $$ \sum_{p \in U} c_p p = 0 \quad (\text{with } \sum c_p = 0 \text{ for affine}) $$
        This relation vector $c$ is the normal to the hyperplane in height space.
        $$ \sum_{p \in U} c_p h_p \ge 0 $$
    *   Collect all such inequality vectors.

3.  **Kähler Cone**:
    *   The Secondary Cone is in height space.
    *   The Kähler cone parameters $t$ are related to heights (roughly dual/linear transform).
    *   For practical purposes in CYTools, the **Mori Cone** is computed first, then dualized (Demirtas et al. 2022, Sec. 5.4.2).

4.  **Mori Cone via Intersection Numbers**:
    *   Alternatively, the Mori cone generators (curves) can be found by intersecting divisors.
    *   Use the Wall criterion: The generators of the Mori cone are the curves $C = D_i \cdot D_j$ that correspond to the 1D cones in the fan (edges of the triangulation) which are "minimal" generators.
