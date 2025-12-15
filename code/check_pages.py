#!/usr/bin/env python3
"""
Check page numbering and content to verify renumbering worked correctly.
"""

import os
import glob
from pathlib import Path

def get_page_title(file_path):
    """Get the title from a page file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('#'):
                return first_line.replace('#', '').strip()
    except:
        pass
    return "Unknown"

def get_first_text_line(file_path):
    """Get first line of PAGE TEXT section."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        in_page_text = False
        
        for line in lines:
            if line.startswith("## PAGE TEXT"):
                in_page_text = True
                continue
            elif line.startswith("## ") and in_page_text:
                break
            elif in_page_text and line.strip():
                return line.strip()[:50] + "..."
    except:
        pass
    return "No text"

# Check page prompts
print("📚 PAGE PROMPTS:")
print("================")
prompt_files = sorted(glob.glob("page-prompts/page-*.md"))

for i, f in enumerate(prompt_files):
    title = get_page_title(f)
    text = get_first_text_line(f)
    print(f"{Path(f).name:25} | {title:40} | {text}")

print(f"\nTotal pages: {len(prompt_files)}")
print(f"Regular pages: {len([f for f in prompt_files if 'back-cover' not in f])}")
print(f"Back cover: {len([f for f in prompt_files if 'back-cover' in f])}")

# Check what should have been renumbered
print("\n📋 EXPECTED RENUMBERING:")
print("========================")
renumber_map = {
    36: 35, 37: 36, 38: 37, 39: 38, 40: 39,
    41: 40, 42: 41, 43: 42, 44: 43, 45: 44,
    46: 45, 47: 46, 48: 47, 49: 48, 50: 49,
    51: 50, 52: 51, 53: 52, 54: 53,
    56: 55  # back cover
}
for old, new in sorted(renumber_map.items()):
    print(f"Page {old} → Page {new}")