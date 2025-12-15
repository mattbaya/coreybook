#!/usr/bin/env python3
"""
Enhance Leonardo prompts with stronger character consistency descriptions.
"""

import glob
import re

def enhance_character_descriptions(prompt):
    """Strengthen character descriptions for better consistency."""
    
    # Enhanced character descriptions
    enhanced_chars = {
        "completely BALD man, no hair, dark olive-green apron, white shirt, round friendly face": 
        "COMPLETELY BALD MALE CHEF (no hair, shiny bald head, large forehead), dark olive-green kitchen apron, crisp white shirt, round friendly face with big warm smile, medium build, clean-shaven face",
        
        "woman with short silver pixie-cut hair, black glasses, gray hoodie, green shirt":
        "ADULT WOMAN with distinctive SHORT SILVER PIXIE HAIR (styled, not messy), black rectangular glasses, gray hoodie over green shirt, confident expression",
        
        "11-year-old boy, dark curly brown hair, blue shirt with red diamond \"3\" logo":
        "11-YEAR-OLD BOY with distinctive DARK CURLY BROWN HAIR (not black), blue t-shirt with red diamond shield logo containing yellow number 3",
        
        "11-year-old girl, long honey blonde hair, blue shirt with red diamond \"3\" logo":
        "11-YEAR-OLD GIRL with distinctive LONG HONEY BLONDE HAIR (wavy, shoulder length), blue t-shirt with red diamond shield logo containing yellow number 3",
        
        "9-year-old girl, light brown shoulder-length hair, blue shirt with red diamond \"3\" logo, smallest child":
        "9-YEAR-OLD GIRL (smallest child) with distinctive LIGHT BROWN SHOULDER-LENGTH HAIR, blue t-shirt with red diamond shield logo containing yellow number 3"
    }
    
    # Replace character descriptions
    for old_desc, new_desc in enhanced_chars.items():
        prompt = prompt.replace(old_desc, new_desc)
    
    # Add consistency reinforcement at the end
    if "COMPLETELY BALD" in prompt:
        prompt += ". CRITICAL: Chef must be completely hairless with shiny bald head, no hair whatsoever"
    
    return prompt

def enhance_leonardo_files():
    """Enhance all Leonardo prompt files."""
    files = glob.glob("leonardo/page-*-leonardo.txt")
    
    enhanced_count = 0
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract and enhance prompt
        prompt_match = re.search(r'\[PROMPT\]\n(.+?)(?=\n\n\[NEGATIVE PROMPT\])', content, re.DOTALL)
        if prompt_match:
            original_prompt = prompt_match.group(1).strip()
            enhanced_prompt = enhance_character_descriptions(original_prompt)
            
            # Replace in content
            content = content.replace(original_prompt, enhanced_prompt)
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            enhanced_count += 1
            print(f"✅ Enhanced: {file_path}")
    
    print(f"\n📊 Enhanced {enhanced_count} Leonardo prompt files")

if __name__ == "__main__":
    enhance_leonardo_files()