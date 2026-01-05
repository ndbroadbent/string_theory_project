# Feedback: Rust Integer Overflow and Infinite Precision Mandate

**Date**: 2026-01-01
**Source**: User chat (referencing `integer_kernel` implementation)
**Status**: **TRIAGED**

**Triaged to:**
- `research/NUMERIC_PRECISION.md`: Added specific warning about Rust's `i64` overflow behavior and the `malachite::Integer` requirement.
- `project_docs/PROJECT_PHILOSOPHY.md`: Reinforced the "Extreme Engineering Standards" for numeric safety.

## Feedback
- **Rust `i64` Risk**: 
    1. Debug builds panic on overflow.
    2. Release builds **silently wrap**, leading to catastrophic geometric errors without warning.
- **Problem**: Intermediate values in algorithms like Gaussian elimination or Hermite Normal Form (HNF) grow exponentially and easily exceed $2^{63}-1$, especially for large matrices ($h^{1,1}=214$).
- **Solution**: Use `malachite::Integer` for all integer matrix operations to ensure infinite precision and mathematical exactness.

## Action Items
- [x] Update documentation with Rust-specific overflow warnings.
- [ ] Ensure all `cyrus-core` integer math primitives use `malachite::Integer`.
