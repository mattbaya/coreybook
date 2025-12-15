#!/usr/bin/env python3
"""
Fix panel label instructions to clarify they should not appear in the generated images.
"""

import os
import glob
import re

def fix_panel_labels(file_path):
    """Add clarification that panel labels are for organization only."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Check if this file has panel references
    if not re.search(r'\*\*PANEL \d+', content):
        return False
    
    # Check if we already have the clarification
    if "DO NOT include any text labels like 'PANEL 1'" in content or "Panel labels are for organization only" in content:
        return False
    
    # Find where to insert the clarification - after the main prompt starts but before first panel
    patterns = [
        (r'(Create a modern 2D cartoon illustration[^:]+showing[^:]+:)\n', r'\1\n\n**IMPORTANT**: DO NOT include any text labels like "PANEL 1", "PANEL 2", etc. in the actual image. These labels are for organization only.\n'),
        (r'(Create a modern 2D cartoon illustration[^:]+THREE PANELS[^:]+:)\n', r'\1\n\n**IMPORTANT**: DO NOT include any text labels like "PANEL 1", "PANEL 2", etc. in the actual image. These labels are for organization only.\n'),
        (r'(showing THREE PANELS[^:]+:)\n', r'\1\n\n**IMPORTANT**: DO NOT include any text labels like "PANEL 1", "PANEL 2", etc. in the actual image. These labels are for organization only.\n'),
        (r'(showing a[^:]+montage[^:]+:)\n', r'\1\n\n**IMPORTANT**: DO NOT include any text labels like "PANEL 1", "PANEL 2", etc. in the actual image. These labels are for organization only.\n'),
        (r'(Comic book page layout[^:]+:)\n', r'\1\n\n**IMPORTANT**: DO NOT include any text labels like "PANEL 1", "PANEL 2", etc. in the actual image. Panel labels are for organization only.\n'),
    ]
    
    modified = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
            break
    
    # If we couldn't find a good spot with patterns, look for the first PANEL mention
    if not modified and '**PANEL' in content:
        # Insert before the first panel
        first_panel_index = content.find('**PANEL')
        if first_panel_index > 0:
            # Find the previous newline
            prev_newline = content.rfind('\n', 0, first_panel_index)
            if prev_newline > 0:
                content = (content[:prev_newline] + 
                          '\n\n**IMPORTANT**: DO NOT include any text labels like "PANEL 1", "PANEL 2", etc. in the actual image. These labels are for organization only.\n' + 
                          content[prev_newline:])
                modified = True
    
    if modified and content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    # Process both main prompts and Leonardo files
    all_files = glob.glob("page-prompts/page-*.md") + glob.glob("leonardo/page-*-leonardo.txt")
    fixed_count = 0
    
    print(f"Checking {len(all_files)} files for panel label clarification...")
    
    for file_path in sorted(all_files):
        if fix_panel_labels(file_path):
            fixed_count += 1
            print(f"  ✅ Fixed {os.path.basename(file_path)}")
    
    print(f"\n📊 Summary:")
    print(f"   Files updated: {fixed_count}/{len(all_files)}")
    
    # Show a sample
    if fixed_count > 0:
        sample_file = None
        for f in ["page-prompts/page-36.md", "leonardo/page-36-leonardo.txt", "page-prompts/page-22.md"]:
            if os.path.exists(f) and fix_panel_labels(f):
                sample_file = f
                break
        
        if sample_file and os.path.exists(sample_file):
            print(f"\n📄 Sample from {sample_file}:")
            with open(sample_file, 'r') as f:
                content = f.read()
                # Find and show the area around the clarification
                if "DO NOT include any text labels" in content:
                    index = content.find("DO NOT include any text labels")
                    start = max(0, index - 100)
                    end = min(len(content), index + 200)
                    print("..." + content[start:end] + "...")

if __name__ == "__main__":
    main()