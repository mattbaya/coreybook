#!/usr/bin/env python3
"""
Fix duplication in Leonardo prompt files where character descriptions appear twice.
"""

import os
import glob
import re

def fix_leonardo_duplication(file_path):
    """Remove duplicate character list from Leonardo files."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Look for the pattern where we have the consistency rules followed by two character lists
    fixed_lines = []
    in_first_list = False
    found_empty_line_after_first = False
    skip_second_list = False
    
    for i, line in enumerate(lines):
        # Detect start of CHARACTER CONSISTENCY RULES
        if 'CHARACTER CONSISTENCY RULES (CRITICAL):' in line:
            in_first_list = True
            fixed_lines.append(line)
            continue
        
        # If we're in the first list
        if in_first_list:
            # Check if this is an empty line after the first list
            if line.strip() == '' and not found_empty_line_after_first:
                found_empty_line_after_first = True
                fixed_lines.append(line)
                continue
            
            # Check if we're starting a duplicate character list
            if found_empty_line_after_first and line.startswith('- COREY:'):
                skip_second_list = True
                continue
            
            # If we're in the second list, skip until we find the actual prompt
            if skip_second_list:
                if (line.startswith('Create ') or 
                    line.startswith('Show ') or 
                    line.startswith('Display ') or
                    line.startswith('Generate ') or
                    line.startswith('Illustrate ')):
                    # Found the actual prompt, stop skipping
                    skip_second_list = False
                    in_first_list = False
                    fixed_lines.append(line)
                elif line.startswith('- TOTAL PEOPLE:'):
                    # This is the last line of the duplicate section
                    # Add it but then prepare to stop skipping
                    continue
                else:
                    # Skip this line
                    continue
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Check if we made any changes
    original_content = ''.join(lines)
    new_content = ''.join(fixed_lines)
    
    if original_content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    leonardo_files = glob.glob("leonardo/page-*-leonardo.txt")
    fixed_count = 0
    
    print(f"Checking {len(leonardo_files)} Leonardo files for character list duplication...")
    
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
                lines = f.readlines()[:25]
                for i, line in enumerate(lines, 1):
                    print(f"{i:3d}: {line.rstrip()}")

if __name__ == "__main__":
    main()