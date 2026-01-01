#!/usr/bin/env bash
set -euo pipefail

# Setup the project symlink in another repository
# Usage: ./scripts/setup_project.sh <path-to-repo>

REPO_PATH="${1:-}"

if [[ -z "$REPO_PATH" ]]; then
  echo "Usage: $0 <path-to-repo>"
  exit 1
fi

if [[ ! -d "$REPO_PATH" ]]; then
  echo "Error: Directory $REPO_PATH does not exist"
  exit 1
fi

# Get absolute path to this project repo
PROJECT_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
ABS_REPO_PATH="$(cd "$REPO_PATH" && pwd -P)"

echo "Setting up project symlink in $ABS_REPO_PATH..."

if [[ -L "$ABS_REPO_PATH/project" ]]; then
  echo "  ✓ project/ symlink already exists"
else
  ln -s "$PROJECT_REPO" "$ABS_REPO_PATH/project"
  echo "  ✓ project/ symlink created"
fi

# Check for CLAUDE.md and offer to link it if missing
if [[ ! -L "$ABS_REPO_PATH/CLAUDE.md" ]] && [[ ! -f "$ABS_REPO_PATH/CLAUDE.md" ]]; then
  echo "  ? CLAUDE.md is missing. Linking appropriate CLAUDE file..."
  
  if [[ -f "$ABS_REPO_PATH/crates/cyrus-core/Cargo.toml" ]]; then
    echo "    Detected Cyrus repo."
    ln -s "project/CYRUS_CLAUDE.md" "$ABS_REPO_PATH/CLAUDE.md"
    echo "    ✓ Linked CYRUS_CLAUDE.md"
  elif [[ -f "$ABS_REPO_PATH/src/searcher.rs" ]]; then
    echo "    Detected String Theory Search repo."
    ln -s "project/STRING_THEORY_CLAUDE.md" "$ABS_REPO_PATH/CLAUDE.md"
    echo "    ✓ Linked STRING_THEORY_CLAUDE.md"
  else
    echo "    ⚠ Could not detect repo type. Please link CLAUDE.md manually."
  fi
fi
