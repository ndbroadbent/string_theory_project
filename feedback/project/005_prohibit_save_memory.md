# Feedback: Prohibition of `save_memory` tool

**Date**: 2026-01-01
**Source**: User chat
**Status**: **TRIAGED**

**Triaged to:**
- `AGENTS.md`: Added explicit prohibition of the `save_memory` tool.

## Feedback
- The `save_memory` tool writes to `~/.gemini/GEMINI.md`, which is outside the repository.
- This information is lost if the computer is wiped.
- **Requirement**: All "long-term memory," rules, and preferences MUST be written directly into `AGENTS.md` within the repository.
- **Requirement**: README.md is external-facing only and is NOT part of the knowledge graph.

## Action Items
- [x] Update `AGENTS.md` to forbid `save_memory`.
- [x] Update `AGENTS.md` regarding `README.md` status.
