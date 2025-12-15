#!/usr/bin/env python3
"""
Update all page prompts to include proper store references:
1. Add 4 two-story white columns to store descriptions
2. Add reference to cartoon-characters/store-cartoon.jpg
"""

import os
import glob
from pathlib import Path

def update_store_references():
    """Update all page prompts with store references."""
    
    prompts_dir = Path("page-prompts")
    updated_files = []
    
    # Find all page prompt files
    page_files = sorted(glob.glob(str(prompts_dir / "page-*.md")))
    
    print(f"🏪 Updating store references in {len(page_files)} files...")
    
    # Replacements for store descriptions
    store_updates = [
        # Add 4 columns to front porch description
        ("Front porch with white columns",
         "Front porch with 4 two-story white columns"),
        
        # Add 4 columns to various column references  
        ("white columns",
         "4 two-story white columns"),
         
        ("White columns",
         "4 two-story white columns"),
         
        # Add store cartoon reference to any store descriptions that don't have it
        ("The Store at Five Corners",
         "The Store at Five Corners (reference: cartoon-characters/store-cartoon.jpg)"),
    ]
    
    # Pattern to add store reference at end of store descriptions
    store_reference_addition = "Reference cartoon-characters/store-cartoon.jpg for accurate building design."
    
    for page_file in page_files:
        file_path = Path(page_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply store-specific replacements
        for old_pattern, new_pattern in store_updates:
            # Only replace if not already updated
            if old_pattern in content and new_pattern not in content:
                content = content.replace(old_pattern, new_pattern)
        
        # Add store cartoon reference if the file mentions the store but doesn't reference cartoon
        if ("Store at Five Corners" in content or "THE STORE" in content) and "cartoon-characters/store-cartoon.jpg" not in content:
            # Find a good place to add the store reference
            if "## IMAGE PROMPT" in content:
                # Add reference before the art style note
                if "**Art Style**:" in content:
                    content = content.replace(
                        "**Art Style**:",
                        f"{store_reference_addition}\n\n**Art Style**:"
                    )
                else:
                    # Add at end of image prompt section
                    content = content.replace(
                        "## IMAGE PROMPT",
                        f"## IMAGE PROMPT\n{store_reference_addition}\n"
                    )
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_files.append(file_path.name)
            print(f"  ✅ Updated {file_path.name}")
    
    print(f"\n📊 Summary:")
    print(f"   Total files checked: {len(page_files)}")
    print(f"   Files updated: {len(updated_files)}")
    
    if updated_files:
        print(f"\n📝 Updated files:")
        for filename in updated_files:
            print(f"   - {filename}")
    else:
        print(f"\n✨ All files already have correct store references!")

if __name__ == "__main__":
    update_store_references()