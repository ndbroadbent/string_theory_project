# Cyrus Project

This repository is the home of **Cyrus**, a high-performance Rust toolkit for Calabi-Yau manifold computations.

## Architecture
- **Crates**:
  - `cyrus-core`: Fundamental mathematics (polytopes, intersection numbers, volumes).
  - `cyrus-moduli`: Moduli stabilization algorithms (KKLT, LVS).
  - `cyrus-cosmology`: Cosmological evolution (quintessence, Friedmann equations).
  - `cyrus-ga`: Genetic algorithms for landscape search.

## Development Workflow
- **Build**: `cargo build`
- **Test**: `cargo test`
- **Lint**: `cargo clippy` and `cargo fmt`
- **Formal Verification**: See `docs/FORMAL_VERIFICATION.md` (in project repo).

## Key Files
- `crates/cyrus-core/src/lib.rs`: Entry point for core logic.
- `crates/cyrus-core/src/intersection.rs`: Intersection tensor logic (verification target).
- `crates/cyrus-core/src/divisor.rs`: Divisor volume logic (verification target).

## Project Management
- **Docs**: `project/project_docs/` (symlinked)
- **Tasks**: `project/todo/cyrus_tasks.md` (symlinked)
- **Research**: `project/research/` (symlinked)

## Commands
- `cargo run --bin cyrus-validate -- mcallister`: Run validation against published results.
