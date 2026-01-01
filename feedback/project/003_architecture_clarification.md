# Feedback: Architecture Clarification and Search Strategy

**Date**: 2026-01-01
**Source**: User chat
Status: **TRIAGED**

**Triaged to:**
- `AGENTS.md`: Added "Obsessive Retention" and "Separation of Concerns" directives.
- `AGENTS.md`: Updated "Indexing" section with strict strategy.

## Feedback
- **End State**: All knowledge (docs, research, plans) lives in `string_theory_project` (THIS repo).
- **Code Repos**: `cyrus` and `string_theory_search` contain *only* code, scripts, and implementation assets.
- **Linkage**: Agents in code repos access knowledge via `./project` symlink.
- **Search Strategy**: Index THIS repo. Do NOT index `reference/` (because knowledge should be migrated here).
- **Failure**: Gemini failed to note this down in `AGENTS.md` before acting.

## Action Items
- [ ] Add "Separation of Concerns" directive to `AGENTS.md`.
- [ ] Add "Search Strategy" to `AGENTS.md`.
