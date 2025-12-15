#!/usr/bin/env python3
"""
Fix character consistency:
1. Change Remi's hair from "dark curly brown hair" to "dark brown straight hair"
2. Ensure all family members have same skin color (caucasian/white)
"""

import os
import glob
import re
from pathlib import Path

def fix_character_descriptions(file_path):
    """Fix character descriptions in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix Remi's hair description - multiple patterns to catch all variations
    patterns = [
        # Main prompt sections
        (r'REMI: 11-year-old boy, dark curly brown hair, blue Super3 shirt',
         'REMI: 11-year-old CAUCASIAN WHITE boy, dark brown straight hair, blue Super3 shirt'),
        
        # In-text descriptions
        (r'REMI \(dark curly hair, blue Super3',
         'REMI (dark brown straight hair, blue Super3'),
        
        (r'REMI \(dark curly hair\)',
         'REMI (dark brown straight hair)'),
         
        (r'\*\*REMI\*\*: Dark curly hair',
         '**REMI**: Dark brown straight hair'),
         
        # Cover page specific
        (r'\*\*Remi\*\*: Dark curly hair',
         '**Remi**: Dark brown straight hair'),
         
        # Leonardo format - preserve existing good format
        (r'REMI: 11-year-old CAUCASIAN WHITE BOY, dark brown hair \(not curly\)',
         'REMI: 11-year-old CAUCASIAN WHITE BOY, dark brown straight hair'),
         
        # Fix any remaining "curly" mentions for Remi
        (r'Remi.*?curly.*?hair', 'Remi with dark brown straight hair'),
    ]
    
    for old_pattern, new_pattern in patterns:
        content = re.sub(old_pattern, new_pattern, content, flags=re.IGNORECASE)
    
    # Add skin color consistency for main character descriptions
    # This ensures all family members are explicitly described as same ethnicity
    character_updates = [
        # Emily
        (r'EMILY: Adult female, short silver pixie hair, black glasses',
         'EMILY: CAUCASIAN WHITE adult female, short silver pixie hair, black glasses'),
         
        # Oona
        (r'OONA: 11-year-old girl, long honey blonde hair, blue Super3 shirt',
         'OONA: 11-year-old CAUCASIAN WHITE girl, long honey blonde hair, blue Super3 shirt'),
         
        # Zephyr  
        (r'ZEPHYR: 9-year-old girl, light brown shoulder-length hair, blue Super3 shirt',
         'ZEPHYR: 9-year-old CAUCASIAN WHITE girl, light brown shoulder-length hair, blue Super3 shirt'),
         
        # Corey
        (r'COREY: Completely BALD adult male \(no hair\), round face,',
         'COREY: CAUCASIAN WHITE completely BALD adult male (no hair), round face,'),
    ]
    
    # Only update if not already specified
    for old_pattern, new_pattern in character_updates:
        if 'CAUCASIAN WHITE' not in content or old_pattern in content:
            content = re.sub(old_pattern, new_pattern, content)
    
    # Add family consistency note if it's a main prompt file and doesn't have it
    if file_path.endswith('.md') and 'FAMILY CONSISTENCY NOTE' not in content:
        # Find where to insert - after character consistency rules
        consistency_insert = """

**FAMILY CONSISTENCY NOTE**: All family members (Corey, Emily, Remi, Oona, and Zephyr) are CAUCASIAN WHITE with the same light/pale skin tone. This is a white American family."""
        
        # Insert after the character list but before the scene description
        if 'TOTAL PEOPLE: Maximum 5' in content:
            content = content.replace(
                'TOTAL PEOPLE: Maximum 5 (Corey, Emily, Remi, Oona, Zephyr)',
                'TOTAL PEOPLE: Maximum 5 (Corey, Emily, Remi, Oona, Zephyr)' + consistency_insert
            )
    
    # Only write if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # Process main page prompts
    page_files = glob.glob("page-prompts/page-*.md")
    updated_count = 0
    
    print(f"Fixing character consistency in {len(page_files)} main page prompt files...")
    for file_path in sorted(page_files):
        if fix_character_descriptions(file_path):
            updated_count += 1
            print(f"  ✅ Fixed {os.path.basename(file_path)}")
    
    # Process Leonardo files
    leonardo_files = glob.glob("leonardo/page-*-leonardo.txt")
    leonardo_updated = 0
    
    print(f"\nFixing character consistency in {len(leonardo_files)} Leonardo prompt files...")
    for file_path in sorted(leonardo_files):
        if fix_character_descriptions(file_path):
            leonardo_updated += 1
            print(f"  ✅ Fixed {os.path.basename(file_path)}")
    
    # Also update generate_images.py if needed
    gen_file = "generate_images.py"
    if os.path.exists(gen_file):
        print(f"\nChecking {gen_file}...")
        if fix_character_descriptions(gen_file):
            print(f"  ✅ Fixed {gen_file}")
    
    print(f"\n📊 Summary:")
    print(f"   Main files updated: {updated_count}/{len(page_files)}")
    print(f"   Leonardo files updated: {leonardo_updated}/{len(leonardo_files)}")
    print(f"   Total updated: {updated_count + leonardo_updated}")

if __name__ == "__main__":
    main()