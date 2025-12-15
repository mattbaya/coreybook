#!/usr/bin/env python3
"""
Fix page prompt structure to match the new format:
1. Main image prompt at the top
2. Character descriptions after
3. Remove duplicate consistency blocks
"""

import glob
import re

def fix_page_structure(file_path):
    """Fix a single page prompt file structure."""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    # Extract components
    title = ""
    page_text = ""
    image_prompt = ""
    character_descriptions = ""
    store_description = ""
    
    # Parse existing content
    current_section = None
    for line in lines:
        if line.startswith("# Page"):
            title = line
        elif line.startswith("## PAGE TEXT"):
            current_section = "page_text"
            continue
        elif line.startswith("## IMAGE PROMPT"):
            current_section = "image_prompt"
            continue
        elif line.startswith("## CHARACTER DESCRIPTIONS"):
            current_section = "character_desc"
            continue
        elif line.startswith("## "):
            current_section = None
            continue
        elif line.startswith("**CRITICAL CHARACTER CONSISTENCY"):
            # Skip the old consistency blocks
            continue
        elif line.startswith("- COREY:") or line.startswith("- EMILY:") or line.startswith("- REMI:") or line.startswith("- OONA:") or line.startswith("- ZEPHYR:") or line.startswith("- SUPER3") or line.startswith("- STORE:") or line.startswith("- TOTAL PEOPLE:"):
            # Skip old consistency block lines
            continue
        elif current_section == "page_text" and line.strip():
            page_text += line.strip() + " "
        elif current_section == "image_prompt" and line.strip():
            # Clean up the image prompt
            line_clean = line.strip()
            # Remove references to Create a modern 2D... if it exists
            if not line_clean.startswith("Create a modern 2D cartoon illustration") and not line_clean.startswith("**Art Style**"):
                image_prompt += line_clean + " "
        elif current_section == "character_desc" and line.strip():
            character_descriptions += line + "\n"
    
    # Extract the clean image prompt from the mess
    # Look for the core scene description
    lines_for_prompt = content.split('\n')
    clean_prompt_lines = []
    
    for i, line in enumerate(lines_for_prompt):
        # Skip the title
        if line.startswith("# Page"):
            continue
        # Skip section headers
        if line.startswith("## "):
            break
        # Skip empty lines at start
        if not clean_prompt_lines and not line.strip():
            continue
        # Skip the old "Create a..." starter if present
        if line.strip().startswith("Create a modern 2D cartoon illustration"):
            # Take everything after "showing"
            if "showing" in line:
                after_showing = line.split("showing", 1)[1].strip()
                if after_showing:
                    clean_prompt_lines.append(after_showing)
            continue
        # Add content lines
        if line.strip() and not line.startswith("**CRITICAL") and not line.startswith("- COREY:"):
            clean_prompt_lines.append(line.strip())
    
    # Reconstruct in new format
    new_content = f"""{title}

{' '.join(clean_prompt_lines).strip()}

## CHARACTER DESCRIPTIONS

### COREY (protagonist)
- **Physical**: Completely BALD head (no hair), warm friendly face with genuine big smile, fit medium build
- **Clothing**: Navy blue apron over casual clothes (long-sleeve gray or black shirt), carrying kitchen equipment
- **Expression**: Stars in his eyes, huge excited grin, eager and optimistic
- **Personality**: Determined chef with a dream, infectious enthusiasm

### EMILY (Corey's wife)
- **Physical**: Short silver pixie-cut hair, black rectangular glasses, confident smile
- **Clothing**: Gray hoodie over green shirt, practical and comfortable
- **Expression**: Supportive and encouraging, warm maternal presence
- **Personality**: Librarian, the family's rock and source of wisdom

### THE SUPER THREE (Corey's children)

#### REMI (11-year-old son)
- **Physical**: Dark curly brown hair, energetic build
- **Clothing**: Blue Super3 t-shirt with red diamond logo containing yellow "3"
- **Expression**: Brave and determined, natural leader
- **Personality**: The oldest, protective of his sisters, adventure-seeker

#### OONA (11-year-old daughter)  
- **Physical**: Long honey blonde hair, athletic build
- **Clothing**: Blue Super3 t-shirt with red diamond logo containing yellow "3"
- **Expression**: Determined and strong-willed
- **Personality**: Athletic twin, fierce and independent

#### ZEPHYR (9-year-old daughter)
- **Physical**: Light brown shoulder-length hair, smallest of the three
- **Clothing**: Blue Super3 t-shirt with red diamond logo containing yellow "3" 
- **Expression**: Biggest smile, most enthusiastic
- **Personality**: The youngest, eternal optimist, brings joy to every situation

## PAGE TEXT
{page_text.strip()}

## SETTING DETAILS

### THE STORE AT FIVE CORNERS
- **Architecture**: Historic 250-year-old building, cream/pale yellow clapboard siding, dark forest green shutters
- **Features**: Four white two-story columns across the front, green front door
- **Location**: Five-way intersection in Berkshire Mountains, Massachusetts, with rolling hills in background
- **Atmosphere**: Quintessential New England charm, community gathering place

### SUPER3 LOGO DETAILS
- **Design**: Red diamond shield with large yellow "3" in center
- **Corner Letters**: Small "Z", "O", "R" in three corners of the diamond
- **Reference**: images/super3v3.png
- **Significance**: Family superhero team identity
"""
    
    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content.strip() + '\n')
    
    print(f"  ✅ Fixed: {file_path}")

def main():
    print("🔧 Fixing page prompt structure...")
    
    # Skip page-02.md since user already fixed it
    page_files = [f for f in glob.glob("page-prompts/page-*.md") if not f.endswith("page-02.md")]
    
    print(f"📄 Found {len(page_files)} page files to fix (skipping page-02.md)")
    
    # Create backup directory
    import os
    os.makedirs("page-prompts/structure-backup", exist_ok=True)
    
    fixed_count = 0
    
    for page_file in sorted(page_files):
        try:
            # Create backup
            backup_file = page_file.replace("page-prompts/", "page-prompts/structure-backup/")
            with open(page_file, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
            
            # Fix the file
            fix_page_structure(page_file)
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error fixing {page_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Fixed: {fixed_count}/{len(page_files)} files")
    print(f"   📁 Backups saved to: page-prompts/structure-backup/")
    print(f"   🎯 All prompts now follow the new structure")

if __name__ == "__main__":
    main()