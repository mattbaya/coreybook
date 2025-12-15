#!/usr/bin/env python3
"""
Add square image format requirement to all prompt files.
"""

import os
import glob
from pathlib import Path

def add_square_format_to_file(file_path):
    """Add square format requirement to a prompt file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has square format requirement
    if "**IMAGE FORMAT**: Generate as a SQUARE image" in content:
        return False
    
    # Add square format requirement at the end, before any existing visual requirements
    square_requirement = "\n\n**IMAGE FORMAT**: Generate as a SQUARE image (1:1 aspect ratio)."
    
    # Insert before existing visual requirements if they exist
    if "**IMPORTANT VISUAL REQUIREMENT**" in content:
        content = content.replace(
            "**IMPORTANT VISUAL REQUIREMENT**", 
            square_requirement + "\n\n**IMPORTANT VISUAL REQUIREMENT**"
        )
    else:
        # Add at the end
        content += square_requirement
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    # Process main page prompts
    page_files = glob.glob("page-prompts/page-*.md")
    updated_count = 0
    
    print(f"Updating {len(page_files)} main page prompt files...")
    for file_path in page_files:
        if add_square_format_to_file(file_path):
            updated_count += 1
            print(f"  ✅ Updated {os.path.basename(file_path)}")
    
    # Process Leonardo files
    leonardo_files = glob.glob("leonardo/page-*-leonardo.txt")
    leonardo_updated = 0
    
    print(f"\nUpdating {len(leonardo_files)} Leonardo prompt files...")
    for file_path in leonardo_files:
        if add_square_format_to_file(file_path):
            leonardo_updated += 1
            print(f"  ✅ Updated {os.path.basename(file_path)}")
    
    print(f"\n📊 Summary:")
    print(f"   Main files updated: {updated_count}/{len(page_files)}")
    print(f"   Leonardo files updated: {leonardo_updated}/{len(leonardo_files)}")
    print(f"   Total updated: {updated_count + leonardo_updated}")

if __name__ == "__main__":
    main()