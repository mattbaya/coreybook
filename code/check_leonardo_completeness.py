#!/usr/bin/env python3
"""
Check Leonardo files for completeness and compare with main prompts.
"""

import os
import glob
from pathlib import Path

def get_main_prompt_content(page_num):
    """Get the IMAGE PROMPT section from main page file."""
    if page_num == "00-cover":
        main_file = "page-prompts/page-00-cover.md"
    elif page_num == "55-back-cover":
        main_file = "page-prompts/page-55-back-cover.md"
    else:
        main_file = f"page-prompts/page-{page_num:02d}.md"
    
    if not os.path.exists(main_file):
        return "FILE NOT FOUND"
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
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
                # Skip character consistency block
                if not line.startswith("**CRITICAL CHARACTER CONSISTENCY"):
                    image_prompt += line.strip() + " "
                    
        return image_prompt.strip()
    except:
        return "ERROR READING"

def check_leonardo_file(leonardo_file):
    """Check if Leonardo file content is complete."""
    try:
        with open(leonardo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the actual prompt part (after character consistency)
        lines = content.split('\n')
        prompt_start = False
        prompt_content = ""
        
        for line in lines:
            if line.startswith("CHARACTER CONSISTENCY RULES"):
                continue
            elif line.strip() and not line.startswith("[PROMPT]") and not line.startswith("- "):
                prompt_start = True
            
            if prompt_start:
                prompt_content += line.strip() + " "
        
        return prompt_content.strip()
    except:
        return "ERROR READING"

def main():
    """Check all Leonardo files for completeness."""
    leonardo_files = sorted(glob.glob("leonardo/page-*-leonardo.txt"))
    
    print("🔍 CHECKING LEONARDO FILE COMPLETENESS")
    print("=" * 60)
    
    issues_found = 0
    
    for leonardo_file in leonardo_files:
        file_path = Path(leonardo_file)
        filename = file_path.name
        
        # Extract page number from filename
        if "back-cover" in filename:
            page_num = "55-back-cover"
        elif "00-cover" in filename:
            page_num = "00-cover"
        else:
            import re
            match = re.search(r'page-(\d+)', filename)
            page_num = int(match.group(1)) if match else None
        
        if page_num is None:
            print(f"❌ {filename}: Could not extract page number")
            issues_found += 1
            continue
            
        # Get content from both files
        leonardo_content = check_leonardo_file(leonardo_file)
        main_content = get_main_prompt_content(page_num)
        
        # Check for issues
        if len(leonardo_content) < 100:
            print(f"⚠️  {filename}: Very short ({len(leonardo_content)} chars)")
            print(f"    Leonardo: {leonardo_content[:100]}...")
            issues_found += 1
        elif leonardo_content.endswith("futuristic"):
            print(f"❌ {filename}: Content appears cut off (ends with 'futuristic')")
            print(f"    Leonardo: ...{leonardo_content[-100:]}")
            print(f"    Main: {main_content[:100]}...")
            issues_found += 1
        elif len(leonardo_content) < len(main_content) * 0.5:
            print(f"⚠️  {filename}: Much shorter than main prompt ({len(leonardo_content)} vs {len(main_content)} chars)")
            issues_found += 1
        else:
            print(f"✅ {filename}: OK ({len(leonardo_content)} chars)")
    
    print(f"\n📊 SUMMARY:")
    print(f"Files checked: {len(leonardo_files)}")
    print(f"Issues found: {issues_found}")

if __name__ == "__main__":
    main()