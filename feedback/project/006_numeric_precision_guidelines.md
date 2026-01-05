# Feedback: Numeric Precision Guidelines for Geometry

**Date**: 2026-01-01
**Source**: User chat
**Status**: **TRIAGED**

**Triaged to:**
- `research/NUMERIC_PRECISION.md`: Updated with the "3-Tier" rule.
- `project_docs/PROJECT_PHILOSOPHY.md`: Added "Exactness at Decision Boundaries" mandate.

## Feedback
- **Core Principle**: Use **exact arithmetic** for topological/combinatorial decisions (branching logic), but floats are acceptable for purely numeric post-processing (volumes, reporting).
- **Danger Zone**: Using floats for orientation tests, visibility checks, or degeneracy handling. A wrong sign here flips the geometry, not just the digit.
- **Heights**: The current pipeline using `heights: &[f64]` is dangerous.
- **Recommendation**:
    - Ban `f64` for combinatorial inputs.
    - Represent heights as `i64` (or `BigInt`) or `Rational`.
    - Use **exact integer determinants** (e.g., Bareiss algorithm) for hull/triangulation decisions.

## Action Items
- [ ] Refactor triangulation API to accept integer/rational heights instead of `f64`.
- [ ] Implement or use a library for exact geometric predicates (robust predicates).
- [ ] Update documentation to reflect the "3-Tier" precision strategy.
