# Hand-off: Cyrus Verification Pipeline (Phase 1)

**Date**: 2026-01-01
**To**: Coding Agent (Claude)
**From**: Knowledge Agent (Gemini)

## 1. Context
We are building a **Clean Room** implementation of the McAllister (arXiv:2107.09064) physics pipeline in Rust (`cyrus` crate).
We need to prove that our Rust code produces the exact same cosmological constant ($V_0 \approx -10^{-203}$) as the reference paper.

## 2. Reading List (Read in Order)
1.  `prds/CYRUS_VERIFICATION_PIPELINE.md`: The high-level strategy (Fixtures -> Racetrack -> KKLT).
2.  `project_docs/FORMULAS.md`: The exact physics formulas to implement.
3.  `todo/cyrus/plan_physics_port.md`: The step-by-step implementation plan.
4.  `todo/cyrus/plan_intersection_computation.md`: (For reference on Phase 2, lower priority for now).

## 3. Directives & Constraints
- **Clean Room Protocol**: You are **FORBIDDEN** from reading the `cytools` source code directly. Use the formulas in `project_docs/FORMULAS.md`. If a formula is missing, ask the Knowledge Agent to extract it.
- **License**: The target code (`cyrus`) is MIT/Apache 2.0.
- **Fixtures**: Use `serde_json` to load test data. Do not hardcode magic numbers in tests.

## 4. Immediate Tasks
Start with **Phase 1: Verification Pipeline**.

1.  **Fixture Tooling**: Write a Python script to dump the McAllister data from `cytools` into JSON.
    - *Reference*: `prds/CYRUS_VERIFICATION_PIPELINE.md` (Test Fixture Structure).
2.  **Racetrack Module**: Implement `cyrus-core/src/racetrack.rs`.
    - *Input*: `gv_invariants.json` (N_q), `flux.json` (W_0).
    - *Goal*: Minimize $V_{scalar}$ to find $g_s$.

## 5. Starting Command
```bash
# Verify you can build the current state
cd reference/cyrus
cargo test
```
