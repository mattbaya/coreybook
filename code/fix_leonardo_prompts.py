#!/usr/bin/env python3
"""
Fix Leonardo prompts by copying complete content from main page prompts.
"""

import os
import glob
from pathlib import Path

def get_image_prompt_content(page_file):
    """Extract the complete IMAGE PROMPT section from a page file."""
    try:
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        image_prompt = ""
        in_image_prompt = False
        
        for line in lines:
            if line.startswith("## IMAGE PROMPT"):
                in_image_prompt = True
                continue
            elif line.startswith("## ") and in_image_prompt:
                break
            elif in_image_prompt and line.strip():
                # Skip character consistency block but keep everything else
                if not line.startswith("**CRITICAL CHARACTER CONSISTENCY"):
                    image_prompt += line + "\n"
        
        # Clean up the prompt - remove character consistency sections
        prompt_lines = image_prompt.split('\n')
        cleaned_lines = []
        skip_until_empty = False
        
        for line in prompt_lines:
            if line.startswith("**CRITICAL CHARACTER CONSISTENCY"):
                skip_until_empty = True
                continue
            elif skip_until_empty and line.strip() == "":
                skip_until_empty = False
                continue
            elif skip_until_empty:
                continue
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
        
    except Exception as e:
        print(f"Error reading {page_file}: {e}")
        return ""

def create_complete_leonardo_file(page_file, leonardo_file):
    """Create a complete Leonardo file from the main page file."""
    
    # Get the image prompt content
    image_content = get_image_prompt_content(page_file)
    
    if not image_content:
        print(f"❌ No content extracted from {page_file}")
        return False
    
    # Character consistency block
    character_block = """CHARACTER CONSISTENCY RULES (CRITICAL):
- COREY: Completely BALD adult male (no hair), round face, navy blue apron, white shirt
- EMILY: Adult female, short silver pixie hair, black glasses
- REMI: 11-year-old CAUCASIAN WHITE BOY, dark brown hair (not curly), pale/white skin, blue Super3 shirt, non-identical twin to Oona
- OONA: 11-year-old CAUCASIAN WHITE GIRL, long honey blonde hair, pale/white skin, blue Super3 shirt, non-identical twin to Remi
- ZEPHYR: 9-year-old CAUCASIAN WHITE GIRL, light brown shoulder-length hair, pale/white skin, blue Super3 shirt, smallest child
- ALL CHILDREN: Caucasian white with pale/light skin tones, family resemblance
- SUPER3 LOGO: Red diamond shield with yellow "3", letters Z-O-R in corners


"""
    
    # Create complete Leonardo content
    leonardo_content = f"""[PROMPT]

{character_block}{image_content}
"""
    
    # Write to Leonardo file
    try:
        with open(leonardo_file, 'w', encoding='utf-8') as f:
            f.write(leonardo_content)
        return True
    except Exception as e:
        print(f"Error writing {leonardo_file}: {e}")
        return False

def main():
    """Fix all Leonardo files."""
    
    print("🔧 FIXING LEONARDO PROMPTS")
    print("=" * 40)
    
    # Get all main page files
    page_files = sorted(glob.glob("page-prompts/page-*.md"))
    
    fixed_count = 0
    total_count = 0
    
    for page_file in page_files:
        page_path = Path(page_file)
        page_name = page_path.stem
        
        # Determine Leonardo filename
        if page_name == "page-00-cover":
            leonardo_file = "leonardo/page-00-cover-leonardo.txt"
        elif page_name == "page-55-back-cover":
            leonardo_file = "leonardo/page-55-back-cover-leonardo.txt"
        else:
            leonardo_file = f"leonardo/{page_name}-leonardo.txt"
        
        total_count += 1
        
        print(f"📄 Processing {page_name}...")
        
        if create_complete_leonardo_file(page_file, leonardo_file):
            print(f"✅ Fixed {leonardo_file}")
            fixed_count += 1
        else:
            print(f"❌ Failed to fix {leonardo_file}")
    
    print(f"\n📊 SUMMARY:")
    print(f"Total files: {total_count}")
    print(f"Fixed: {fixed_count}")
    print(f"Failed: {total_count - fixed_count}")

if __name__ == "__main__":
    main()