#!/usr/bin/env python3
"""
Create master markdown files combining all page prompts and all page texts.
"""

from pathlib import Path
import re

def extract_page_text(content):
    """Extract just the PAGE TEXT section from a prompt file."""
    lines = content.split('\n')
    page_text_lines = []
    in_page_text = False
    
    for line in lines:
        if line.strip().startswith("## PAGE TEXT"):
            in_page_text = True
            continue
        elif line.strip().startswith("## ") and in_page_text:
            break
        
        if in_page_text and line.strip():
            page_text_lines.append(line.strip())
    
    return '\n'.join(page_text_lines) if page_text_lines else None

def create_master_files():
    """Create master files for all prompts and all texts."""
    prompts_dir = Path("page-prompts")
    
    # Get all page files in order
    page_files = []
    
    # Add cover
    page_files.append(("Page 0 - Cover", prompts_dir / "page-00-cover.md"))
    
    # Add pages 1-51
    for i in range(1, 52):
        page_files.append((f"Page {i}", prompts_dir / f"page-{i:02d}.md"))
    
    # Add back cover
    page_files.append(("Page 52 - Back Cover", prompts_dir / "page-52.md"))
    
    # Create master prompts file
    all_prompts = []
    all_texts = []
    
    for page_title, page_file in page_files:
        if not page_file.exists():
            print(f"❌ Missing file: {page_file}")
            continue
        
        with open(page_file, 'r') as f:
            content = f.read()
        
        # For full prompts file
        all_prompts.append(f"# {page_title}")
        all_prompts.append("")
        all_prompts.append(content)
        all_prompts.append("")
        all_prompts.append("---")
        all_prompts.append("")
        
        # For text-only file
        page_text = extract_page_text(content)
        if page_text:
            all_texts.append(f"# {page_title}")
            all_texts.append("")
            all_texts.append(page_text)
            all_texts.append("")
            all_texts.append("---")
            all_texts.append("")
    
    # Write master prompts file
    with open("all_page_prompts.md", 'w') as f:
        f.write("# The Chef at the Store - All Page Prompts\n\n")
        f.write("This file contains all page prompts including character descriptions, page text, and image prompts.\n\n")
        f.write("---\n\n")
        f.write('\n'.join(all_prompts))
    
    print("✅ Created all_page_prompts.md")
    
    # Write master text file
    with open("all_page_text.md", 'w') as f:
        f.write("# The Chef at the Store - All Page Text\n\n")
        f.write("This file contains only the page text for the entire book.\n\n")
        f.write("---\n\n")
        f.write('\n'.join(all_texts))
    
    print("✅ Created all_page_text.md")
    
    # Statistics
    print(f"\n📊 Statistics:")
    print(f"   Total pages processed: {len([f for _, f in page_files if f.exists()])}")
    print(f"   Pages with text: {len([t for t in all_texts if t and not t.startswith('#') and t != '---' and t != ''])}")

if __name__ == "__main__":
    print("📚 Creating master markdown files...\n")
    create_master_files()