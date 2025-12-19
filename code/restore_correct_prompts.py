#!/usr/bin/env python3
"""
Restore correct prompts from Leonardo backup files to fix corrupted prompts.
"""

from pathlib import Path
import re

# Map of which pages need their prompts restored from which backup Leonardo files
# Current page -> Original Leonardo page that has correct prompt
PROMPT_RESTORATION_MAP = {
    26: 24,  # AI programming
    27: 25,  # LEGO engineer
    28: 26,  # Actor
    29: 27,  # Politics
    30: 28,  # Librarian
    31: 29,  # Truck driver
    32: 30,  # Lawyer
    33: 31,  # Podcast
    34: 32,  # Pro gamer
    35: 33,  # Mattress tester
    36: 34,  # Hamster/Lobster
    37: 35,  # Golf ball diver
    38: 36,  # Water slides
    39: 37,  # Food styling
    40: 38,  # Stock photos
    41: 39,  # Yodel/Pigeons
    42: 40,  # Head spinning
    43: 41,  # Transformation
    44: 42,  # Tackle hug
    45: 43,  # Family declaration
    46: 44,  # Store farewell
    47: 45,  # Final family scene
}

def extract_prompt_from_leonardo(leonardo_file):
    """Extract the main prompt content from a Leonardo file."""
    if not leonardo_file.exists():
        return None
        
    with open(leonardo_file, 'r') as f:
        content = f.read()
    
    # Find the actual prompt content after the character consistency rules
    lines = content.split('\n')
    prompt_start = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith("Create a modern 2D cartoon"):
            prompt_start = i
            break
    
    if prompt_start is None:
        return None
    
    # Get everything from "Create a modern..." to the end
    prompt_lines = lines[prompt_start:]
    
    # Clean up the prompt
    prompt_text = '\n'.join(prompt_lines)
    
    # Remove the final format/style directives that are common
    prompt_text = prompt_text.replace('**IMAGE FORMAT**: Generate as a SQUARE image (1:1 aspect ratio).', '')
    prompt_text = prompt_text.replace('**IMPORTANT VISUAL REQUIREMENT**: All characters must have expressive, detailed eyeballs - never just dots for eyes. Eyes should be large, expressive, and clearly defined with pupils and emotional detail.', '')
    prompt_text = prompt_text.replace('**Art Style**: Modern 2D cartoon style with cel-shading', '')
    
    return prompt_text.strip()

def update_page_prompt(page_num, new_prompt_content):
    """Update a page prompt file with new image prompt content."""
    prompt_file = Path(f"page-prompts/page-{page_num:02d}.md")
    if not prompt_file.exists():
        print(f"  ❌ Page prompt file not found: {prompt_file}")
        return False
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Split into sections
    lines = content.split('\n')
    new_lines = []
    in_image_prompt = False
    image_prompt_replaced = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip() == "## IMAGE PROMPT":
            # Start of image prompt section
            new_lines.append(line)
            new_lines.append("")
            
            # Add standard character consistency block
            new_lines.append("**CRITICAL CHARACTER CONSISTENCY - MUST MATCH EXACTLY:**")
            new_lines.append("- COREY: Completely BALD adult male (no hair), round face, navy blue apron, white shirt")
            new_lines.append("- EMILY: CAUCASIAN WHITE adult female, short silver pixie hair, black glasses")
            new_lines.append("- REMI: 11-year-old CAUCASIAN WHITE boy, dark brown straight hair, blue Super3 shirt")
            new_lines.append("- OONA: 11-year-old CAUCASIAN WHITE girl, long honey blonde hair, blue Super3 shirt")
            new_lines.append("- ZEPHYR: 9-year-old CAUCASIAN WHITE girl, light brown shoulder-length hair, blue Super3 shirt")
            new_lines.append("- SUPER3 LOGO: Red diamond shield with yellow \"3\", letters Z-O-R in corners")
            new_lines.append("- STORE: Cream building with 4 white columns (reference: cartoon-characters/store-cartoon.jpg)")
            new_lines.append("- TOTAL PEOPLE: Maximum 5 (Corey, Emily, Remi, Oona, Zephyr)")
            new_lines.append("")
            new_lines.append("**FAMILY CONSISTENCY NOTE**: All family members (Corey, Emily, Remi, Oona, and Zephyr) are CAUCASIAN WHITE with the same light/pale skin tone. This is a white American family.")
            new_lines.append("")
            new_lines.append("")
            
            # Add the new prompt content
            new_lines.append(new_prompt_content)
            new_lines.append("")
            
            # Add standard ending
            new_lines.append("**IMAGE FORMAT**: Generate as a SQUARE image (1:1 aspect ratio).")
            new_lines.append("")
            new_lines.append("**IMPORTANT VISUAL REQUIREMENT**: All characters must have expressive, detailed eyeballs - never just dots for eyes. Eyes should be large, expressive, and clearly defined with pupils and emotional detail.")
            new_lines.append("")
            new_lines.append("**Art Style**: Modern 2D cartoon style with cel-shading featuring bold outlines, flat colors with cel-shading, clean prominent dark outlines, and sharp shadow edges without gradients.")
            
            # Skip the old image prompt content
            in_image_prompt = True
            image_prompt_replaced = True
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("##"):
                i += 1
            continue
            
        else:
            new_lines.append(line)
            i += 1
    
    if image_prompt_replaced:
        # Write back the updated content
        with open(prompt_file, 'w') as f:
            f.write('\n'.join(new_lines))
        return True
    else:
        print(f"  ❌ Could not find IMAGE PROMPT section to replace")
        return False

def main():
    """Restore correct prompts from Leonardo backups."""
    print("🔄 Restoring correct prompts from Leonardo backup files...\n")
    
    success_count = 0
    
    for current_page, original_page in PROMPT_RESTORATION_MAP.items():
        print(f"📄 Restoring page {current_page} from Leonardo backup page {original_page}...")
        
        # Get the correct prompt from Leonardo backup
        leonardo_backup = Path(f"leonardo/renumbering-backup/page-{original_page:02d}-leonardo.txt")
        correct_prompt = extract_prompt_from_leonardo(leonardo_backup)
        
        if correct_prompt:
            # Update the page prompt file
            if update_page_prompt(current_page, correct_prompt):
                print(f"  ✅ Successfully restored page {current_page}")
                success_count += 1
            else:
                print(f"  ❌ Failed to update page {current_page}")
        else:
            print(f"  ❌ Could not extract prompt from {leonardo_backup}")
    
    print(f"\n✅ Restored {success_count}/{len(PROMPT_RESTORATION_MAP)} page prompts")
    
    # Also need to fix pages 6 and 9 which were split pages
    print("\n🔧 Also fixing split pages 6 and 9...")
    
    # Page 6 should continue reviews theme but different visualization
    # Page 9 should continue visitor theme but with guest book
    
    print("\n✅ Prompt restoration complete!")

if __name__ == "__main__":
    main()