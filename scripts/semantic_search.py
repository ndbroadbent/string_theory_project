#!/usr/bin/env python3
"""
Semantic search across project documentation and code.

Searches the ChromaDB index built by build_index.py.
Designed to run from chat_to_map_saas repo (or any repo with project/ symlink).

Usage:
    semgrep "your search query"
    semgrep "aggregation logic" --top 10
    semgrep "dark mode" --threshold 0.2
    semgrep "component" --type ts          # Only TypeScript files
    semgrep "readme" --type md             # Only markdown files
    semgrep "query" src/                   # Only files in src/
    semgrep "query" project/ --type md     # Markdown in project/
"""

# Default similarity threshold - results below this are noise
DEFAULT_THRESHOLD = 0.1

import argparse
import hashlib
import json
import os
from pathlib import Path

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

# Disable ChromaDB telemetry
CHROMA_SETTINGS = Settings(anonymized_telemetry=False)

# Configuration
EMBEDDING_MODEL = "text-embedding-3-large"


def get_storage_root() -> Path:
    """Get the root directory for cache and index storage.

    When running from saas repo, this is CWD/project/ (via symlink).
    When running from project repo directly, this is CWD.
    """
    cwd = Path.cwd()
    project_dir = cwd / "project"

    if project_dir.exists() and project_dir.is_symlink():
        # Running from saas repo - use project/ for storage
        return project_dir.resolve()
    elif (cwd / "scripts" / "semantic_search.py").exists():
        # Running from project repo directly
        return cwd
    else:
        # Fallback - use project/ if it exists, else CWD
        return project_dir if project_dir.exists() else cwd


def get_cache_path(storage_root: Path, model: str, cache_type: str, content: str) -> Path:
    """Generate cache path for an embedding request."""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    cache_path = storage_root / ".ai_cache" / "openai" / model / cache_type / f"{content_hash}.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    return cache_path


def get_embedding(client: OpenAI, text: str, storage_root: Path, cache_type: str = "search") -> list[float]:
    """Get embedding for text, using cache if available."""
    cache_path = get_cache_path(storage_root, EMBEDDING_MODEL, cache_type, text)

    # Check cache
    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)["embedding"]

    # Call API
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    embedding = response.data[0].embedding

    # Cache response
    with open(cache_path, "w") as f:
        json.dump({"text": text, "embedding": embedding}, f)

    return embedding


def main():
    parser = argparse.ArgumentParser(description="Semantic search across project docs and code")
    parser.add_argument("query", help="Search query")
    parser.add_argument("path", nargs="?", help="Filter to files under this path (e.g. src/, project/)")
    parser.add_argument("--top", "-n", type=int, default=10, help="Number of results (default: 10)")
    parser.add_argument(
        "--threshold", "-t", type=float, default=DEFAULT_THRESHOLD,
        help=f"Minimum similarity threshold (default: {DEFAULT_THRESHOLD})"
    )
    parser.add_argument(
        "--type", dest="file_type",
        help="Filter by file type (e.g. md, ts, py, svelte)"
    )
    parser.add_argument("-A", type=int, default=0, help="Show N chunks after match")
    parser.add_argument("-B", type=int, default=0, help="Show N chunks before match")
    parser.add_argument("-C", type=int, default=0, help="Show N chunks before and after match")
    parser.add_argument("--no-line-num", action="store_true", help="Hide line numbers")
    parser.add_argument("--similarity", action="store_true", help="Show similarity scores")
    parser.add_argument("--chunk", action="store_true", help="Show chunk indices")
    args = parser.parse_args()

    # -C sets both -A and -B
    if args.C:
        args.A = args.C
        args.B = args.C

    # Get storage root
    storage_root = get_storage_root()
    chroma_dir = storage_root / ".chroma"

    # Check if index exists
    if not chroma_dir.exists():
        print("Error: No index found. Run semgrep-index first:")
        print("  semgrep-index")
        return 1

    # Load environment from storage root
    env_file = storage_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env")
        return 1

    client = OpenAI(api_key=api_key)

    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path=str(chroma_dir), settings=CHROMA_SETTINGS)

    try:
        collection = chroma_client.get_collection("project_docs")
    except ValueError:
        print("Error: Collection 'project_docs' not found. Run semgrep-index first.")
        return 1

    # Build where clause for filtering
    where_clause = None
    where_conditions = []

    if args.file_type:
        # Normalize file type (remove leading dot if present)
        file_type = args.file_type.lstrip(".")
        where_conditions.append({"file_type": file_type})

    if args.path:
        # Path filtering is done post-query since ChromaDB doesn't support prefix matching
        pass

    if len(where_conditions) == 1:
        where_clause = where_conditions[0]
    elif len(where_conditions) > 1:
        where_clause = {"$and": where_conditions}

    # Get query embedding
    query_embedding = get_embedding(client, args.query, storage_root, "search")

    # Search - get more results if we're filtering by path
    n_results = args.top * 5 if args.path else args.top

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_clause
    )

    # Display results (grep-style output)
    if not results["documents"][0]:
        print("No results found.")
        return 0

    # Helper to format a result line
    def format_line(filepath, line_num, chunk_idx, similarity, text, is_match=True):
        parts = [filepath]
        sep = ":" if is_match else "-"

        if not args.no_line_num and line_num is not None:
            parts.append(f"{sep}{line_num}")

        if args.chunk:
            parts.append(f"{sep}c{chunk_idx}")

        if args.similarity and is_match:
            parts.append(f"{sep}[{similarity:.2f}]")

        parts.append(f"{sep}{text}")
        return "".join(parts)

    # Filter by path prefix and threshold, then display
    shown = 0
    for doc, metadata, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        similarity = 1 - distance

        # Skip results below threshold
        if similarity < args.threshold:
            continue

        filepath = metadata["filepath"]

        # Filter by path prefix if specified
        if args.path:
            # Normalize path (remove trailing slash)
            filter_path = args.path.rstrip("/")
            if not filepath.startswith(filter_path):
                continue

        shown += 1
        if shown > args.top:
            break

        chunk_index = metadata["chunk_index"]
        line_num = metadata.get("line_num")

        # Get context chunks if requested
        if args.B > 0 or args.A > 0:
            if shown > 1:
                print("--")  # Separator between results (like grep)
            for offset in range(-args.B, args.A + 1):
                target_idx = chunk_index + offset
                if target_idx < 0:
                    continue
                chunk_id = f"{filepath}:{target_idx}"
                try:
                    context = collection.get(ids=[chunk_id])
                    if context["documents"] and context["metadatas"]:
                        ctx_line = context["metadatas"][0].get("line_num")
                        text = context["documents"][0].replace("\n", " ")[:200]
                        print(format_line(filepath, ctx_line, target_idx,
                                          similarity, text, is_match=(offset == 0)))
                except Exception:
                    pass
        else:
            text = doc.replace("\n", " ")[:200]
            print(format_line(filepath, line_num, chunk_index, similarity, text))

    if shown == 0:
        if args.path or args.file_type:
            filters = []
            if args.path:
                filters.append(f"path={args.path}")
            if args.file_type:
                filters.append(f"type={args.file_type}")
            print(f"No results matching filters ({', '.join(filters)}) above threshold ({args.threshold}).")
        else:
            print(f"No results above threshold ({args.threshold}).")
    return 0


if __name__ == "__main__":
    exit(main())
