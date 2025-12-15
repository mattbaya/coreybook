#!/usr/bin/env python3
"""
Fix duplication in Leonardo prompt files where CHARACTER CONSISTENCY RULES appear twice.
"""

import os
import glob
import re

def fix_leonardo_duplication(file_path):
    """Remove duplicate CHARACTER CONSISTENCY RULES section from Leonardo files."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there's duplication by counting occurrences
    consistency_count = content.count('CHARACTER CONSISTENCY RULES (CRITICAL):')
    
    if consistency_count <= 1:
        return False  # No duplication
    
    # Split content by the consistency rules marker
    parts = content.split('CHARACTER CONSISTENCY RULES (CRITICAL):')
    
    if len(parts) >= 3:
        # Keep only the first occurrence and the content after the second
        # Find where the actual prompt content starts after the second rules section
        second_section = parts[2]
        
        # Find where the actual prompt starts (usually after TOTAL PEOPLE or similar)
        prompt_start_patterns = [
            r'Create a modern 2D cartoon',
            r'Show ',
            r'Display ',
            r'Illustrate ',
            r'Generate ',
        ]
        
        prompt_start_index = -1
        for pattern in prompt_start_patterns:
            match = re.search(pattern, second_section)
            if match:
                prompt_start_index = match.start()
                break
        
        if prompt_start_index == -1:
            # Fallback: find the end of the character list
            # Look for common ending patterns
            ending_patterns = [
                r'- TOTAL PEOPLE:.*?\n',
                r'- STORE:.*?\n',
            ]
            
            for pattern in ending_patterns:
                match = re.search(pattern, second_section)
                if match:
                    prompt_start_index = match.end()
                    break
        
        if prompt_start_index > -1:
            # Reconstruct without duplication
            new_content = (
                parts[0] + 
                'CHARACTER CONSISTENCY RULES (CRITICAL):' + 
                parts[1].rstrip() + 
                '\n\n' + 
                second_section[prompt_start_index:].lstrip()
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
    
    return False

def main():
    leonardo_files = glob.glob("leonardo/page-*-leonardo.txt")
    fixed_count = 0
    
    print(f"Checking {len(leonardo_files)} Leonardo files for duplication...")
    
    for file_path in sorted(leonardo_files):
        if fix_leonardo_duplication(file_path):
            fixed_count += 1
            print(f"  ✅ Fixed duplication in {os.path.basename(file_path)}")
    
    print(f"\n📊 Summary:")
    print(f"   Files fixed: {fixed_count}/{len(leonardo_files)}")
    
    # Show a sample of the fixed content
    if fixed_count > 0:
        sample_file = "leonardo/page-36-leonardo.txt"
        if os.path.exists(sample_file):
            print(f"\n📄 Sample of fixed content from {sample_file}:")
            with open(sample_file, 'r') as f:
                lines = f.readlines()[:30]
                for i, line in enumerate(lines, 1):
                    print(f"{i:3d}: {line.rstrip()}")

if __name__ == "__main__":
    main()