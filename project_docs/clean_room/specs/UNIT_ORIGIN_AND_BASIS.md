# Unit Spec: Origin Handling and Basis Transformation

**Goal**: Verify the post-processing steps to recover origin intersections and transform to basis.

## 1. Origin Recovery
- **Input**: Computed $\kappa_{ijk}$ for $i,j,k \ne 0$.
- **Formula**:
    $$ \kappa_{0jk} = - \sum_{i \ne 0} \kappa_{ijk} $$
    $$ \kappa_{00k} = - \sum_{i \ne 0} \kappa_{i0k} $$
    $$ \kappa_{000} = - \sum_{i \ne 0} \kappa_{i00} $$

## 2. Basis Transformation
- **Input**: Full tensor $\kappa$.
- **Basis**: Indices $B = [3, 4, 5, 8]$.
- **Method**: Subtensor extraction.
    $$ \kappa^{\text{basis}}_{abc} = \kappa_{B[a], B[b], B[c]} $$

## Test Case (4-214-647)
- **Target**: $\kappa_{345} = 1$ (in full tensor).
- **Check**: Does the least-squares solution for the full tensor yield $\kappa_{345} \approx 1$?
- **Check**: Does `filter_tensor_indices` correctly extract it?

## Verification
- Implement the recursive sum.
- Implement the subtensor extraction.
