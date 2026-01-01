#!/usr/bin/env python3
import os
import re

def check_archived_todos():
    archive_dir = 'todo/archive'
    stale_items = {}
    
    if not os.path.exists(archive_dir):
        return stale_items

    for file in os.listdir(archive_dir):
        if file.endswith('.md'):
            path = os.path.join(archive_dir, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Find unchecked items
            unchecked = re.findall(r'- [ ].+', content)
            if unchecked:
                stale_items[file] = [item.strip() for item in unchecked]
                    
    return stale_items

def main():
    print("# Stale TODO Items (in Archived Phases)\n")
    
    stale = check_archived_todos()
    if not stale:
        print("No stale items found in archived phases! All tasks completed.")
        return

    for file, items in sorted(stale.items()):
        print(f"## {file}")
        for item in items:
            print(f"{item}")
        print()

if __name__ == "__main__":
    main()

