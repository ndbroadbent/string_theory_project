# String Theory Search Project

This repository hosts the **Meta-Genetic Algorithm** for exploring the string theory landscape.

## Architecture
- **Language**: Rust (binary) + Python (PyO3 bridge to CYTools/cymyc).
- **Core Logic**:
  - `src/main.rs`: Entry point.
  - `src/searcher.rs`: Genetic algorithm implementation.
  - `src/physics.rs`: Bridge to Python physics libraries.
  - `src/meta_ga.rs`: Meta-evolution logic.

## Development Workflow
- **Build**: `PYO3_PYTHON=... cargo build --release`
- **Run**: `VIRTUAL_ENV=... ./target/release/search`
- **Test**: `uv run pytest` (Python) and `cargo test` (Rust)

## Key Files
- `config.toml`: Local configuration.
- `FORMULAS.md`: Definitive physics formula reference.
- `physics_bridge.py`: Python-side implementations of CYTools/cymyc calls.

## Project Management
- **Docs**: `project/project_docs/` (symlinked)
- **Tasks**: `project/todo/string_theory_tasks.md` (symlinked)
- **Research**: `project/research/` (symlinked)

## Critical Constraints
- **Correctness**: "Physics code bugs produce plausible-looking wrong answers."
- **No Shortcuts**: Do not use precomputed databases or approximations.
- **Verification**: All results must be reproducible against McAllister et al. (2021).
