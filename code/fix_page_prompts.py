#!/usr/bin/env python3
"""
Fix all page prompts to include consistent character descriptions.
Addresses the issues identified in the comprehensive review.
"""

import os
import glob
from pathlib import Path

# Character consistency block to add to every page
CHARACTER_BLOCK = """
**CRITICAL CHARACTER CONSISTENCY - MUST MATCH EXACTLY:**
- COREY: Completely BALD adult male (no hair), round face, navy blue apron, white shirt
- EMILY: Adult female, short silver pixie hair, black glasses
- REMI: 11-year-old boy, dark curly brown hair, blue Super3 shirt
- OONA: 11-year-old girl, long honey blonde hair, blue Super3 shirt  
- ZEPHYR: 9-year-old girl, light brown shoulder-length hair, blue Super3 shirt
- SUPER3 LOGO: Red diamond shield with yellow "3", letters Z-O-R in corners
- STORE: Cream building with 4 white columns (reference: cartoon-characters/store-cartoon.jpg)
- TOTAL PEOPLE: Maximum 5 (Corey, Emily, Remi, Oona, Zephyr)
"""

def fix_page_prompt(file_path):
    """Fix a single page prompt file."""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    in_image_prompt = False
    character_block_added = False
    
    for line in lines:
        if line.startswith("## IMAGE PROMPT"):
            in_image_prompt = True
            new_lines.append(line)
            # Add character block right after IMAGE PROMPT header
            new_lines.extend(CHARACTER_BLOCK.split('\n'))
            character_block_added = True
            continue
        elif line.startswith("## ") and in_image_prompt:
            in_image_prompt = False
        elif in_image_prompt and not character_block_added:
            # If we're in image prompt section but haven't added block yet
            new_lines.extend(CHARACTER_BLOCK.split('\n'))
            character_block_added = True
        
        # Fix common inconsistencies in existing content
        line = fix_inconsistencies(line)
        new_lines.append(line)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"  ✅ Fixed: {file_path}")

def fix_inconsistencies(line):
    """Fix known inconsistencies in line content."""
    
    # Fix apron color
    line = line.replace("dark olive-green apron", "navy blue apron")
    line = line.replace("olive-green apron", "navy blue apron")
    
    # Fix hair color standardization
    line = line.replace("light brown/honey blonde", "honey blonde")
    line = line.replace("long light brown hair", "long honey blonde hair")
    
    # Fix Super3 logo description
    line = line.replace("Superman-style shield", "red diamond shield with yellow '3'")
    line = line.replace("Superman logo", "Super3 logo: red diamond shield with yellow '3'")
    
    # Ensure Corey is always described as bald
    if "Corey" in line and "hair" in line.lower() and "bald" not in line.lower():
        line = line.replace("Corey", "Corey (completely bald)")
    
    return line

def main():
    print("🔧 Fixing all page prompts for character consistency...")
    
    # Find all page prompt files
    page_files = glob.glob("page-prompts/page-*.md")
    
    if not page_files:
        print("❌ No page prompt files found in page-prompts/")
        return
    
    print(f"📄 Found {len(page_files)} page files to fix")
    
    # Create backup directory
    backup_dir = Path("page-prompts/backup")
    backup_dir.mkdir(exist_ok=True)
    
    fixed_count = 0
    
    for page_file in sorted(page_files):
        try:
            # Create backup
            backup_path = backup_dir / Path(page_file).name
            with open(page_file, 'r') as src, open(backup_path, 'w') as dst:
                dst.write(src.read())
            
            # Fix the file
            fix_page_prompt(page_file)
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error fixing {page_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Fixed: {fixed_count}/{len(page_files)} files")
    print(f"   📁 Backups saved to: {backup_dir}")
    print(f"   🎯 All prompts now include character consistency blocks")
    
    print(f"\n🔄 Next: Re-generate backgrounds with consistent prompts")

if __name__ == "__main__":
    main()