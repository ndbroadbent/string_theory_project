# Unit Spec: Known Intersection Numbers

**Goal**: Verify the computation of intersection numbers for distinct indices on the ambient variety.

## Inputs
- **Simplices**: List of simplices from the triangulation. Each simplex has $d+1$ vertices.
- **Points**: Homogenized points (last coord 1).

## Logic
1.  **Iterate Simplices**: For each simplex $S = \{v_0, \dots, v_d\}$.
2.  **Filter Origin**: If origin (index 0) is in $S$, remove it. The remaining $d$ vertices define a cone in the fan.
3.  **Determinant**: Compute $\det(v_1, \dots, v_d)$.
4.  **Value**: $\kappa_{v_1 \dots v_d} = 1 / |\det|$.
    - **Note**: This value is fractional if the variety is singular.

## Test Case (4-214-647 Dual)
- **Simplex**: `[0, 1, 3, 4, 5]`
- **Rays**: `[1, 3, 4, 5]` (Origin 0 removed)
- **Points**:
    - 1: `[-1, 2, -1, -1]`
    - 3: `[-1, -1, 1, 1]`
    - 4: `[-1, -1, 1, 2]`
    - 5: `[-1, -1, 2, 1]`
- **Determinant**: 3.
- **Expected**: $\kappa_{1345} = 1/3 \approx 0.3333$.

## Verification
- Assert `known_map` contains key `(1,3,4,5)` (sorted).
- Assert value is `1.0/3.0` (within float epsilon).
