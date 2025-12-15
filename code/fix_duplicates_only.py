#!/usr/bin/env python3
"""
Simple fix: Just remove duplicate character consistency blocks from pages.
Keep the existing structure but remove duplication.
"""

import glob
import re

def remove_duplicates(file_path):
    """Remove duplicate character consistency blocks."""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove duplicate character consistency blocks
    # Keep only the first occurrence
    lines = content.split('\n')
    new_lines = []
    seen_consistency_block = False
    skip_until_empty = False
    
    for line in lines:
        if line.startswith("**CRITICAL CHARACTER CONSISTENCY"):
            if not seen_consistency_block:
                # Keep the first one
                new_lines.append(line)
                seen_consistency_block = True
                skip_until_empty = False
            else:
                # Skip subsequent ones
                skip_until_empty = True
                continue
        elif skip_until_empty:
            # Skip lines until we hit an empty line or new section
            if line.strip() == "" or line.startswith("##") or line.startswith("Create a modern 2D"):
                skip_until_empty = False
                if line.strip():
                    new_lines.append(line)
            continue
        else:
            new_lines.append(line)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"  ✅ Removed duplicates from {file_path}")

def main():
    print("🧹 Removing duplicate character blocks...")
    
    # Skip page-02.md since user already fixed it
    page_files = [f for f in glob.glob("page-prompts/page-*.md") if not f.endswith("page-02.md")]
    
    print(f"📄 Found {len(page_files)} page files to fix")
    
    for page_file in sorted(page_files):
        try:
            remove_duplicates(page_file)
        except Exception as e:
            print(f"❌ Error fixing {page_file}: {e}")
    
    print(f"\n✅ Done! Removed duplicate blocks from all files.")

if __name__ == "__main__":
    main()