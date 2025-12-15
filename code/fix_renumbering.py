#!/usr/bin/env python3
"""
Fix the renumbering by restoring missing pages from backup and renumbering properly.
"""

import os
import shutil
from pathlib import Path

# First, restore missing pages 36-54 from backup
print("📚 Restoring missing pages from backup...")

backup_dir = Path("page-prompts/backup")
main_dir = Path("page-prompts")

# Pages to restore (36-54)
for page_num in range(36, 55):
    backup_file = backup_dir / f"page-{page_num:02d}.md"
    if page_num < 10:
        backup_file = backup_dir / f"page-0{page_num}.md"
    else:
        backup_file = backup_dir / f"page-{page_num}.md"
    
    if backup_file.exists():
        # Renumber as we restore: 36->35, 37->36, etc.
        new_num = page_num - 1
        new_file = main_dir / f"page-{new_num:02d}.md"
        
        print(f"✅ Restoring page-{page_num} as page-{new_num}")
        shutil.copy2(backup_file, new_file)
        
        # Update internal page references
        with open(new_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace(f'Page {page_num}', f'Page {new_num}')
        content = content.replace(f'page-{page_num}', f'page-{new_num:02d}')
        
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("\n✅ Pages restored and renumbered!")
print("📌 What was page 36 is now page 35")
print("📌 What was page 54 is now page 53")