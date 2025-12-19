#!/usr/bin/env python3
"""
Check what pages are missing from the original structure.
"""

from pathlib import Path

def get_page_numbers_from_dir(dir_path):
    """Extract page numbers from a directory."""
    pages = []
    for file in Path(dir_path).glob("page-*.md"):
        name = file.stem
        if name == "page-00-cover":
            pages.append(0)
        elif name == "page-47-back-cover":
            pages.append("back-cover")
        elif name.startswith("page-") and name[5:7].isdigit():
            pages.append(int(name[5:7]))
    return sorted([p for p in pages if isinstance(p, int)])

def get_page_text_summary(file_path):
    """Get a brief summary of what the page is about."""
    if not file_path.exists():
        return "File not found"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract PAGE TEXT section
    lines = content.split('\n')
    page_text = ""
    in_page_text = False
    
    for line in lines:
        if line.strip().startswith("## PAGE TEXT"):
            in_page_text = True
            continue
        elif line.strip().startswith("## ") and in_page_text:
            break
        elif in_page_text and line.strip():
            page_text += line.strip() + " "
    
    # Return first 100 characters
    return page_text.strip()[:100] + "..." if len(page_text.strip()) > 100 else page_text.strip()

def main():
    """Check for missing pages."""
    print("🔍 Checking for missing pages between original and current structure...\n")
    
    original_pages = get_page_numbers_from_dir("page-prompts/backup")
    current_pages = get_page_numbers_from_dir("page-prompts")
    
    print(f"📚 Original structure: {len(original_pages)} pages (0-{max(original_pages)})")
    print(f"📖 Current structure: {len(current_pages)} pages (0-{max(current_pages)})")
    print()
    
    missing_pages = []
    for page in original_pages:
        if page not in current_pages:
            missing_pages.append(page)
    
    if missing_pages:
        print(f"🚨 MISSING PAGES: {len(missing_pages)} pages are missing!")
        print("=" * 60)
        
        for page_num in missing_pages:
            backup_file = Path(f"page-prompts/backup/page-{page_num:02d}.md")
            text_summary = get_page_text_summary(backup_file)
            print(f"📄 Page {page_num:02d}: {text_summary}")
            print()
    
    # Also check for pages that might be in wrong sequence
    print("🔄 Checking sequence...")
    original_max = max(original_pages)
    current_max = max(current_pages)
    
    if current_max < original_max:
        print(f"📉 Original went up to page {original_max}, current only goes to {current_max}")
        
        # Show what pages 48+ contained
        for i in range(current_max + 1, original_max + 1):
            if i in original_pages:
                backup_file = Path(f"page-prompts/backup/page-{i:02d}.md")
                text_summary = get_page_text_summary(backup_file)
                print(f"📄 Original page {i:02d}: {text_summary}")
    
    # Check if there's a back cover issue
    back_cover_original = Path("page-prompts/backup/page-56-back-cover.md")
    back_cover_current = Path("page-prompts/page-47-back-cover.md")
    
    print(f"\n📖 Back cover:")
    print(f"   Original: page-56-back-cover.md (exists: {back_cover_original.exists()})")
    print(f"   Current:  page-47-back-cover.md (exists: {back_cover_current.exists()})")

if __name__ == "__main__":
    main()