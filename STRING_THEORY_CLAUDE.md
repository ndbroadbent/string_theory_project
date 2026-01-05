# String Theory Code Repo (Hands)

This repository contains the **Legacy Python Code** and **Data Dependencies** for the String Theory project. 

## Repository Roles (Brain vs. Hands)

| Repository | Role | Content |
|------------|------|---------|
| **string_theory_project** (Brain) | **Knowledge Base** | Documentation, Research Papers, Clean Room Specs, PRDs, Task Tracking. |
| **string_theory** (this repo) | **Legacy Code & Data** | Python GA search, CYTools, `resources/` (data dependencies like `.dat` files). |
| **cyrus** (Hands) | **Rust Implementation** | New high-performance physics toolkit (Cyrus). |

### Important Linkage
- **Documentation**: Use the `./project/` symlink to access the central knowledge base.
- **Source of Truth**: Do NOT add documentation here. Add it to `string_theory_project/`.

---

## Local Setup (Execution & Data)

### Execution Environment
- Python: Homebrew 3.11 (`/opt/homebrew/opt/python@3.11/bin/python3.11`)
- Package manager: `uv`
- Run Python: `uv run python script.py`
- Run tests: `uv run pytest`

### Data Dependencies (`resources/`)
This repo is the **Primary Source of Data** for the McAllister reproduction and GA search.
- `resources/small_cc_2107.09064_source/anc/paper_data/` - Essential `.dat` files.
- `resources/mcallister_4-214-647_orientifold.json` - Orientifold mask data.

**CRITICAL**: Do NOT move `.dat`, `.json`, or `.txt` files out of `resources/`. Scripts depend on these relative paths.

---

## CRITICAL: Development Mandates

**Read `project/AGENTS.md` before starting.**

1. **Exactness at Decision Boundaries**: Floating point is forbidden for geometric decision making.
2. **"No Cheating" Rule**: We do not hardcode constants from papers. Every derived value (e.g., $W_0$, $g_s$) must be computed from first principles within the pipeline.
3. **Multiprocessing Warning**: CYTools uses multiprocessing. Scripts MUST be written to actual `.py` files (no heredocs) and use `if __name__ == "__main__":` guards.
4. **Institutional Memory**: NEVER delete debugging/testing scripts (`debug_*.py`, `test_*.py`). They document API usage and edge cases.

---

## Navigation via Symlink
- [[project/project_docs/FORMULAS.md|Physics Formula Reference]]
- [[project/project_docs/CYTOOLS_ALGORITHMS_CLEAN_ROOM.md|CYTools Algorithm Specs]]
- [[project/research/mcallister_reproduction/REPRODUCTION_OUTLINE.md|McAllister Reproduction Status]]
