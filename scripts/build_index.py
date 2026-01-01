#!/usr/bin/env python3
"""
Build semantic search index for project documentation and code.

Indexes markdown and code files into ChromaDB with OpenAI embeddings.
Designed to run from chat_to_map_saas repo (or any repo with project/ symlink).

Usage:
    # From saas repo:
    semgrep-index                      # Index all configured directories
    semgrep-index --dry-run            # Estimate costs without API calls
    semgrep-index --limit 100          # Test with first 100 chunks
    semgrep-index src/                 # Index specific directory
    semgrep-index project/*.md         # Index specific files
"""

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
from pathlib import Path

import chromadb
import tiktoken
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

# Disable ChromaDB telemetry
CHROMA_SETTINGS = Settings(anonymized_telemetry=False)

# Embedding configuration
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_COST_PER_1M_TOKENS = 0.13  # USD per 1M tokens

# File types to index
INDEXABLE_EXTENSIONS = {
    # Documentation
    ".md": "markdown",
    ".sql": "sql",
    # Code
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".py": "python",
    ".svelte": "svelte",
    ".rs": "rust",
}

# Directories to exclude from indexing
EXCLUDED_DIRS = {
    ".venv",
    "venv",
    "node_modules",
    ".git",
    "__pycache__",
    ".chroma",
    ".ai_cache",
    ".svelte-kit",
    "dist",
    "build",
    ".wrangler",
    "coverage",
}

# Default directories to index (relative to CWD)
# We scan everything, but filter by allowlist
DEFAULT_INDEX_DIRS = ["."]

# Setup logging
logger = logging.getLogger(__name__)

# Tokenizer (cached after first load)
_tokenizer = None


def load_allowlist(storage_root: Path) -> set[str]:
    """Load the index allowlist from scripts/index_allowlist.txt."""
    allowlist_path = storage_root / "scripts" / "index_allowlist.txt"
    if not allowlist_path.exists():
        logger.warning(f"Allowlist not found at {allowlist_path}. Indexing NOTHING by default.")
        return set()

    allowed = set()
    with open(allowlist_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                allowed.add(line)
    return allowed


def is_allowed(rel_path: str, allowlist: set[str]) -> bool:
    """Check if a relative path is in the allowlist.
    
    Rules:
    1. Everything in reference/ is BLOCKED by default (even .md files).
    2. All other .md files are allowed automatically.
    3. Other files must be in the allowlist (exact path or directory prefix).
    """
    # Rule 1: Block reference/ by default
    if rel_path.startswith("reference/"):
        # You can override this by adding specific reference/ paths to allowlist
        if rel_path in allowlist:
            return True
        for allowed in allowlist:
            if allowed.endswith("/") and rel_path.startswith(allowed):
                return True
        return False

    # Rule 2: Allow all other markdown files
    if rel_path.endswith(".md"):
        return True

    # Rule 3: Check allowlist
    if rel_path in allowlist:
        return True
    
    # Check directory prefixes
    for allowed in allowlist:
        if allowed.endswith("/") and rel_path.startswith(allowed):
            return True
            
    return False


def get_tokenizer():
    """Get tiktoken tokenizer (lazy loaded)."""
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = tiktoken.get_encoding("cl100k_base")
    return _tokenizer


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    return len(get_tokenizer().encode(text))


def format_cost(cost: float) -> str:
    """Format cost in dollars, showing appropriate precision."""
    if cost < 0.01:
        return f"${cost:.4f}"
    return f"${cost:.2f}"


def is_worktree() -> bool:
    """Check if current directory is a git worktree (not the main repo)."""
    git_path = Path.cwd() / ".git"
    if git_path.is_file():
        # .git is a file in worktrees, containing "gitdir: /path/to/.git/worktrees/name"
        return True
    return False


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
    elif (cwd / "scripts" / "build_index.py").exists():
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


def is_cached(storage_root: Path, model: str, text: str, cache_type: str = "content") -> bool:
    """Check if embedding is cached (without loading it)."""
    cache_path = get_cache_path(storage_root, model, cache_type, text)
    return cache_path.exists()


def get_embeddings_batch(
    client: OpenAI,
    texts: list[str],
    model: str,
    storage_root: Path,
    cache_type: str = "content",
    cache_mode: str = "normal",
    batch_size: int = 100,
) -> tuple[list[list[float]], int, int, int]:
    """Get embeddings for multiple texts with batching.

    Returns (embeddings, cached_count, uncached_count, api_requests).
    Checks cache first, batches uncached texts to API, caches results.
    """
    embeddings = [None] * len(texts)
    cached_count = 0
    uncached_indices = []
    uncached_texts = []

    # First pass: check cache
    for i, text in enumerate(texts):
        cache_path = get_cache_path(storage_root, model, cache_type, text)
        if cache_mode == "normal" and cache_path.exists():
            with open(cache_path) as f:
                embeddings[i] = json.load(f)["embedding"]
            cached_count += 1
        else:
            uncached_indices.append(i)
            uncached_texts.append(text)

    # Batch API calls for uncached texts
    api_requests = 0
    for batch_start in range(0, len(uncached_texts), batch_size):
        batch_texts = uncached_texts[batch_start : batch_start + batch_size]
        batch_indices = uncached_indices[batch_start : batch_start + batch_size]

        logger.info(f"  API request {api_requests + 1}: {len(batch_texts)} texts")
        response = client.embeddings.create(model=model, input=batch_texts)
        api_requests += 1

        for j, item in enumerate(response.data):
            idx = batch_indices[j]
            text = batch_texts[j]
            embedding = item.embedding
            embeddings[idx] = embedding

            # Cache response (unless none mode)
            if cache_mode != "none":
                cache_path = get_cache_path(storage_root, model, cache_type, text)
                with open(cache_path, "w") as f:
                    json.dump({"text": text, "embedding": embedding}, f)

    return embeddings, cached_count, len(uncached_texts), api_requests


def split_markdown_into_chunks(content: str, filepath: str) -> list[dict]:
    """Split markdown content into searchable chunks (paragraphs) with line numbers."""
    chunks = []
    current_pos = 0
    chunk_index = 0
    file_type = Path(filepath).suffix.lstrip(".")

    # Split by double newlines (paragraphs)
    for para in re.split(r"\n\n+", content):
        para_stripped = para.strip()
        if not para_stripped or len(para_stripped) < 20:
            current_pos = content.find(para, current_pos) + len(para)
            continue

        # Skip code blocks that are just syntax
        if para_stripped.startswith("```") and para_stripped.endswith("```"):
            current_pos = content.find(para, current_pos) + len(para)
            continue

        # Find line number where this paragraph starts
        para_start = content.find(para, current_pos)
        line_num = content[:para_start].count("\n") + 1

        chunks.append({
            "id": f"{filepath}:{chunk_index}",
            "text": para_stripped,
            "metadata": {
                "filepath": filepath,
                "file_type": file_type,
                "chunk_index": chunk_index,
                "line_num": line_num,
            },
        })
        chunk_index += 1
        current_pos = para_start + len(para)

    return chunks


def split_code_into_chunks(content: str, filepath: str) -> list[dict]:
    """Split code content into searchable chunks.

    Strategy: Split by logical blocks (functions, classes) or fall back to
    paragraph-style splitting for simpler files.
    """
    chunks = []
    chunk_index = 0
    file_type = Path(filepath).suffix.lstrip(".")
    lines = content.split("\n")

    # For now, use a simple approach: split by blank lines or logical boundaries
    # This works reasonably well for most code
    current_chunk_lines = []
    current_start_line = 1

    for i, line in enumerate(lines, 1):
        # Check for logical boundaries
        is_boundary = (
            line.strip() == "" and current_chunk_lines and
            len("\n".join(current_chunk_lines)) > 100
        )

        # Also split on function/class definitions if chunk is getting large
        is_definition = (
            len(current_chunk_lines) > 20 and
            (line.strip().startswith("function ") or
             line.strip().startswith("export function ") or
             line.strip().startswith("export const ") or
             line.strip().startswith("class ") or
             line.strip().startswith("def ") or
             line.strip().startswith("async def ") or
             line.strip().startswith("export default "))
        )

        if is_boundary or is_definition:
            chunk_text = "\n".join(current_chunk_lines).strip()
            if chunk_text and len(chunk_text) >= 20:
                chunks.append({
                    "id": f"{filepath}:{chunk_index}",
                    "text": chunk_text,
                    "metadata": {
                        "filepath": filepath,
                        "file_type": file_type,
                        "chunk_index": chunk_index,
                        "line_num": current_start_line,
                    },
                })
                chunk_index += 1

            current_chunk_lines = [line] if is_definition else []
            current_start_line = i
        else:
            if not current_chunk_lines:
                current_start_line = i
            current_chunk_lines.append(line)

    # Don't forget the last chunk
    chunk_text = "\n".join(current_chunk_lines).strip()
    if chunk_text and len(chunk_text) >= 20:
        chunks.append({
            "id": f"{filepath}:{chunk_index}",
            "text": chunk_text,
            "metadata": {
                "filepath": filepath,
                "file_type": file_type,
                "chunk_index": chunk_index,
                "line_num": current_start_line,
            },
        })

    return chunks


def split_into_chunks(content: str, filepath: str) -> list[dict]:
    """Split file content into chunks based on file type."""
    ext = Path(filepath).suffix.lower()
    if ext == ".md":
        return split_markdown_into_chunks(content, filepath)
    else:
        return split_code_into_chunks(content, filepath)


def find_indexable_files(root: Path, base_path: Path = None) -> list[tuple[Path, str]]:
    """Find all indexable files in a directory.

    Returns list of (absolute_path, relative_path) tuples.
    relative_path is relative to base_path (or root if not specified).
    """
    if base_path is None:
        base_path = root

    files = []

    if not root.exists():
        return files

    for path in root.rglob("*"):
        # Skip excluded directories
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            continue

        # Skip non-files
        if not path.is_file():
            continue

        # Check extension
        if path.suffix.lower() not in INDEXABLE_EXTENSIONS:
            continue

        # Get relative path from base
        try:
            relative = str(path.relative_to(base_path))
        except ValueError:
            relative = str(path)

        files.append((path, relative))

    return sorted(files, key=lambda x: x[1])


def main():
    parser = argparse.ArgumentParser(
        description="Build semantic search index for docs and code"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Specific files or directories to index (default: all configured dirs)",
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "--limit", "-l", type=int, default=None,
        help="Limit number of chunks to index (for testing)",
    )
    parser.add_argument(
        "--update-cache", action="store_true",
        help="Force refresh cache (write only, no read)"
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Skip cache entirely (no read, no write)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Estimate costs without making API calls"
    )
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s" if args.debug else "%(message)s",
        datefmt="%H:%M:%S",
    )

    # Suppress noisy third-party loggers
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    # Check for worktree
    if is_worktree():
        logger.error("ERROR: Running from a git worktree is not allowed.")
        logger.error("Worktrees would create duplicate index entries.")
        logger.error("Please run from the main repo: ~/code/chat_to_map_saas")
        return 1

    # Determine cache mode
    if args.no_cache:
        cache_mode = "none"
    elif args.update_cache:
        cache_mode = "update"
    else:
        cache_mode = "normal"

    # Get storage root (where cache and index live)
    storage_root = get_storage_root()
    cache_dir = storage_root / ".ai_cache" / "openai"
    chroma_dir = storage_root / ".chroma"

    logger.info(f"Storage root: {storage_root}")
    logger.info(f"Working dir: {Path.cwd()}")

    # Load environment from storage root
    env_file = storage_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    # Initialize OpenAI client (skip for dry-run)
    client = None
    if not args.dry_run:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in .env")
            logger.error(f"Create {storage_root / '.env'} with your API key")
            return 1
        client = OpenAI(api_key=api_key)

    # Initialize ChromaDB (skip for dry-run)
    chroma_client = None
    collection = None
    if not args.dry_run:
        logger.debug(f"ChromaDB path: {chroma_dir}")
        chroma_client = chromadb.PersistentClient(path=str(chroma_dir), settings=CHROMA_SETTINGS)

    # Determine what to index
    cwd = Path.cwd()
    files_to_index = []
    
    # Load allowlist
    allowlist = load_allowlist(storage_root)
    if not allowlist and not args.paths:
        logger.error("No allowlist found and no paths specified. Aborting.")
        return 1

    if args.paths:
        # Specific paths provided - bypass allowlist check (explicit user intent)
        for pattern in args.paths:
            path = Path(pattern)
            if path.is_file():
                files_to_index.append((path.resolve(), str(path)))
            elif path.is_dir():
                files_to_index.extend(find_indexable_files(path.resolve(), cwd))
            else:
                # Try as glob pattern
                for p in cwd.glob(pattern):
                    if p.is_file() and p.suffix.lower() in INDEXABLE_EXTENSIONS:
                        files_to_index.append((p.resolve(), str(p.relative_to(cwd))))
                    elif p.is_dir():
                        files_to_index.extend(find_indexable_files(p.resolve(), cwd))

        files_to_index = sorted(set(files_to_index), key=lambda x: x[1])
        logger.info(f"Indexing {len(files_to_index)} specified file(s) (bypassing allowlist)")

        # When indexing specific files/dirs, update existing collection
        if chroma_client:
            collection = chroma_client.get_or_create_collection(
                name="project_docs",
                metadata={"hnsw:space": "cosine"},
            )
    else:
        # Index default directories with allowlist filtering
        potential_files = []
        for dir_name in DEFAULT_INDEX_DIRS:
            dir_path = cwd / dir_name
            if dir_path.exists():
                potential_files.extend(find_indexable_files(dir_path, cwd))

        # Filter by allowlist
        for abs_path, rel_path in potential_files:
            if is_allowed(rel_path, allowlist):
                files_to_index.append((abs_path, rel_path))
            else:
                # Optional: Log skipped files at DEBUG level
                # logger.debug(f"Skipped {rel_path} (not in allowlist)")
                pass

        logger.info(f"Found {len(files_to_index)} indexable files in allowlist")

        # Full rebuild - delete and recreate collection
        if chroma_client:
            try:
                chroma_client.delete_collection("project_docs")
                logger.debug("Deleted existing collection")
            except Exception:
                pass

            collection = chroma_client.create_collection(
                name="project_docs",
                metadata={"hnsw:space": "cosine"},
            )

    # Collect all chunks
    all_chunks = []
    files_processed = []

    for abs_path, rel_path in files_to_index:
        try:
            content = abs_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"  Skipping {rel_path}: {e}")
            continue

        chunks = split_into_chunks(content, rel_path)
        if chunks:
            all_chunks.extend(chunks)
            files_processed.append(rel_path)
            logger.debug(f"  {rel_path}: {len(chunks)} chunks")

    # If updating specific files, remove their old chunks first
    if args.paths and files_processed and collection:
        for filepath in files_processed:
            existing = collection.get(where={"filepath": filepath})
            if existing["ids"]:
                collection.delete(ids=existing["ids"])
                logger.debug(f"  Removed {len(existing['ids'])} old chunks from {filepath}")

    logger.info(f"Total chunks to index: {len(all_chunks)}")

    # Apply limit if specified
    if args.limit:
        all_chunks = all_chunks[: args.limit]
        logger.info(f"Limited to {len(all_chunks)} chunks (--limit {args.limit})")

    if not all_chunks:
        logger.info("No chunks to index.")
        return 0

    # Track stats
    total_chunks = len(all_chunks)
    cached_count = 0
    uncached_count = 0
    cached_tokens = 0
    uncached_tokens = 0

    # Dry-run mode: just scan and estimate costs
    if args.dry_run:
        logger.info(f"\n[DRY RUN] Scanning cache for model: {EMBEDDING_MODEL}")

        for chunk in all_chunks:
            tokens = count_tokens(chunk["text"])
            if is_cached(storage_root, EMBEDDING_MODEL, chunk["text"], "content"):
                cached_count += 1
                cached_tokens += tokens
            else:
                uncached_count += 1
                uncached_tokens += tokens

        # Calculate costs
        total_tokens = cached_tokens + uncached_tokens
        total_cost = (total_tokens / 1_000_000) * EMBEDDING_COST_PER_1M_TOKENS
        cached_cost = (cached_tokens / 1_000_000) * EMBEDDING_COST_PER_1M_TOKENS
        uncached_cost = (uncached_tokens / 1_000_000) * EMBEDDING_COST_PER_1M_TOKENS

        # Calculate batch count (100 per batch)
        batch_size = 100
        batch_count = (uncached_count + batch_size - 1) // batch_size if uncached_count > 0 else 0

        logger.info(f"\n{'=' * 50}")
        logger.info(f"Cost Estimate for {EMBEDDING_MODEL}")
        logger.info(f"{'=' * 50}")
        logger.info(f"Total chunks:    {total_chunks:,}")
        logger.info(f"Total tokens:    {total_tokens:,}")
        logger.info(f"")
        logger.info(f"Cached:          {cached_count:,} chunks ({cached_tokens:,} tokens)")
        logger.info(f"Uncached:        {uncached_count:,} chunks ({uncached_tokens:,} tokens)")
        logger.info(f"API requests:    {batch_count} (batch size: {batch_size})")
        logger.info(f"")
        logger.info(f"Cost if all API: {format_cost(total_cost)}")
        logger.info(f"Saved by cache:  {format_cost(cached_cost)}")
        logger.info(f"This run cost:   {format_cost(uncached_cost)}")
        logger.info(f"{'=' * 50}")
        return 0

    # Real indexing mode
    texts = [chunk["text"] for chunk in all_chunks]

    # Count tokens before API calls
    for text in texts:
        tokens = count_tokens(text)
        if is_cached(storage_root, EMBEDDING_MODEL, text, "content"):
            cached_tokens += tokens
        else:
            uncached_tokens += tokens

    logger.info("Generating embeddings (batched)...")
    embeddings, cached_count, uncached_count, api_requests = get_embeddings_batch(
        client, texts, EMBEDDING_MODEL, storage_root, "content", cache_mode
    )

    # Add all to ChromaDB (in batches due to max batch size limit)
    logger.info("Adding to ChromaDB...")
    CHROMA_BATCH_SIZE = 5000  # ChromaDB max is 5461
    for batch_start in range(0, len(all_chunks), CHROMA_BATCH_SIZE):
        batch_end = min(batch_start + CHROMA_BATCH_SIZE, len(all_chunks))
        batch_chunks = all_chunks[batch_start:batch_end]
        batch_embeddings = embeddings[batch_start:batch_end]

        collection.add(
            ids=[chunk["id"] for chunk in batch_chunks],
            embeddings=batch_embeddings,
            documents=[chunk["text"] for chunk in batch_chunks],
            metadatas=[chunk["metadata"] for chunk in batch_chunks],
        )
        logger.debug(f"  Added batch {batch_start // CHROMA_BATCH_SIZE + 1}: {len(batch_chunks)} chunks")

    total_indexed = len(all_chunks)

    # Calculate costs
    total_tokens = cached_tokens + uncached_tokens
    total_cost = (total_tokens / 1_000_000) * EMBEDDING_COST_PER_1M_TOKENS
    cached_cost = (cached_tokens / 1_000_000) * EMBEDDING_COST_PER_1M_TOKENS
    uncached_cost = (uncached_tokens / 1_000_000) * EMBEDDING_COST_PER_1M_TOKENS

    logger.info(f"\n{'=' * 50}")
    logger.info(f"Indexing Complete ({EMBEDDING_MODEL})")
    logger.info(f"{'=' * 50}")
    logger.info(f"Indexed:         {total_indexed:,} chunks from {len(files_processed)} files")
    logger.info(f"Total tokens:    {total_tokens:,}")
    logger.info(f"")
    logger.info(f"Cache hits:      {cached_count:,} chunks ({cached_tokens:,} tokens)")
    logger.info(f"Uncached:        {uncached_count:,} chunks ({uncached_tokens:,} tokens)")
    logger.info(f"API requests:    {api_requests}")
    logger.info(f"")
    logger.info(f"Cost if all API: {format_cost(total_cost)}")
    logger.info(f"Saved by cache:  {format_cost(cached_cost)}")
    logger.info(f"This run cost:   {format_cost(uncached_cost)}")
    logger.info(f"{'=' * 50}")
    logger.info(f"Database: {chroma_dir}")
    return 0


if __name__ == "__main__":
    exit(main())
