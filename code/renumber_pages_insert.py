#!/usr/bin/env python3
"""
Renumber pages after inserting new page 34.
Move pages 34+ forward by one number.
"""

import os
import glob
from pathlib import Path

def renumber_pages():
    """Renumber pages after inserting new page 34."""
    
    prompts_dir = Path("page-prompts")
    
    print("📄 Renumbering pages after inserting new page 34...")
    
    # Start from the end and work backwards to avoid conflicts
    # We need to move page-35.md to page-36.md, etc.
    # But first handle the temp file
    
    # Move the backed up page-35-temp.md to page-36.md
    temp_file = prompts_dir / "page-35-temp.md"
    if temp_file.exists():
        new_file = prompts_dir / "page-36.md"
        temp_file.rename(new_file)
        print(f"  ✅ Moved page-35-temp.md to page-36.md")
        
        # Update the page number inside the file
        with open(new_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace("# Page 34 - The Chef at the Store", "# Page 36 - The Chef at the Store")
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Updated page title in page-36.md")
    
    # Now renumber all pages from 55 down to 35
    for page_num in range(55, 34, -1):  # 55, 54, 53, ... down to 35
        current_file = prompts_dir / f"page-{page_num:02d}.md"
        new_file = prompts_dir / f"page-{page_num+1:02d}.md"
        
        if current_file.exists():
            # Read and update content
            with open(current_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update page number in title
            old_title = f"# Page {page_num:02d} - The Chef at the Store"
            new_title = f"# Page {page_num+1:02d} - The Chef at the Store"
            content = content.replace(old_title, new_title)
            
            # Also handle single-digit format
            old_title_single = f"# Page {page_num} - The Chef at the Store"
            new_title_single = f"# Page {page_num+1} - The Chef at the Store"
            content = content.replace(old_title_single, new_title_single)
            
            # Rename file
            current_file.rename(new_file)
            
            # Write updated content
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Renamed page-{page_num:02d}.md to page-{page_num+1:02d}.md")
    
    # Handle the special case of page 35 -> 37 (since we already did 36)
    old_35 = prompts_dir / "page-35.md"
    if old_35.exists():
        new_37 = prompts_dir / "page-37.md"
        with open(old_35, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace("# Page 35 - The Chef at the Store", "# Page 37 - The Chef at the Store")
        old_35.rename(new_37)
        with open(new_37, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Renamed page-35.md to page-37.md")
    
    # Update back cover to page 56
    old_back = prompts_dir / "page-55-back-cover.md"
    new_back = prompts_dir / "page-56-back-cover.md"
    if old_back.exists():
        old_back.rename(new_back)
        print(f"  ✅ Renamed back cover to page-56-back-cover.md")
    
    print(f"\n✨ Page renumbering complete!")
    print(f"   New total: 56 pages (page-00-cover.md through page-56-back-cover.md)")
    print(f"   New careers page is now page-34.md")

if __name__ == "__main__":
    renumber_pages()