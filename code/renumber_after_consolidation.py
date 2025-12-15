#!/usr/bin/env python3
"""
Renumber pages after consolidating the emotional arc (pages 42-44).

Original structure:
- Pages 42-44: New consolidated emotional arc (already updated)
- Pages 45-47: Old emotional arc content (to be deleted)
- Pages 48-53: Final pages (to be renumbered to 45-50)
- Page 55: Back cover (to become page 51)

New structure:
- Pages 42-44: Consolidated emotional arc
- Pages 45-50: Final pages (renumbered from 48-53)
- Page 51: Back cover (renumbered from 55)

This saves 6 pages total: 3 from consolidation + 3 from eliminating redundant pages.
"""

import os
import shutil

def renumber_pages():
    """Renumber pages after emotional arc consolidation."""
    
    # Define the renumbering mapping
    # Format: (old_page_num, new_page_num)
    renumber_map = [
        (48, 45),  # Page 48 becomes 45
        (49, 46),  # Page 49 becomes 46  
        (50, 47),  # Page 50 becomes 47
        (51, 48),  # Page 51 becomes 48
        (52, 49),  # Page 52 becomes 49
        (53, 50),  # Page 53 becomes 50
        (55, 51),  # Back cover: 55 becomes 51
    ]
    
    # Pages to delete (old emotional arc content)
    pages_to_delete = [45, 46, 47]
    
    print("🔄 Renumbering pages after emotional arc consolidation...")
    
    # Step 1: Delete old emotional arc pages (45-47)
    print("\n📄 Deleting old emotional arc pages...")
    for page_num in pages_to_delete:
        # Delete main prompts
        main_file = f"page-prompts/page-{page_num:02d}.md"
        if os.path.exists(main_file):
            os.remove(main_file)
            print(f"   Deleted: {main_file}")
        
        # Delete Leonardo prompts
        leonardo_file = f"leonardo/page-{page_num:02d}-leonardo.txt"
        if os.path.exists(leonardo_file):
            os.remove(leonardo_file)
            print(f"   Deleted: {leonardo_file}")
    
    # Step 2: Renumber remaining pages
    print("\n🔢 Renumbering pages...")
    for old_num, new_num in renumber_map:
        # Handle main prompts
        if old_num == 55:
            old_main = "page-prompts/page-55-back-cover.md"
            new_main = f"page-prompts/page-{new_num:02d}-back-cover.md"
        else:
            old_main = f"page-prompts/page-{old_num:02d}.md"
            new_main = f"page-prompts/page-{new_num:02d}.md"
        
        if os.path.exists(old_main):
            shutil.move(old_main, new_main)
            print(f"   Renamed: page-{old_num:02d}.md → page-{new_num:02d}.md")
            
            # Update the page title in the content
            update_page_title(new_main, new_num)
        
        # Handle Leonardo prompts
        if old_num == 55:
            old_leonardo = "leonardo/page-55-back-cover-leonardo.txt"
            new_leonardo = f"leonardo/page-{new_num:02d}-back-cover-leonardo.txt"
        else:
            old_leonardo = f"leonardo/page-{old_num:02d}-leonardo.txt"
            new_leonardo = f"leonardo/page-{new_num:02d}-leonardo.txt"
        
        if os.path.exists(old_leonardo):
            shutil.move(old_leonardo, new_leonardo)
            print(f"   Renamed: page-{old_num:02d}-leonardo.txt → page-{new_num:02d}-leonardo.txt")

def update_page_title(file_path, new_page_num):
    """Update the page title in the markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the title line
        lines = content.split('\n')
        if lines and lines[0].startswith('# Page'):
            # Extract the title part after the page number
            parts = lines[0].split(' - ', 1)
            if len(parts) == 2:
                title_part = parts[1]
                if 'back-cover' in file_path.lower() or 'back cover' in title_part.lower():
                    lines[0] = f"# Page {new_page_num} - {title_part}"
                else:
                    lines[0] = f"# Page {new_page_num} - {title_part}"
            else:
                lines[0] = f"# Page {new_page_num} - The Chef at the Store"
        
        # Write back the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
    except Exception as e:
        print(f"   Warning: Could not update title in {file_path}: {e}")

def verify_renumbering():
    """Verify the renumbering was successful."""
    print("\n✅ Verifying renumbering...")
    
    # Check that new pages exist
    expected_pages = list(range(42, 52))  # Pages 42-51
    
    for page_num in expected_pages:
        if page_num == 51:
            main_file = f"page-prompts/page-{page_num:02d}-back-cover.md"
            leonardo_file = f"leonardo/page-{page_num:02d}-back-cover-leonardo.txt"
        else:
            main_file = f"page-prompts/page-{page_num:02d}.md"
            leonardo_file = f"leonardo/page-{page_num:02d}-leonardo.txt"
        
        if os.path.exists(main_file):
            print(f"   ✅ {main_file}")
        else:
            print(f"   ❌ Missing: {main_file}")
        
        if os.path.exists(leonardo_file):
            print(f"   ✅ {leonardo_file}")
        else:
            print(f"   ❌ Missing: {leonardo_file}")
    
    # Check that old pages are gone
    old_pages = [45, 46, 47, 48, 49, 50, 52, 53, 55]
    print("\n🗑️  Verifying old pages are removed...")
    for page_num in old_pages:
        if page_num == 55:
            old_files = [
                "page-prompts/page-55-back-cover.md",
                "leonardo/page-55-back-cover-leonardo.txt"
            ]
        else:
            old_files = [
                f"page-prompts/page-{page_num:02d}.md",
                f"leonardo/page-{page_num:02d}-leonardo.txt"
            ]
        
        for old_file in old_files:
            if not os.path.exists(old_file):
                print(f"   ✅ Removed: {old_file}")
            else:
                print(f"   ❌ Still exists: {old_file}")

def main():
    """Main function to handle the renumbering."""
    print("📚 CoreyBook Page Renumbering After Consolidation")
    print("=" * 50)
    print("This script will:")
    print("- Delete old emotional arc pages (45-47)")
    print("- Renumber pages 48-53 to become 45-50")
    print("- Renumber back cover from 55 to 51")
    print("- Save 6 pages total (3 from consolidation + 3 removed)")
    
    print("\n✅ Proceeding with renumbering...")
    
    try:
        renumber_pages()
        verify_renumbering()
        
        print("\n🎉 Renumbering completed successfully!")
        print(f"📊 Book structure:")
        print(f"   - Pages 1-41: Unchanged")
        print(f"   - Pages 42-44: Consolidated emotional arc")
        print(f"   - Pages 45-50: Final story pages (renumbered from 48-53)")
        print(f"   - Page 51: Back cover (renumbered from 55)")
        print(f"   - Total pages: 51 (reduced from 55)")
        
    except Exception as e:
        print(f"❌ Error during renumbering: {e}")
        print("Please check the file system and try again.")

if __name__ == "__main__":
    main()