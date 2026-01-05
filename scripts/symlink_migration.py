import os
import filecmp

SOURCE_REPO = "/Users/ndbroadbent/code/string_theory"
PROJECT_REPO = "/Users/ndbroadbent/code/string_theory_project"

# Mappings: Source Dir -> Project Target Dir
MAPPINGS = {
    "docs": "research",
    "plans": "project_docs/plans",
    "research": "research",
    "resources": "research/papers",
}

def link_files():
    for source_sub, project_sub in MAPPINGS.items():
        source_dir = os.path.join(SOURCE_REPO, source_sub)
        project_dir = os.path.join(PROJECT_REPO, project_sub)
        
        if not os.path.exists(source_dir):
            continue
            
        for filename in os.listdir(source_dir):
            source_path = os.path.join(source_dir, filename)
            
            # Skip directories and DS_Store
            if os.path.isdir(source_path) or filename == ".DS_Store":
                continue
                
            # Skip .dat, .json, .txt in resources (keep data local)
            if source_sub == "resources" and filename.endswith((".dat", ".json", ".txt")):
                continue
                
            # Search for the file in the project repo (recursive search might be needed if I reorganized)
            # For now, check direct mapping
            target_path = os.path.join(project_dir, filename)
            
            # Special case for docs -> research (flat copy)
            if not os.path.exists(target_path):
                # Try finding it recursively in project repo
                found = False
                for root, _, files in os.walk(PROJECT_REPO):
                    if filename in files:
                        target_path = os.path.join(root, filename)
                        found = True
                        break
                if not found:
                    print(f"Skipping {filename}: Not found in project repo")
                    continue

            # Check if source is already a symlink
            if os.path.islink(source_path):
                print(f"Skipping {filename}: Already a symlink")
                continue

            # Replace with symlink
            print(f"Linking {filename} -> {target_path}")
            os.remove(source_path)
            # Create relative symlink if possible, or absolute
            # os.symlink(target_path, source_path)
            # Use relative path for portability? No, separate repos. Use absolute for now.
            os.symlink(target_path, source_path)

if __name__ == "__main__":
    link_files()
