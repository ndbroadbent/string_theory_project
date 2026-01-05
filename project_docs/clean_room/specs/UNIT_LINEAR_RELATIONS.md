# Unit Spec: Linear Relations Matrix

**Goal**: Verify the construction of the GLSM linear relations matrix used for intersection numbers.

## Inputs
- **Points**: Integer lattice points $P = \{p_1, \dots, p_N\}$ (excluding origin).
- **GLSM Charge Matrix**: $Q$ (from `glsm_charge_matrix`).

## Logic
1.  **Exclude Origin**: The origin (index 0) must be removed.
2.  **Constraint Row**: The "homogeneity" constraint (row of 1s in $Q$) must be removed.
3.  **Result**: A matrix $L$ where $L_{ri} = Q_{ri}$ (for remaining rows $r$ and columns $i$).

## Test Case (4-214-647 Dual)
- **Input**: 12 points. Origin is index 0.
- **GLSM**: 4 rows, 9 columns (columns 0-8).
    - Row 0: [-6, 2, 3, -1, 1, 1, 0, 0, 0]
    - Row 1: [-6, 2, 3, 1, -1, 0, 1, 0, 0]
    - Row 2: [-12, 4, 6, 0, 1, 0, 0, 1, 0]
    - Row 3: [-6, 2, 3, 0, 0, 0, 0, 0, 1]
- **Expected Output**:
    - Remove column 0 (value -6, -6, -12, -6).
    - Remove "homogeneity" row? (Wait, the GLSM rows sum to 0, they are charge conservation. Is there an *extra* row of 1s?)
    - CYTools `linear_relations` usually has a row of 1s prepended. If so, remove it.
    - If the input GLSM is just the charge matrix (rows sum to 0), then we use it as is (minus origin column).

## Verification
- Assert `L.cols` == `num_points - 1`.
- Assert `L` does not contain the origin column.
