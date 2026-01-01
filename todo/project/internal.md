# Internal Project Management Tasks

This file tracks tasks for improving the project management system itself (Gemini's internal operations).

## Knowledge Base Migration & Organization
- [ ] **Audit & Categorize**:
    - [ ] Complete inventory of `reference/cyrus` docs.
    - [ ] Complete inventory of `reference/string_theory_search` docs.
- [ ] **Synthesis**:
    - [ ] Update `project_docs/FORMAL_VERIFICATION.md` with full details from `reference/cyrus` if available.
    - [ ] Create `project_docs/ARCHITECTURE.md` unifying the Cyrus and String Theory architectures.
- [ ] **Verification**:
    - [ ] Verify `research/mcallister_reproduction/` contains all critical context from the old repo.

## Tooling & Infrastructure
- [ ] **Semgrep Cost Controls**:
    - [ ] Implement `scripts/index_allowlist.txt`.
    - [ ] Update `scripts/build_index.py` to enforce the allowlist.
    - [ ] Update `bin/semgrep-index` to default to `--dry-run` or require confirmation.
    - [ ] Verify caching logic covers all API calls.
- [ ] **Search Indexing**:
    - [ ] Run `bin/semgrep-index` to populate the initial index.
    - [ ] Verify `bin/semgrep` works across submodules.
- [ ] **Submodules**:
    - [ ] Verify `git submodule update --remote` workflow works locally.

## Project Management
- [ ] **Triage**:
    - [ ] Review `todo/legacy_string_theory.md` and move active items to `todo/string_theory_tasks.md`.
    - [ ] Review `todo/CRITICAL.md` and integrate into the main roadmap.
