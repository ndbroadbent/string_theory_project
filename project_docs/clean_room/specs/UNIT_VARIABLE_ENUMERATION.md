# Unit Spec: Variable Enumeration

**Goal**: Verify that we enumerate exactly the necessary variables (self-intersections) and no more.

## Logic
1.  **Iterate Simplices**: For each simplex $S$ (origin removed).
2.  **Generate Tuples**:
    - **3-Faces**: For each subset of size 3 from $S$, duplicate one index.
        - e.g., {a, b, c} -> {a, a, b, c}, {a, b, b, c}, {a, b, c, c}.
    - **2-Faces**: For each subset of size 2, duplicate indices.
        - {a, b} -> {a, a, b, b}, {a, a, a, b}, {a, b, b, b}.
    - **1-Faces**: {a} -> {a, a, a, a}.
3.  **Filter**: Ensure sorted, unique, and no origin.

## Verification
- Assert that *distinct* tuples (e.g., {a, b, c, d}) are NOT in the variable list.
- Assert that tuples with origin are NOT in the list.
- Count variables for 4-214-647 (should be around 167).
