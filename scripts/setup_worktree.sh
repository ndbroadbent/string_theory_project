#!/usr/bin/env bash
set -euo pipefail

# Setup a new git worktree with all dependencies for any ChatToMap work
# Usage: ./scripts/setup_worktree.sh <branch-name>
#
# Can be run from ANYWHERE - it finds the repos automatically.
#
# This script is IDEMPOTENT - safe to re-run to update existing worktrees.
#
# Creates a complete working environment with:
# - project symlink (shared coordination)
# - chat_to_map submodule (isolated copy)
# - chat_to_map_desktop clone (isolated copy)
# - feedback directory for the branch
#
# NOTE: CLAUDE.md is tracked in git as a symlink - worktrees inherit it automatically

BRANCH="${1:-}"

if [[ -z "$BRANCH" ]]; then
  echo "Usage: $0 <branch-name>"
  echo ""
  echo "Creates a worktree for ANY ChatToMap work (SaaS, core, or desktop)."
  echo "Can be run from anywhere - finds repos automatically."
  echo "Safe to re-run on existing worktrees to update symlinks."
  echo ""
  echo "Examples:"
  echo "  $0 feature-pricing-slider    # SaaS feature work"
  echo "  $0 core-parser-refactor      # Core library work"
  echo "  $0 desktop-imessage-export   # Desktop app work"
  exit 1
fi

# Find the project repo (where this script lives)
# Use -P to get physical path (resolve symlinks)
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_REPO="${SCRIPT_PATH%/scripts}"

# Find the SaaS repo (sibling directory)
PARENT_DIR="$(dirname "$PROJECT_REPO")"
REPO_ROOT="$PARENT_DIR/chat_to_map_saas"

# Validate that both repos exist
if [[ ! -d "$PROJECT_REPO/prds" ]]; then
  echo "Error: Could not find project repo at $PROJECT_REPO"
  exit 1
fi
if [[ ! -d "$REPO_ROOT/src" ]]; then
  echo "Error: Could not find SaaS repo at $REPO_ROOT"
  exit 1
fi

WORKTREE_BASE="$PARENT_DIR/chat_to_map_worktrees"
WORKTREE_PATH="$WORKTREE_BASE/$BRANCH"
DESKTOP_REPO="git@github.com:DocSpring/chat_to_map_desktop.git"

# Check if this is an update to existing worktree
IS_UPDATE=false
if [[ -d "$WORKTREE_PATH" ]]; then
  IS_UPDATE=true
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║  Updating existing worktree: $BRANCH"
  echo "╚════════════════════════════════════════════════════════════╝"
else
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║  Setting up worktree: $BRANCH"
  echo "╚════════════════════════════════════════════════════════════╝"
fi
echo ""
echo "  Worktree path:  $WORKTREE_PATH"
echo "  Project repo:   $PROJECT_REPO"
echo ""

# Create worktrees directory if needed
mkdir -p "$WORKTREE_BASE"

# Step 1: Create worktree (skip if exists)
echo "┌─────────────────────────────────────────────────────────────"
echo "│ Step 1/6: Git worktree"
echo "└─────────────────────────────────────────────────────────────"
# Run git commands from SaaS repo
cd "$REPO_ROOT"
if [[ "$IS_UPDATE" == "true" ]]; then
  echo "  ✓ Worktree already exists, skipping"
else
  if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    echo "  Branch '$BRANCH' exists, creating worktree..."
    git worktree add "$WORKTREE_PATH" "$BRANCH"
  else
    echo "  Branch '$BRANCH' does not exist, creating new branch..."
    git worktree add -b "$BRANCH" "$WORKTREE_PATH"
  fi
fi
echo ""

# Step 2: Set up project symlink
echo "┌─────────────────────────────────────────────────────────────"
echo "│ Step 2/6: Project symlink"
echo "└─────────────────────────────────────────────────────────────"

# Remove old project_notes symlink if it exists (migration)
if [[ -L "$WORKTREE_PATH/project_notes" ]]; then
  rm "$WORKTREE_PATH/project_notes"
  echo "  ✓ Removed old project_notes symlink"
fi

# project symlink
if [[ -L "$WORKTREE_PATH/project" ]]; then
  echo "  ✓ project/ symlink exists"
else
  rm -rf "$WORKTREE_PATH/project" 2>/dev/null || true
  ln -s "../../chat_to_map_project" "$WORKTREE_PATH/project"
  echo "  ✓ project/ symlink created"
fi

# Remove old TODO.md symlink if it exists (no longer needed - edit project/TODO.md directly)
if [[ -L "$WORKTREE_PATH/TODO.md" ]]; then
  rm "$WORKTREE_PATH/TODO.md"
  echo "  ✓ Removed old TODO.md symlink (edit project/TODO.md directly)"
fi

# CLAUDE.md is tracked in git as a symlink - it should already exist
if [[ -L "$WORKTREE_PATH/CLAUDE.md" ]]; then
  echo "  ✓ CLAUDE.md symlink exists (from git)"
else
  echo "  ⚠ Warning: CLAUDE.md missing - should be tracked in git"
fi

# Verify
if [[ -f "$WORKTREE_PATH/project/prds/main.md" ]]; then
  echo "  ✓ Project symlink verified"
else
  echo "  ⚠ Warning: Could not verify project symlink"
fi
echo ""

# Step 3: Initialize submodules
echo "┌─────────────────────────────────────────────────────────────"
echo "│ Step 3/6: Git submodules"
echo "└─────────────────────────────────────────────────────────────"
if [[ -d "$WORKTREE_PATH/chat_to_map/.git" ]] || [[ -f "$WORKTREE_PATH/chat_to_map/.git" ]]; then
  echo "  ✓ Submodules already initialized"
else
  cd "$WORKTREE_PATH"
  git submodule update --init --recursive
  echo "  ✓ Submodules initialized"
fi
echo ""

# Step 4: Clone desktop app repo
echo "┌─────────────────────────────────────────────────────────────"
echo "│ Step 4/6: Desktop app repo"
echo "└─────────────────────────────────────────────────────────────"
if [[ -d "$WORKTREE_PATH/chat_to_map_desktop/.git" ]]; then
  echo "  ✓ Desktop repo already cloned"
else
  rm -rf "$WORKTREE_PATH/chat_to_map_desktop" 2>/dev/null || true
  if git ls-remote "$DESKTOP_REPO" &>/dev/null; then
    git clone "$DESKTOP_REPO" "$WORKTREE_PATH/chat_to_map_desktop"
    echo "  ✓ Desktop repo cloned"
  else
    echo "  ⚠ Desktop repo not accessible, creating placeholder"
    mkdir -p "$WORKTREE_PATH/chat_to_map_desktop"
  fi
fi
echo ""

# Step 5: Copy .env file from main repo
echo "┌─────────────────────────────────────────────────────────────"
echo "│ Step 5/6: Environment file"
echo "└─────────────────────────────────────────────────────────────"
if [[ -f "$WORKTREE_PATH/.env" ]]; then
  echo "  ✓ .env already exists"
elif [[ -f "$REPO_ROOT/.env" ]]; then
  cp "$REPO_ROOT/.env" "$WORKTREE_PATH/.env"
  echo "  ✓ Copied .env from main repo"
else
  echo "  ⚠ No .env found in main repo to copy"
fi
echo ""

# Step 6: Create feedback directory for this branch
echo "┌─────────────────────────────────────────────────────────────"
echo "│ Step 6/6: Feedback directory"
echo "└─────────────────────────────────────────────────────────────"
# Use absolute PROJECT_REPO path, not the symlink in the worktree
if [[ -d "$PROJECT_REPO/feedback/$BRANCH" ]]; then
  echo "  ✓ Feedback directory already exists"
else
  mkdir -p "$PROJECT_REPO/feedback/$BRANCH"
  echo "  ✓ Created feedback/$BRANCH/"
fi
echo ""

# Done!
echo "╔════════════════════════════════════════════════════════════╗"
if [[ "$IS_UPDATE" == "true" ]]; then
  echo "║  ✅ Worktree updated!"
else
  echo "║  ✅ Worktree ready!"
fi
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Contents:"
echo "  CLAUDE.md           → Tracked symlink to project/CHAT_TO_MAP_CLAUDE.md"
echo "  project/            → Symlink to shared project repo"
echo "  chat_to_map/        → Core library (submodule)"
echo "  chat_to_map_desktop/→ Desktop app (clone)"
echo "  src/                → SaaS code"
echo ""
echo "To start working:"
echo "  cd $WORKTREE_PATH"
echo ""
echo "When done:"
echo "  git worktree remove $WORKTREE_PATH"
echo "  git branch -d $BRANCH  # if merging to main"
echo "  git branch -D $BRANCH  # if deleting without merge"
