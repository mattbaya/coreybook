#!/usr/bin/env python3
"""
Update all page prompts to reference the specific Super3 logo (images/super3v3.png).
"""

import os
import glob
from pathlib import Path

def update_super3_references():
    """Update all page prompts to reference the specific Super3 logo."""
    
    prompts_dir = Path("page-prompts")
    updated_files = []
    
    # Find all page prompt files
    page_files = sorted(glob.glob(str(prompts_dir / "page-*.md")))
    
    print(f"🔍 Updating Super3 logo references in {len(page_files)} files...")
    
    # Patterns to replace
    replacements = [
        # Old pattern 1
        ("Red Superman-style shield with yellow \"3\" in center", 
         "Red diamond shield with large yellow \"3\" in center, plus small letters \"Z\", \"O\", \"R\" in corners (reference: images/super3v3.png)"),
        
        # Old pattern 2  
        ("Red Superman-style shield with yellow \"3\" in center, black outline",
         "Red diamond shield with large yellow \"3\" in center, plus small letters \"Z\", \"O\", \"R\" in corners (reference: images/super3v3.png)"),
         
        # Old pattern 3
        ("SUPER3 LOGO (red/yellow Superman-style shield with \"3\")",
         "SUPER3 LOGO (red diamond shield with yellow \"3\" and corner letters - see images/super3v3.png)"),
         
        # Old pattern 4
        ("SUPER3 LOGO (red and yellow Superman-style shield with \"3\")",
         "SUPER3 LOGO (red diamond shield with yellow \"3\" and corner letters - see images/super3v3.png)"),
         
        # Old pattern 5 - more generic
        ("Super3 logo",
         "Super3 logo (reference: images/super3v3.png)"),
         
        # Old pattern 6
        ("SUPER3 logo",
         "SUPER3 logo (reference: images/super3v3.png)"),
    ]
    
    for page_file in page_files:
        file_path = Path(page_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old_pattern, new_pattern in replacements:
            content = content.replace(old_pattern, new_pattern)
        
        # Additional specific updates for consistency
        if "SUPER3" in content or "Super3" in content:
            # Add explicit logo reference section if it contains Super3 references
            if "reference: images/super3v3.png" not in content:
                # Find a good place to add the reference
                if "All wear BLUE T-SHIRTS with SUPER3 LOGO" in content:
                    content = content.replace(
                        "All wear BLUE T-SHIRTS with SUPER3 LOGO",
                        "All wear BLUE T-SHIRTS with SUPER3 LOGO (see reference image: images/super3v3.png)"
                    )
                elif "blue Super3 t-shirts" in content:
                    content = content.replace(
                        "blue Super3 t-shirts", 
                        "blue Super3 t-shirts (logo reference: images/super3v3.png)"
                    )
                elif "blue Super3 shirt" in content:
                    content = content.replace(
                        "blue Super3 shirt",
                        "blue Super3 shirt (logo reference: images/super3v3.png)"
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
        print(f"\n✨ All files already have correct Super3 logo references!")

if __name__ == "__main__":
    update_super3_references()