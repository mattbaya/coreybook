#!/usr/bin/env python3
"""
Add eyeball requirement to all prompts - both main and Leonardo files.
"""

import os
import glob
from pathlib import Path

def update_main_prompt_file(file_path):
    """Update a main page prompt file with eyeball requirement."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add eyeball requirement to the Art Style section or create one
        eyeball_requirement = "\n\n**IMPORTANT VISUAL REQUIREMENT**: All characters must have expressive, detailed eyeballs - never just dots for eyes. Eyes should be large, expressive, and clearly defined with pupils and emotional detail."
        
        # Look for existing Art Style section
        if "**Art Style**:" in content:
            # Add before the Art Style section
            content = content.replace("**Art Style**:", f"{eyeball_requirement}\n\n**Art Style**:")
        else:
            # Add at the end of the file
            content = content.rstrip() + eyeball_requirement + "\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def update_leonardo_file(file_path):
    """Update a Leonardo file with eyeball requirement."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add eyeball requirement before the last line or at end
        eyeball_requirement = "\n\nIMPORTANT VISUAL REQUIREMENT: All characters must have expressive, detailed eyeballs - never just dots for eyes. Eyes should be large, expressive, and clearly defined with pupils and emotional detail."
        
        # Add at the end
        content = content.rstrip() + eyeball_requirement + "\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update all prompt files with eyeball requirements."""
    
    print("👁️ ADDING EYEBALL REQUIREMENTS TO ALL PROMPTS")
    print("=" * 50)
    
    # Update main prompt files
    print("\n📄 Updating main prompt files...")
    main_files = sorted(glob.glob("page-prompts/page-*.md"))
    main_updated = 0
    
    for file_path in main_files:
        if update_main_prompt_file(file_path):
            print(f"✅ Updated {Path(file_path).name}")
            main_updated += 1
        else:
            print(f"❌ Failed to update {Path(file_path).name}")
    
    # Update Leonardo files
    print("\n📄 Updating Leonardo files...")
    leonardo_files = sorted(glob.glob("leonardo/page-*-leonardo.txt"))
    leonardo_updated = 0
    
    for file_path in leonardo_files:
        if update_leonardo_file(file_path):
            print(f"✅ Updated {Path(file_path).name}")
            leonardo_updated += 1
        else:
            print(f"❌ Failed to update {Path(file_path).name}")
    
    print(f"\n📊 SUMMARY:")
    print(f"Main prompts updated: {main_updated}/{len(main_files)}")
    print(f"Leonardo files updated: {leonardo_updated}/{len(leonardo_files)}")
    print(f"Total files updated: {main_updated + leonardo_updated}")
    
    print(f"\n👁️ All prompts now require expressive eyeballs, never dots!")

if __name__ == "__main__":
    main()