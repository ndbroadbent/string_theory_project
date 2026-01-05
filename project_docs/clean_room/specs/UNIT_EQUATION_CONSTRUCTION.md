# Unit Spec: Equation Construction

**Goal**: Verify the linear equations generated from GLSM relations.

## Logic
1.  **Iterate Probes**: All sorted 3-tuples {j, k, l} from the variable/known set.
2.  **Iterate GLSM Rows**: For each row R of the linear relations matrix L.
3.  **Equation**:
    $$ \sum_{i \in \text{Points} \setminus \{0\}} L_{ri} \cdot \kappa_{\{i, j, k, l\}} = 0 $$
4.  **Partition**:
    - Terms where {i, j, k, l} is distinct → Move to RHS (Known).
    - Terms where {i, j, k, l} has repeats → Keep on LHS (Variable).

## Test Case (4-214-647 Probe {3,4,5})
- **Probe**: {3, 4, 5}
- **GLSM Row 3**: `[-6, 2, 3, 0, 0, 0, 0, 0, 1]` (Full) -> `[2, 3, 0, 0, 0, 0, 0, 1]` (No Origin, indices 1..8)
    - Coefficients: Q_1=2, Q_2=3, Q_3=0, Q_4=0, Q_5=0, Q_6=0, Q_7=0, Q_8=1.
- **Equation**:
    $$ 2 \kappa_{1345} + 3 \kappa_{2345} + 0 \kappa_{3345} + 0 \kappa_{3445} + 0 \kappa_{3455} + 1 \kappa_{3458} = 0 $$
- **Values**:
    - \kappa_{1345} = 1/3 (Known)
    - \kappa_{2345} = 1/2 (Known)
    - \kappa_{3458} = 0 (Not in any simplex? Verify.)
- **Result**:
    $$ 2(1/3) + 3(1/2) + 0 = 0 \implies 2.166... = 0 $$
- **Inconsistency**: This equation is `2.17 = 0`.
    - **Conclusion**: The Least Squares solver must handle this. It will find values for *other* variables in the system such that the *total* error is minimized, effectively "ignoring" this impossible constraint or balancing it against others.

## Verification
- Assert that the equation is constructed exactly as above.
- Assert that the solver returns a finite residual.
