# String Theory Project: Central Knowledge Base

This is the central knowledge base and project management database for the String Theory and Cyrus projects.

## Documentation
- **AGENTS.md**: The "Ground Control" manual for Gemini (Project Manager).
- **CLAUDE.md**: Tooling instructions for Claude (Coding Agent).
- **project_docs/**: General documentation.

## Repository Structure
- `ai_chats/`: Significant AI interaction logs.
- `feedback/`: Triage for bugs and ideas.
- `prds/`: Product Requirements Documents.
- `research/`: Deep-dive research notes and paper summaries.
- `todo/`: Task tracking and roadmaps.
- `scripts/`: Tooling for knowledge management and semantic search.

## Knowledge Management
This repo is **additive-only**. Nothing is archived or deleted.
Every thought, bug fix, and research insight is recorded here to build a comprehensive RAG-ready corpus.

## Setup for Other Repos
To link this knowledge base to your workspace:
```bash
# For Cyrus
./scripts/setup_project.sh ../cyrus

# For String Theory Search
./scripts/setup_project.sh ../string_theory_search
```
This creates a `./project/` symlink and links the appropriate `CLAUDE.md`.

## Tooling
- **Search**: `bin/semgrep "query"` (requires `OPENAI_API_KEY` in `.env`)
- **Index**: `bin/semgrep-index` (requires `OPENAI_API_KEY` in `.env`)