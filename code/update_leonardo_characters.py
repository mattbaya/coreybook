#!/usr/bin/env python3
"""
Update Leonardo prompts with improved character consistency.
"""

import os
import glob
from pathlib import Path

def update_leonardo_file(file_path):
    """Update a single Leonardo file with improved character descriptions."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Character consistency block to add
    character_block = """
CHARACTER CONSISTENCY RULES (CRITICAL):
- COREY: Completely BALD adult male (no hair), round face, navy blue apron, white shirt
- EMILY: Adult female, short silver pixie hair, black glasses
- REMI: 11-year-old CAUCASIAN WHITE BOY, dark brown hair (not curly), pale/white skin, blue Super3 shirt, non-identical twin to Oona
- OONA: 11-year-old CAUCASIAN WHITE GIRL, long honey blonde hair, pale/white skin, blue Super3 shirt, non-identical twin to Remi
- ZEPHYR: 9-year-old CAUCASIAN WHITE GIRL, light brown shoulder-length hair, pale/white skin, blue Super3 shirt, smallest child
- ALL CHILDREN: Caucasian white with pale/light skin tones, family resemblance
- SUPER3 LOGO: Red diamond shield with yellow "3", letters Z-O-R in corners

"""

    # Find the [PROMPT] section and add character consistency after it
    lines = content.split('\n')
    updated_lines = []
    
    for i, line in enumerate(lines):
        updated_lines.append(line)
        if line.strip() == "[PROMPT]":
            # Add character consistency block after [PROMPT]
            updated_lines.append(character_block)
    
    # Write updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines))
    
    return True

def main():
    """Update all Leonardo files."""
    leonardo_files = glob.glob("leonardo/page-*-leonardo.txt")
    
    print(f"📁 Found {len(leonardo_files)} Leonardo files to update")
    
    updated_count = 0
    for file_path in leonardo_files:
        try:
            update_leonardo_file(file_path)
            print(f"✅ Updated {file_path}")
            updated_count += 1
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    print(f"\n📊 Summary: Updated {updated_count}/{len(leonardo_files)} files")

if __name__ == "__main__":
    main()