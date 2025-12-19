#!/usr/bin/env python3
"""
Update page prompts to match the new page numbering with text splits.
"""

import os
from pathlib import Path
import shutil

def update_main_prompts():
    """Update the main page-prompts folder."""
    print("Updating main page prompts...")
    
    # Create backup
    backup_dir = Path("page-prompts/renumbering-backup")
    backup_dir.mkdir(exist_ok=True)
    
    # Mapping from new page number to original page number
    # Pages that got split will share the same prompt
    page_mapping = {
        1: 1,   # Store abandoned
        2: 2,   # Corey arriving
        3: 3,   # Cleaning
        4: 4,   # Serving customers
        5: 5,   # Phone reviews (part 1)
        6: 5,   # Phone reviews (part 2) - same prompt
        7: 6,   # Tablet reviews
        8: 7,   # Visitors (part 1)
        9: 7,   # Visitors (part 2) - same prompt
        10: 8,  # Money troubles
        11: 9,  # Road crews
        12: 10, # E.coli
        13: 11, # November
        14: 12, # Alone in café
        15: 13, # Goodbye
        16: 14, # Family arrives
        17: 15, # Emily encouragement
        18: 16, # Zephyr suggestion
        19: 17, # Emily with list
        20: 18, # Astronaut
        21: 19, # Punk rock
        22: 20, # Ship captain
        23: 21, # Crypto
        24: 22, # Self-driving cars
        25: 23, # Dreams in air
        26: 24, # AI programming
        27: 25, # Lego engineer
        28: 26, # Actor
        29: 27, # Politics
        30: 28, # Bowling
        31: 29, # Truck driver
        32: 30, # Lawyer
        33: 31, # Podcast
        34: 32, # Pro gamer
        35: 33, # Mattress tester
        36: 34, # Hamster guard
        37: 35, # Golf balls
        38: 36, # Water slides
        39: 37, # Food styling
        40: 38, # Stock photos
        41: 39, # Yodeling
        42: 40, # Head spinning
        43: 41, # Transformation
        44: 42, # Tackle hug
        45: 43, # Family declaration
        46: 44, # Store farewell
        47: 45, # Final scene
    }
    
    prompts_dir = Path("page-prompts")
    
    # First, backup all existing files
    for file in prompts_dir.glob("page-*.md"):
        if file.name != "page-00-cover.md":
            shutil.copy2(file, backup_dir / file.name)
    
    # Create new files based on mapping
    for new_page, original_page in page_mapping.items():
        original_file = prompts_dir / f"page-{original_page:02d}.md"
        new_file = prompts_dir / f"page-{new_page:02d}.md"
        
        if original_file.exists():
            # Read original content
            with open(original_file, 'r') as f:
                content = f.read()
            
            # Update the title to reflect new page number
            content = content.replace(
                f"# Page {original_page:02d}",
                f"# Page {new_page:02d}"
            )
            content = content.replace(
                f"# Page {original_page}",
                f"# Page {new_page}"
            )
            
            # Write to new location
            with open(new_file, 'w') as f:
                f.write(content)
            
            print(f"  Created page-{new_page:02d}.md (from page-{original_page:02d}.md)")
        else:
            print(f"  Warning: Original file page-{original_page:02d}.md not found")
    
    # Clean up old numbered files that are no longer needed
    for i in range(48, 56):  # Remove old pages 48-55
        old_file = prompts_dir / f"page-{i:02d}.md"
        if old_file.exists():
            print(f"  Removed obsolete {old_file.name}")
            old_file.unlink()

def update_leonardo_prompts():
    """Update the leonardo folder prompts."""
    print("\nUpdating Leonardo prompts...")
    
    # Same mapping as main prompts
    page_mapping = {
        1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5, 7: 6, 8: 7, 9: 7, 10: 8,
        11: 9, 12: 10, 13: 11, 14: 12, 15: 13, 16: 14, 17: 15, 18: 16,
        19: 17, 20: 18, 21: 19, 22: 20, 23: 21, 24: 22, 25: 23, 26: 24,
        27: 25, 28: 26, 29: 27, 30: 28, 31: 29, 32: 30, 33: 31, 34: 32,
        35: 33, 36: 34, 37: 35, 38: 36, 39: 37, 40: 38, 41: 39, 42: 40,
        43: 41, 44: 42, 45: 43, 46: 44, 47: 45
    }
    
    leonardo_dir = Path("leonardo")
    backup_dir = leonardo_dir / "renumbering-backup"
    backup_dir.mkdir(exist_ok=True)
    
    # Backup existing files
    for file in leonardo_dir.glob("page-*-leonardo.txt"):
        shutil.copy2(file, backup_dir / file.name)
    
    # Create new files
    for new_page, original_page in page_mapping.items():
        original_file = leonardo_dir / f"page-{original_page:02d}-leonardo.txt"
        new_file = leonardo_dir / f"page-{new_page:02d}-leonardo.txt"
        
        if original_file.exists():
            # Read original content
            with open(original_file, 'r') as f:
                content = f.read()
            
            # Update any page number references in the content
            content = content.replace(f"Page {original_page:02d}", f"Page {new_page:02d}")
            content = content.replace(f"Page {original_page}", f"Page {new_page}")
            
            # Write to new location
            with open(new_file, 'w') as f:
                f.write(content)
            
            print(f"  Created page-{new_page:02d}-leonardo.txt (from page-{original_page:02d}-leonardo.txt)")
    
    # Handle back cover
    back_cover_old = leonardo_dir / "page-56-back-cover-leonardo.txt"
    back_cover_new = leonardo_dir / "page-47-back-cover-leonardo.txt"
    if back_cover_old.exists():
        with open(back_cover_old, 'r') as f:
            content = f.read()
        content = content.replace("page-56", "page-47")
        content = content.replace("Page 56", "Page 47")
        with open(back_cover_new, 'w') as f:
            f.write(content)
        print(f"  Updated back cover: page-47-back-cover-leonardo.txt")
    
    # Clean up old files
    for i in range(46, 57):
        old_file = leonardo_dir / f"page-{i:02d}-leonardo.txt"
        if old_file.exists() and i != 47:  # Keep the new back cover
            print(f"  Removed obsolete {old_file.name}")
            old_file.unlink()

def main():
    """Update both sets of prompts."""
    print("🔄 Updating page prompts to match new numbering...")
    update_main_prompts()
    update_leonardo_prompts()
    print("\n✅ All page prompts updated!")
    print("   - Main prompts: page-prompts/")
    print("   - Leonardo prompts: leonardo/")
    print("   - Backups created in respective backup folders")

if __name__ == "__main__":
    main()