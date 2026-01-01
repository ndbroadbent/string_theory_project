# PRD: Central Knowledge Base & Project Management Database

## Overview
A central repository for the `string_theory` and `cyrus` projects to manage documentation, research, task tracking, and AI-assisted knowledge management.

## Goals
1. **Centralized Truth**: One place for all design docs, PRDs, and research notes.
2. **Additive-Only Record**: Never archive or delete; maintain a complete history of the project's evolution.
3. **Semantic Search**: 100% vector embedding search across all content.
4. **Automated Knowledge Graph**: Future-proofing for RAG and automated insight generation.

## Structure
- `ai_chats/`: Transcripts of significant AI interactions.
- `ai_pm_reviews/`: AI-generated reviews of project progress and strategy.
- `bin/` & `scripts/`: Tooling for indexing, search, and project management.
- `design/`: UI/UX and architectural design documents.
- `experiments/`: Documentation of experimental results and hypotheses.
- `feedback/`: Triage for user and developer feedback.
- `prds/`: Product Requirements Documents for all sub-components.
- `project_docs/`: General documentation.
- `qa/`: Quality assurance plans and test results.
- `research/`: Deep-dive research notes and paper summaries.
- `templates/`: Reusable document templates.
- `todo/`: Task lists and roadmap items.
- `user_stories/`: User-centric feature definitions.

## Tooling
- **ChromaDB**: For vector storage.
- **OpenAI Embeddings**: `text-embedding-3-large`.
- **scripts/build_index.py**: To update the index.
- **scripts/semantic_search.py**: For querying the knowledge base.
