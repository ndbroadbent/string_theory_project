# Feedback: Semgrep Indexing Costs and Rigorous Caching

**Date**: 2026-01-01
**Source**: User chat
**Status**: PENDING

## Feedback
- `bin/semgrep` is critical to get right; mistakes can cost hundreds of dollars.
- Indexing massive physics papers (LaTeX) requires rigorous caching.
- Caching is a hard requirement.
- An **allowlist** of papers/files to index is required to prevent accidental bulk indexing of `research/`.
- This is a core part of the feedback/triage system.

## Proposed Actions (Initial)
- [ ] Implement `scripts/index_allowlist.txt`.
- [ ] Ensure `build_index.py` respects the allowlist.
- [ ] Verify caching logic in `build_index.py`.
- [ ] Make `--dry-run` the default or highly visible.
