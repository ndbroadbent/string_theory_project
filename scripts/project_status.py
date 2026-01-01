#!/usr/bin/env python3
import os
import re
import sys

def get_todos():
    # Assume script is run from project root, look for 'todo' dir
    todo_dir = 'todo'
    if not os.path.isdir(todo_dir):
        # Fallback: if run from inside scripts/ dir
        if os.path.isdir('../todo'):
            todo_dir = '../todo'
        else:
            print(f"Error: Could not find 'todo' directory from {os.getcwd()}")
            sys.exit(1)

    status_summary = {}
    
    # Regex to match "- [ ]", "* [ ]", "- [x]", "- [X]"
    # \s* matches optional leading whitespace
    # [-\*] matches bullet
    # \s+ matches space between bullet and box
    re_checked = re.compile(r'^\s*[-\*]\s+\[[xX]\]', re.MULTILINE)
    re_unchecked = re.compile(r'^\s*[-\*]\s+\[ \]', re.MULTILINE)

    for root, dirs, files in os.walk(todo_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Skipping {path}: {e}")
                    continue
                    
                checked = len(re_checked.findall(content))
                unchecked = len(re_unchecked.findall(content))
                total = checked + unchecked
                
                if total > 0:
                    percent = (checked / total) * 100
                    # Clean up path for display
                    if todo_dir.startswith('..'):
                         rel_path = os.path.relpath(path, '../todo')
                    else:
                         rel_path = os.path.relpath(path, todo_dir)
                         
                    status_summary[rel_path] = {
                        'checked': checked,
                        'total': total,
                        'percent': percent
                    }
                    
    return status_summary

def main():
    status = get_todos()
    
    if not status:
        print("No TODOs found (checked for '- [ ]' or '- [x]' in todo/ directory).")
        return

    print("# Project Status Summary\n")
    print(f"{ 'Todo File':<50} | { 'Progress':<10} | {'Done %'}")
    print("-" * 75)
    
    for file, data in sorted(status.items(), key=lambda x: x[1]['percent'], reverse=True):
        progress = f"{data['checked']}/{data['total']}"
        print(f"{file:<50} | {progress:<10} | {data['percent']:>5.1f}%")

if __name__ == "__main__":
    main()

