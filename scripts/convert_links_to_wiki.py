import os
import re

# Directories to process
TARGET_DIRS = [
    'research', 'project_docs', 'prds', 'feedback', 'handoffs',
    'todo', 'design', 'experiments', 'qa', 'user_stories'
]

# Regex for standard markdown links: [text](path)
# We avoid matching images ![text](path) by using a negative lookbehind, or just processing them carefully.
# Standard link: (?<!!)\[(.*?)\]\((.*?)\)
LINK_PATTERN = re.compile(r'(?<!!)\[(.*?)\]\((.*?)\)')

def convert_link(match):
    text = match.group(1)
    path = match.group(2)
    
    # Ignore external links
    if path.startswith('http://') or path.startswith('https://') or path.startswith('mailto:'):
        return match.group(0)
    
    # Ignore anchor links within same page
    if path.startswith('#'):
        return match.group(0)

    # Clean path (remove ./ at start)
    clean_path = path
    if clean_path.startswith('./'):
        clean_path = clean_path[2:]
        
    # Construct WikiLink
    # Case 1: [[path]] if text is same as path
    if text == path or text == clean_path:
        return f'[[{clean_path}]]'
    
    # Case 2: [[path|text]] otherwise
    return f'[[{clean_path}|{text}]]'

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = LINK_PATTERN.sub(convert_link, content)
        
        if new_content != content:
            print(f"Updating: {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root_dir = os.getcwd()
    
    for folder in TARGET_DIRS:
        folder_path = os.path.join(root_dir, folder)
        if not os.path.exists(folder_path):
            continue
            
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.md'):
                    process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
