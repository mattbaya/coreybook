#!/usr/bin/env python3
"""
Remove negative prompts from all Leonardo files.
"""

import os
import glob
from pathlib import Path

def remove_negative_prompt(file_path):
    """Remove negative prompt section from a Leonardo file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    updated_lines = []
    
    skip_negative = False
    for line in lines:
        if line.strip() == "[NEGATIVE PROMPT]":
            skip_negative = True
            continue
        elif line.strip().startswith("[") and skip_negative:
            # Found a new section after negative prompt
            skip_negative = False
            updated_lines.append(line)
        elif not skip_negative:
            updated_lines.append(line)
    
    # Remove trailing empty lines
    while updated_lines and not updated_lines[-1].strip():
        updated_lines.pop()
    
    # Write updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines) + '\n')
    
    return True

def main():
    """Remove negative prompts from all Leonardo files."""
    leonardo_files = glob.glob("leonardo/page-*-leonardo.txt")
    
    print(f"📁 Found {len(leonardo_files)} Leonardo files to update")
    
    updated_count = 0
    for file_path in leonardo_files:
        try:
            remove_negative_prompt(file_path)
            print(f"✅ Removed negative prompt from {file_path}")
            updated_count += 1
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    print(f"\n📊 Summary: Updated {updated_count}/{len(leonardo_files)} files")

if __name__ == "__main__":
    main()