#!/usr/bin/env python3
"""
Renumber all pages after 34, skipping missing pages like 35.
Updates all associated files: prompts, images, text files, leonardo files.
"""

import os
import glob
import shutil
from pathlib import Path

def get_page_number(filename):
    """Extract page number from filename."""
    import re
    match = re.search(r'page-(\d+)', filename)
    if match:
        return int(match.group(1))
    return None

def renumber_file(old_path, new_number):
    """Rename a file with new page number."""
    old_path = Path(old_path)
    old_name = old_path.name
    
    # Handle special case for back cover
    if "page-56-back-cover" in old_name:
        new_name = old_name.replace("page-56-back-cover", "page-55-back-cover")
    else:
        import re
        new_name = re.sub(r'page-\d+', f'page-{new_number:02d}', old_name)
    
    new_path = old_path.parent / new_name
    
    if old_path.exists():
        shutil.move(str(old_path), str(new_path))
        return True
    return False

def update_file_content(file_path, old_number, new_number):
    """Update page references inside text files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update page references in content
        import re
        # Update "Page X" references
        content = re.sub(f'Page {old_number}', f'Page {new_number}', content)
        # Update "page-X" references
        content = re.sub(f'page-{old_number}\\b', f'page-{new_number:02d}', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error updating content: {e}")
        return False

def main():
    """Renumber all files after page 34."""
    
    # Define renumbering map (old -> new)
    renumber_map = {
        36: 35, 37: 36, 38: 37, 39: 38, 40: 39,
        41: 40, 42: 41, 43: 42, 44: 43, 45: 44,
        46: 45, 47: 46, 48: 47, 49: 48, 50: 49,
        51: 50, 52: 51, 53: 52, 54: 53,
        56: 55  # back cover
    }
    
    # Directories to process
    directories = {
        "page-prompts": "*.md",
        "generated_images": "page-*.png|page-*.txt",
        "page text": "*.txt",
        "leonardo": "*-leonardo.txt",
        "generated_images/leonardo": "page-*.png",
        "generated_images/leonardo_seeded": "page-*.png",
        "generated_images/hyperbolic": "page-*.png",
        "generated_images/old_versions": "page-*.png",
        "generated_images/backgrounds": "page-*_background.png",
    }
    
    print("📚 Starting page renumbering process...")
    print("📋 Renumbering plan:")
    for old, new in sorted(renumber_map.items()):
        print(f"   Page {old} → Page {new}")
    print()
    
    # Process each directory
    for directory, pattern in directories.items():
        if not os.path.exists(directory):
            continue
            
        print(f"\n📁 Processing {directory}...")
        
        # Get all files matching pattern
        files = []
        for p in pattern.split('|'):
            files.extend(glob.glob(f"{directory}/{p}"))
        
        # Sort files by page number in reverse order to avoid conflicts
        files_with_numbers = []
        for f in files:
            num = get_page_number(f)
            if num and num in renumber_map:
                files_with_numbers.append((f, num))
        
        files_with_numbers.sort(key=lambda x: x[1], reverse=True)
        
        # Rename files
        for file_path, old_num in files_with_numbers:
            new_num = renumber_map[old_num]
            if renumber_file(file_path, new_num):
                print(f"   ✅ Renamed: {Path(file_path).name} → page-{new_num:02d}")
                
                # Update internal content for text files
                new_path = Path(file_path).parent / Path(file_path).name.replace(f'page-{old_num}', f'page-{new_num:02d}')
                if new_path.suffix in ['.md', '.txt']:
                    update_file_content(new_path, old_num, new_num)
    
    # Also handle special case files
    print("\n📁 Processing special cases...")
    
    # Handle page-56-back-cover files specifically
    back_cover_patterns = [
        "page-prompts/page-56-back-cover.md",
        "leonardo/page-56-back-cover-leonardo.txt",
        "generated_images/page-56-back-cover.png",
        "generated_images/page-56-back-cover-text.png",
        "generated_images/backgrounds/page-56-back-cover_background.png"
    ]
    
    for pattern in back_cover_patterns:
        files = glob.glob(pattern)
        for file_path in files:
            if renumber_file(file_path, 55):
                print(f"   ✅ Renamed: {Path(file_path).name} → page-55-back-cover")
                # Update internal content
                new_path = Path(file_path).parent / Path(file_path).name.replace('page-56', 'page-55')
                if new_path.suffix in ['.md', '.txt']:
                    update_file_content(new_path, 56, 55)
    
    print("\n✅ Renumbering complete!")
    print("📌 Note: Page 35 is now what was previously page 36")
    print("📌 Note: Back cover is now page 55 instead of page 56")

if __name__ == "__main__":
    main()