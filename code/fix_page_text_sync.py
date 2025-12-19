#!/usr/bin/env python3
"""
Fix page text synchronization issues by restoring correct text from backups.
"""

from pathlib import Path
import re

def extract_page_text(file_path):
    """Extract PAGE TEXT section from a markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    page_text_lines = []
    in_page_text = False
    
    for line in lines:
        if line.strip().startswith("## PAGE TEXT"):
            in_page_text = True
            page_text_lines.append(line)
            continue
        elif line.strip().startswith("## ") and in_page_text:
            break
        
        if in_page_text:
            page_text_lines.append(line)
    
    return '\n'.join(page_text_lines) if page_text_lines else None

def fix_page_texts():
    """Fix pages that have wrong text content."""
    fixes = [
        # Page 39 should have stock photos/fortune cookies text
        (39, "backup/page-39.md"),
        # Page 40 should have yodeling/pigeons text  
        (40, "backup/page-40.md"),
        # Page 41 should have head spinning text
        (41, "backup/page-41.md"),
    ]
    
    for page_num, backup_path in fixes:
        current_file = Path(f"page-prompts/page-{page_num:02d}.md")
        backup_file = Path(f"page-prompts/{backup_path}")
        
        if not backup_file.exists():
            print(f"❌ Backup file not found: {backup_file}")
            continue
        
        # Extract correct text from backup
        correct_text = extract_page_text(backup_file)
        
        if not correct_text:
            print(f"❌ Could not extract text from backup: {backup_file}")
            continue
        
        # Read current file
        with open(current_file, 'r') as f:
            current_content = f.read()
        
        # Replace the PAGE TEXT section
        new_content = re.sub(
            r'## PAGE TEXT.*?(?=## |\Z)',
            correct_text + '\n',
            current_content,
            flags=re.DOTALL
        )
        
        # Write back
        with open(current_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Fixed page {page_num} text from {backup_path}")
        
        # Show what was restored
        text_lines = correct_text.split('\n')
        preview = []
        for line in text_lines[1:]:  # Skip the "## PAGE TEXT" header
            if line.strip():
                preview.append(line.strip())
        print(f"   Restored text: {' '.join(preview[:2])[:60]}...")

if __name__ == "__main__":
    print("🔧 Fixing page text synchronization issues...\n")
    fix_page_texts()
    print("\n✅ Text synchronization fixes complete!")