#!/usr/bin/env bash
set -euo pipefail

# Renumber feedback files in each category directory to close gaps
# Usage: ./scripts/renumber_feedback.sh [--dry-run]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FEEDBACK_DIR="$PROJECT_ROOT/feedback"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "=== DRY RUN MODE ==="
  echo
fi

# Track all renames for sed replacement
declare -A RENAMES=()
RENAME_COUNT=0

renumber_category() {
  local category_dir="$1"
  local category_name
  category_name="$(basename "$category_dir")"

  # Skip if not a directory
  [[ -d "$category_dir" ]] || return 0

  # Get all numbered files (NNN_*.md pattern), excluding FEEDBACK* legacy files
  local files=()
  while IFS= read -r -d '' file; do
    files+=("$file")
  done < <(find "$category_dir" -maxdepth 1 -type f -name '[0-9][0-9][0-9]_*.md' -print0 2>/dev/null | sort -z)

  [[ ${#files[@]} -eq 0 ]] && return 0

  local new_num=1
  for file in "${files[@]}"; do
    local basename
    basename="$(basename "$file")"
    local suffix="${basename:3}"  # Everything after NNN
    local new_num_padded
    new_num_padded=$(printf "%03d" "$new_num")
    local new_basename="${new_num_padded}${suffix}"

    if [[ "$basename" != "$new_basename" ]]; then
      local old_path="$category_name/$basename"
      local new_path="$category_name/$new_basename"

      echo "Rename: $old_path -> $new_path"
      RENAMES["$old_path"]="$new_path"
      ((RENAME_COUNT++))

      if [[ "$DRY_RUN" == "false" ]]; then
        mv "$file" "$category_dir/$new_basename"
      fi
    fi

    ((new_num++))
  done
}

# Process each category directory
echo "=== Renumbering feedback files ==="
echo

for dir in "$FEEDBACK_DIR"/*/; do
  [[ -d "$dir" ]] || continue
  # Skip archive directories
  [[ "$(basename "$dir")" == "archive" ]] && continue
  renumber_category "$dir"
done

echo

# If we have renames, update references across all text files
if [[ "$RENAME_COUNT" -gt 0 ]]; then
  echo "=== Updating references in text files ==="
  echo

  for old_path in "${!RENAMES[@]}"; do
    new_path="${RENAMES[$old_path]}"

    # Use rg for fast searching, then sed only on matching files
    matching_files=$(rg -l --type md --type txt --type sh -F "$old_path" "$PROJECT_ROOT" 2>/dev/null || true)

    if [[ -n "$matching_files" ]]; then
      while IFS= read -r file; do
        if [[ "$DRY_RUN" == "false" ]]; then
          echo "  Updating reference in: $file"
          sed -i '' "s|$old_path|$new_path|g" "$file"
        else
          echo "  Would update in: $file"
          rg -F "$old_path" "$file" | head -3
        fi
      done <<< "$matching_files"
    fi
  done

  echo
  echo "=== Checking for orphaned partial references ==="
  echo

  # Check for partial matches that might be out of sync
  for old_path in "${!RENAMES[@]}"; do
    # Extract just the suffix part (e.g., "_message_context_copy.md")
    suffix="${old_path#*/[0-9][0-9][0-9]}"
    new_path="${RENAMES[$old_path]}"

    # Use rg for fast searching
    matching_files=$(rg -l --type md --type txt --type sh -F "$suffix" "$PROJECT_ROOT" 2>/dev/null || true)

    if [[ -n "$matching_files" ]]; then
      while IFS= read -r file; do
        # Check if file contains a numbered reference that's not the new path
        if rg -q "[0-9]{3}$suffix" "$file" 2>/dev/null; then
          if ! rg -qF "$new_path" "$file" 2>/dev/null; then
            echo "WARNING: found '...$suffix' in $file that may be out of sync. Check manually."
          fi
        fi
      done <<< "$matching_files"
    fi
  done
fi

echo
echo "=== Done ==="
