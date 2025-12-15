#!/usr/bin/env python3
"""
Update Leonardo prompts to match the consolidated final pages 45-47.
This copies the image descriptions from the main prompts to the Leonardo versions.
"""

import re

def extract_image_prompt(main_file_path):
    """Extract the image prompt section from a main prompt file."""
    try:
        with open(main_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the image prompt section (after "Create a modern 2D cartoon illustration")
        match = re.search(r'(Create a modern 2D cartoon illustration.*?)(\*\*IMAGE FORMAT\*\*|\*\*IMPORTANT VISUAL REQUIREMENT\*\*|$)', content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        else:
            print(f"Warning: Could not find image prompt in {main_file_path}")
            return None
            
    except Exception as e:
        print(f"Error reading {main_file_path}: {e}")
        return None

def update_leonardo_prompt(leonardo_file_path, new_image_prompt):
    """Update a Leonardo prompt file with new image content."""
    try:
        with open(leonardo_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace everything after the character consistency rules with the new prompt
        lines = content.split('\n')
        
        # Find where to insert the new prompt (after the empty line after SUPER3 LOGO)
        new_lines = []
        found_end_of_rules = False
        
        for line in lines:
            new_lines.append(line)
            if line.strip() == '- SUPER3 LOGO: Red diamond shield with yellow "3", letters Z-O-R in corners':
                new_lines.append('')  # Empty line
                new_lines.append('')  # Another empty line
                new_lines.append(new_image_prompt)
                found_end_of_rules = True
                break
        
        if not found_end_of_rules:
            print(f"Warning: Could not find end of character rules in {leonardo_file_path}")
            return False
        
        # Add the standard endings
        new_lines.extend([
            '**IMAGE FORMAT**: Generate as a SQUARE image (1:1 aspect ratio).',
            '**IMPORTANT VISUAL REQUIREMENT**: All characters must have expressive, detailed eyeballs - never just dots for eyes. Eyes should be large, expressive, and clearly defined with pupils and emotional detail.',
            '**Art Style**: Modern 2D cartoon style with cel-shading with brilliant, hopeful colors representing the final moments of this transformative story.',
            ''
        ])
        
        # Write back the updated content
        with open(leonardo_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True
        
    except Exception as e:
        print(f"Error updating {leonardo_file_path}: {e}")
        return False

def main():
    """Update Leonardo prompts for the consolidated final pages."""
    print("🔄 Updating Leonardo prompts for consolidated final pages...")
    
    # Map of page numbers to update
    pages_to_update = [45, 46, 47]
    
    for page_num in pages_to_update:
        main_file = f"page-prompts/page-{page_num:02d}.md"
        leonardo_file = f"leonardo/page-{page_num:02d}-leonardo.txt"
        
        print(f"\n📄 Processing page {page_num}...")
        
        # Extract image prompt from main file
        image_prompt = extract_image_prompt(main_file)
        if not image_prompt:
            print(f"   ❌ Failed to extract image prompt from {main_file}")
            continue
        
        # Update Leonardo file
        if update_leonardo_prompt(leonardo_file, image_prompt):
            print(f"   ✅ Updated {leonardo_file}")
        else:
            print(f"   ❌ Failed to update {leonardo_file}")
    
    print("\n🎉 Leonardo prompt updates completed!")

if __name__ == "__main__":
    main()