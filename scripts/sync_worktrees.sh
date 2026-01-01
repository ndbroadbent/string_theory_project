#!/usr/bin/env bash
set -euo pipefail

# Sync all worktrees back to main branch
#
# For each worktree (in alphabetical order):
#   1. Skip if untracked/unstaged files exist (in-progress work)
#   2. Rebase worktree branch onto main
#   3. Fast-forward main to include worktree changes
#   4. Stop on any conflicts for manual resolution
#
# Usage: ./scripts/sync_worktrees.sh [--dry-run]
#
# Options:
#   --dry-run    Show what would happen without making changes
#   --help       Show this help message

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DRY_RUN=false

# Parse args
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--dry-run]"
      echo ""
      echo "Sync all worktrees back to main branch."
      echo ""
      echo "For each worktree (alphabetically):"
      echo "  1. Skip if has untracked/unstaged files"
      echo "  2. Rebase onto main"
      echo "  3. Fast-forward main to worktree"
      echo ""
      echo "Options:"
      echo "  --dry-run    Show what would happen without changes"
      echo "  --help       Show this message"
      exit 0
      ;;
  esac
done

# Resolve paths relative to this project repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_REPO="${SCRIPT_DIR%/scripts}"
CODE_DIR="$(dirname "$PROJECT_REPO")"

# Repository locations
# Structure: Main saas repo + worktrees, each with their own submodule copies
#
# ~/code/
# ├── chat_to_map_saas/           # Main repo
# │   ├── chat_to_map/            # Core library (SUBMODULE - pinned version)
# │   └── chat_to_map_desktop/    # Desktop app (regular clone, NOT a submodule)
# ├── chat_to_map_worktrees/
# │   ├── <branch>/               # Each worktree has isolated copies
# │   │   ├── chat_to_map/        # Its own submodule copy
# │   │   └── chat_to_map_desktop/# Its own clone
# │   └── ...
# └── chat_to_map_project/        # Shared docs (symlinked)
#
# SUBMODULE NOTE:
# - chat_to_map is a SUBMODULE (saas pins a specific version of core library)
# - chat_to_map_desktop is NOT a submodule (saas doesn't depend on desktop app)
# - "modified: chat_to_map (new commits)" is EXPECTED and IGNORED by this script
#   This means core library work happened in that worktree but the saas repo
#   hasn't pinned the new commits yet. That's fine - we only care about saas changes.
#
SAAS_REPO="$CODE_DIR/chat_to_map_saas"
WORKTREE_BASE="$CODE_DIR/chat_to_map_worktrees"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ChatToMap Worktree Sync                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
  echo -e "${YELLOW}DRY RUN MODE - no changes will be made${NC}"
  echo ""
fi

# Check if a git repo is clean (no untracked or unstaged files)
# Ignores submodule pointer changes (e.g., "modified: chat_to_map (new commits)")
is_repo_clean() {
  local repo_path="$1"
  if [[ ! -d "$repo_path/.git" ]] && [[ ! -f "$repo_path/.git" ]]; then
    return 1  # Not a git repo
  fi

  cd "$repo_path"

  # Check for uncommitted changes (staged or unstaged)
  # --ignore-submodules: ignore "modified: chat_to_map (new commits)"
  # This is expected when core library work happened but wasn't pinned in saas yet
  if ! git diff --quiet --ignore-submodules 2>/dev/null; then
    return 1
  fi

  # Check for staged changes (also ignore submodule pointer changes)
  if ! git diff --cached --quiet --ignore-submodules 2>/dev/null; then
    return 1
  fi

  # Check for untracked files
  if [[ -n "$(git ls-files --others --exclude-standard 2>/dev/null)" ]]; then
    return 1
  fi

  return 0
}

# Get current branch name
get_branch() {
  git rev-parse --abbrev-ref HEAD 2>/dev/null
}

# Get commit count ahead of main
commits_ahead() {
  git rev-list --count main..HEAD 2>/dev/null || echo "0"
}

# Get commit count behind main
commits_behind() {
  git rev-list --count HEAD..main 2>/dev/null || echo "0"
}

# Sync a single repo's worktrees
sync_repo_worktrees() {
  local main_repo="$1"
  local repo_name="$2"

  echo "┌─────────────────────────────────────────────────────────────"
  echo "│ Syncing: $repo_name"
  echo "└─────────────────────────────────────────────────────────────"

  if [[ ! -d "$main_repo" ]]; then
    echo -e "  ${YELLOW}⚠ Repository not found: $main_repo${NC}"
    echo ""
    return 0
  fi

  cd "$main_repo"

  # Check if main repo is clean
  if ! is_repo_clean "$main_repo"; then
    echo -e "  ${YELLOW}⚠ Main repo has uncommitted changes, skipping${NC}"
    echo ""
    return 0
  fi

  # Get list of worktrees (excluding main)
  local worktrees
  worktrees=$(git worktree list --porcelain | grep "^worktree " | sed 's/^worktree //' | sort)

  local synced=0
  local skipped=0

  # Process worktrees (use process substitution to avoid subshell)
  while IFS= read -r worktree_path; do
    [[ -z "$worktree_path" ]] && continue
    [[ "$worktree_path" == "$main_repo" ]] && continue

    local branch_name
    branch_name=$(basename "$worktree_path")

    echo ""
    echo -e "  ${BLUE}▶ $branch_name${NC}"

    # Check if worktree is clean
    if ! is_repo_clean "$worktree_path"; then
      echo -e "    ${YELLOW}↳ Skipping (has uncommitted changes)${NC}"
      skipped=$((skipped + 1))
      continue
    fi

    cd "$worktree_path"

    local ahead behind
    ahead=$(commits_ahead)
    behind=$(commits_behind)

    if [[ "$ahead" == "0" ]] && [[ "$behind" == "0" ]]; then
      echo "    ↳ Already up to date with main"
      continue
    fi

    # Show status
    if [[ "$ahead" != "0" ]] && [[ "$behind" != "0" ]]; then
      echo "    ↳ $ahead ahead, $behind behind main"
    elif [[ "$ahead" != "0" ]]; then
      echo "    ↳ $ahead commit(s) ahead of main"
    else
      echo "    ↳ $behind commit(s) behind main"
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
      if [[ "$ahead" != "0" ]]; then
        echo -e "    ${BLUE}↳ Would rebase onto main and fast-forward${NC}"
      else
        echo -e "    ${BLUE}↳ Would rebase onto main${NC}"
      fi
      synced=$((synced + 1))
      SYNCED_THIS_PASS=$((SYNCED_THIS_PASS + 1))
      continue
    fi

    # If worktree is behind main, just fast-forward the worktree
    if [[ "$ahead" == "0" ]] && [[ "$behind" != "0" ]]; then
      echo "    ↳ Fast-forwarding worktree to main..."
      if ! git merge --ff-only main; then
        echo "    ↳ Can't fast-forward, resetting to main..."
        git reset --hard main
      fi
      echo -e "    ${GREEN}✓ Synced${NC}"
      synced=$((synced + 1))
      SYNCED_THIS_PASS=$((SYNCED_THIS_PASS + 1))
      continue
    fi

    # Worktree has commits ahead of main - need to rebase and merge
    echo "    ↳ Rebasing onto main..."
    if ! git rebase main; then
      echo -e "    ${RED}✗ Rebase failed! Resolve conflicts and run again.${NC}"
      echo ""
      echo "  To continue manually:"
      echo "    cd $worktree_path"
      echo "    # resolve conflicts"
      echo "    git rebase --continue"
      echo ""
      exit 1
    fi

    # Fast-forward main to include the rebased commits
    cd "$main_repo"
    echo "    ↳ Fast-forwarding main..."
    if ! git merge --ff-only "$branch_name"; then
      echo -e "    ${RED}✗ Fast-forward failed!${NC}"
      echo ""
      exit 1
    fi

    # Now reset the worktree branch to match main exactly
    # This ensures next run sees them as identical
    cd "$worktree_path"
    git reset --hard main

    echo -e "    ${GREEN}✓ Synced${NC}"
    synced=$((synced + 1))
    SYNCED_THIS_PASS=$((SYNCED_THIS_PASS + 1))

  done <<< "$worktrees"

  echo ""
  echo "  Summary: $synced synced, $skipped skipped"
  echo ""
}

# Sync submodules across worktrees (set up local remotes)
setup_submodule_remotes() {
  local submodule_name="$1"
  local main_submodule="$2"

  echo "┌─────────────────────────────────────────────────────────────"
  echo "│ Setting up local remotes for: $submodule_name"
  echo "└─────────────────────────────────────────────────────────────"

  if [[ ! -d "$main_submodule/.git" ]] && [[ ! -f "$main_submodule/.git" ]]; then
    echo -e "  ${YELLOW}⚠ Submodule not found: $main_submodule${NC}"
    echo ""
    return 0
  fi

  # Find all worktree copies of this submodule
  local worktree_submodules=()
  if [[ -d "$WORKTREE_BASE" ]]; then
    for worktree in "$WORKTREE_BASE"/*/; do
      local submodule_path="$worktree$submodule_name"
      if [[ -d "$submodule_path/.git" ]] || [[ -f "$submodule_path/.git" ]]; then
        worktree_submodules+=("$submodule_path")
      fi
    done
  fi

  if [[ ${#worktree_submodules[@]} -eq 0 ]]; then
    echo "  No worktree copies found"
    echo ""
    return 0
  fi

  cd "$main_submodule"

  # Add remotes for each worktree submodule
  for submodule_path in "${worktree_submodules[@]}"; do
    local worktree_name
    worktree_name=$(basename "$(dirname "$submodule_path")")
    local remote_name="worktree-$worktree_name"

    # Check if remote already exists
    if git remote get-url "$remote_name" &>/dev/null; then
      echo "  ✓ Remote $remote_name already configured"
    else
      if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "  ${BLUE}Would add remote: $remote_name → $submodule_path${NC}"
      else
        git remote add "$remote_name" "$submodule_path"
        echo "  ✓ Added remote: $remote_name"
      fi
    fi
  done

  echo ""
}

# Main execution
echo "Repository locations:"
echo "  SaaS:      $SAAS_REPO"
echo "  Worktrees: $WORKTREE_BASE"
echo ""

# Sync saas repo worktrees (loop until no changes)
if [[ "$DRY_RUN" == "true" ]]; then
  # Dry-run: single pass only
  SYNCED_THIS_PASS=0
  sync_repo_worktrees "$SAAS_REPO" "chat_to_map_saas"
else
  # Real run: loop until no changes
  SYNC_COUNT=0
  while true; do
    SYNC_COUNT=$((SYNC_COUNT + 1))
    if [[ "$SYNC_COUNT" -gt 1 ]]; then
      echo ""
      echo -e "${BLUE}Pass $SYNC_COUNT (catching up after fast-forward)${NC}"
    fi

    SYNCED_THIS_PASS=0
    sync_repo_worktrees "$SAAS_REPO" "chat_to_map_saas"

    # Break if nothing was synced this pass
    if [[ "$SYNCED_THIS_PASS" -eq 0 ]]; then
      break
    fi
  done
fi

# Set up local remotes for submodules across all worktrees
# This lets you fetch commits between worktree submodules directly
setup_submodule_remotes "chat_to_map" "$SAAS_REPO/chat_to_map"
setup_submodule_remotes "chat_to_map_desktop" "$SAAS_REPO/chat_to_map_desktop"

# Sync submodule commits from worktrees back to main repo
sync_submodule_from_worktrees() {
  local submodule_name="$1"
  local main_submodule="$2"

  echo "┌─────────────────────────────────────────────────────────────"
  echo "│ Syncing $submodule_name from worktrees"
  echo "└─────────────────────────────────────────────────────────────"

  if [[ ! -d "$main_submodule/.git" ]] && [[ ! -f "$main_submodule/.git" ]]; then
    echo -e "  ${YELLOW}⚠ Submodule not found: $main_submodule${NC}"
    echo ""
    return 0
  fi

  cd "$main_submodule"

  # Check if main submodule is clean
  if ! is_repo_clean "$main_submodule"; then
    echo -e "  ${YELLOW}⚠ Main submodule has uncommitted changes, skipping${NC}"
    echo ""
    return 0
  fi

  local current_branch
  current_branch=$(get_branch)

  # Find all worktree remotes and sync from them
  local synced=0
  local skipped=0

  for remote in $(git remote | grep "^worktree-"); do
    local worktree_name="${remote#worktree-}"
    local worktree_submodule="$WORKTREE_BASE/$worktree_name/$submodule_name"

    echo ""
    echo -e "  ${BLUE}▶ $worktree_name${NC}"

    # Check if worktree submodule exists and is clean
    if [[ ! -d "$worktree_submodule" ]]; then
      echo "    ↳ Worktree submodule not found, skipping"
      skipped=$((skipped + 1))
      continue
    fi

    if ! is_repo_clean "$worktree_submodule"; then
      echo -e "    ${YELLOW}↳ Skipping (has uncommitted changes)${NC}"
      skipped=$((skipped + 1))
      continue
    fi

    cd "$main_submodule"

    # Check if worktree submodule has any commits
    cd "$worktree_submodule"
    if ! git rev-parse HEAD &>/dev/null; then
      echo "    ↳ No commits in worktree submodule, skipping"
      cd "$main_submodule"
      continue
    fi

    cd "$main_submodule"

    # Fetch from worktree
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "    ↳ Would fetch from $remote"
    else
      echo "    ↳ Fetching from $remote..."
      if ! git fetch "$remote" --quiet 2>/dev/null; then
        echo -e "    ${YELLOW}↳ Fetch failed, skipping${NC}"
        continue
      fi
    fi

    # Get the worktree's current branch
    cd "$worktree_submodule"
    local worktree_branch
    worktree_branch=$(get_branch)

    cd "$main_submodule"

    # Check if we can fast-forward to include worktree commits
    local remote_ref="$remote/$worktree_branch"
    if ! git rev-parse "$remote_ref" &>/dev/null; then
      echo "    ↳ No branch $worktree_branch on remote"
      continue
    fi

    # Check if worktree has commits not in main
    local ahead
    ahead=$(git rev-list --count "$current_branch..$remote_ref" 2>/dev/null || echo "0")

    if [[ "$ahead" == "0" ]]; then
      echo "    ↳ Already up to date"
      continue
    fi

    echo "    ↳ $ahead commit(s) to merge"

    if [[ "$DRY_RUN" == "true" ]]; then
      echo -e "    ${BLUE}↳ Would fast-forward $current_branch${NC}"
      synced=$((synced + 1))
      continue
    fi

    # Try to fast-forward
    if git merge --ff-only "$remote_ref" 2>/dev/null; then
      echo -e "    ${GREEN}✓ Fast-forwarded${NC}"
      synced=$((synced + 1))

      # Update worktree submodule to match main
      local main_head
      main_head=$(git rev-parse HEAD)
      cd "$worktree_submodule"
      git fetch "$main_submodule" --quiet 2>/dev/null || true
      git reset --hard "$main_head"
      cd "$main_submodule"
    else
      # If can't fast-forward, try rebase
      echo "    ↳ Can't fast-forward, attempting rebase..."
      if git rebase "$remote_ref"; then
        echo -e "    ${GREEN}✓ Rebased${NC}"
        synced=$((synced + 1))

        # Update worktree submodule to match main (critical for idempotency)
        local main_head
        main_head=$(git rev-parse HEAD)
        cd "$worktree_submodule"
        git fetch "$main_submodule" --quiet 2>/dev/null || true
        git reset --hard "$main_head"
        cd "$main_submodule"
      else
        echo -e "    ${RED}✗ Rebase failed! Resolve conflicts manually.${NC}"
        git rebase --abort
        echo ""
        echo "  To resolve:"
        echo "    cd $main_submodule"
        echo "    git fetch $remote"
        echo "    git rebase $remote_ref"
        echo ""
        exit 1
      fi
    fi

  done

  echo ""
  echo "  Summary: $synced synced, $skipped skipped"
  echo ""
}

# Sync submodules from worktrees into main
sync_submodule_from_worktrees "chat_to_map" "$SAAS_REPO/chat_to_map"
sync_submodule_from_worktrees "chat_to_map_desktop" "$SAAS_REPO/chat_to_map_desktop"

# Push main submodule state back to all worktrees
sync_submodule_to_worktrees() {
  local submodule_name="$1"
  local main_submodule="$2"

  echo "┌─────────────────────────────────────────────────────────────"
  echo "│ Updating worktrees with $submodule_name"
  echo "└─────────────────────────────────────────────────────────────"

  if [[ ! -d "$main_submodule/.git" ]] && [[ ! -f "$main_submodule/.git" ]]; then
    echo -e "  ${YELLOW}⚠ Submodule not found: $main_submodule${NC}"
    echo ""
    return 0
  fi

  cd "$main_submodule"
  local main_branch
  main_branch=$(get_branch)
  local main_commit
  main_commit=$(git rev-parse HEAD)

  local synced=0
  local skipped=0

  # Update each worktree submodule
  for remote in $(git remote | grep "^worktree-"); do
    local worktree_name="${remote#worktree-}"
    local worktree_submodule="$WORKTREE_BASE/$worktree_name/$submodule_name"

    echo ""
    echo -e "  ${BLUE}▶ $worktree_name${NC}"

    if [[ ! -d "$worktree_submodule" ]]; then
      echo "    ↳ Worktree submodule not found, skipping"
      skipped=$((skipped + 1))
      continue
    fi

    # Check if worktree submodule has any commits
    cd "$worktree_submodule"
    if ! git rev-parse HEAD &>/dev/null; then
      echo "    ↳ No commits in worktree submodule, skipping"
      skipped=$((skipped + 1))
      continue
    fi

    if ! is_repo_clean "$worktree_submodule"; then
      echo -e "    ${YELLOW}↳ Skipping (has uncommitted changes)${NC}"
      skipped=$((skipped + 1))
      continue
    fi

    local worktree_branch
    worktree_branch=$(get_branch)
    local worktree_commit
    worktree_commit=$(git rev-parse HEAD)

    # Already up to date?
    if [[ "$worktree_commit" == "$main_commit" ]]; then
      echo "    ↳ Already up to date"
      continue
    fi

    # Check how far behind
    local behind
    behind=$(git rev-list --count "HEAD..$main_commit" 2>/dev/null || echo "0")

    if [[ "$behind" == "0" ]]; then
      echo "    ↳ Already up to date"
      continue
    fi

    echo "    ↳ $behind commit(s) behind main"

    if [[ "$DRY_RUN" == "true" ]]; then
      echo -e "    ${BLUE}↳ Would fast-forward to main${NC}"
      synced=$((synced + 1))
      continue
    fi

    # Add main submodule as remote if not present
    if ! git remote get-url main-repo &>/dev/null; then
      git remote add main-repo "$main_submodule"
    fi

    # Fetch and fast-forward
    git fetch main-repo --quiet
    if git merge --ff-only "main-repo/$main_branch" 2>/dev/null; then
      echo -e "    ${GREEN}✓ Fast-forwarded${NC}"
      synced=$((synced + 1))
    else
      echo "    ↳ Can't fast-forward, attempting rebase..."
      if git rebase "main-repo/$main_branch"; then
        echo -e "    ${GREEN}✓ Rebased${NC}"
        synced=$((synced + 1))
      else
        echo -e "    ${RED}✗ Rebase failed! Resolve conflicts manually.${NC}"
        git rebase --abort
        skipped=$((skipped + 1))
      fi
    fi

  done

  echo ""
  echo "  Summary: $synced synced, $skipped skipped"
  echo ""
}

# Push main submodule state to all worktrees
sync_submodule_to_worktrees "chat_to_map" "$SAAS_REPO/chat_to_map"
sync_submodule_to_worktrees "chat_to_map_desktop" "$SAAS_REPO/chat_to_map_desktop"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Sync complete                                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
  echo "Run without --dry-run to apply changes."
fi
