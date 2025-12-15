#!/usr/bin/env python3
"""
Extract PAGE TEXT content from all page prompt files and save to separate text files.
"""

import os
import glob
from pathlib import Path

def extract_page_text(file_path: Path) -> str:
    """Extract PAGE TEXT section from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    page_text = ""
    in_page_text = False
    
    for line in lines:
        if line.startswith("## PAGE TEXT"):
            in_page_text = True
            continue
        elif line.startswith("## ") and in_page_text:
            # Found next section, stop collecting
            break
        elif in_page_text and line.strip():
            page_text += line.strip() + "\n"
    
    return page_text.strip()

def main():
    """Extract text from all page prompt files."""
    # Create output directory
    output_dir = Path("page text")
    output_dir.mkdir(exist_ok=True)
    
    # Find all page prompt files
    prompt_files = sorted(glob.glob("page-prompts/page-*.md"))
    
    print(f"📁 Found {len(prompt_files)} page prompt files")
    print(f"📝 Creating text files in '{output_dir}' folder")
    
    extracted_count = 0
    
    for prompt_file in prompt_files:
        file_path = Path(prompt_file)
        base_name = file_path.stem  # e.g., "page-01" or "page-00-cover"
        
        try:
            # Extract page text
            page_text = extract_page_text(file_path)
            
            if page_text:
                # Create output file
                output_file = output_dir / f"{base_name}.txt"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(page_text)
                
                print(f"✅ Extracted text from {base_name}: {len(page_text.split())} words")
                extracted_count += 1
            else:
                print(f"⏭️  No text found in {base_name}")
                
        except Exception as e:
            print(f"❌ Error processing {base_name}: {e}")
    
    print(f"\n📊 Summary: Extracted text from {extracted_count}/{len(prompt_files)} files")
    print(f"📁 Text files saved to: {output_dir}")

if __name__ == "__main__":
    main()