#!/usr/bin/env python3
"""
Convert all page prompts to Leonardo.ai optimized format.
"""

import os
import glob
import re
from pathlib import Path

def extract_scene_description(content):
    """Extract the main scene description from the page content."""
    lines = content.split('\n')
    
    # Find the IMAGE PROMPT section
    in_image_section = False
    scene_lines = []
    
    for line in lines:
        if line.startswith("## IMAGE PROMPT"):
            in_image_section = True
            continue
        elif line.startswith("## ") and in_image_section:
            break
        elif in_image_section and line.strip():
            # Skip character consistency blocks
            if "CRITICAL CHARACTER CONSISTENCY" in line or line.startswith("- COREY:") or line.startswith("- EMILY:") or line.startswith("- REMI:") or line.startswith("- OONA:") or line.startswith("- ZEPHYR:") or line.startswith("- SUPER3") or line.startswith("- STORE:") or line.startswith("- TOTAL PEOPLE:"):
                continue
            scene_lines.append(line)
    
    return ' '.join(scene_lines)

def create_leonardo_prompt(scene_text, page_num):
    """Convert scene text to Leonardo.ai optimized format."""
    
    # Clean up the text
    text = scene_text.strip()
    
    # Remove instructional language
    text = re.sub(r'\*\*Art Style\*\*:.*?(?=\n|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Create a modern 2D cartoon illustration.*?showing ', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Create a.*?illustration.*?showing ', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Show the.*?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Should be.*?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'The illustration should.*?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*.*?\*\*', '', text)  # Remove markdown bold
    text = re.sub(r'reference: cartoon-characters/.*?\.jpg', '', text, flags=re.IGNORECASE)
    
    # Replace character descriptions with standardized ones
    text = re.sub(r'Corey[^.]*?bald[^.]*?(wearing|with|stands|is)[^.]*?apron[^.]*?', 'completely BALD man, no hair, dark olive-green apron, white shirt, round friendly face ', text, flags=re.IGNORECASE)
    text = re.sub(r'Emily[^.]*?(wearing|with|has)[^.]*?', 'woman with short silver pixie-cut hair, black glasses, gray hoodie, green shirt ', text, flags=re.IGNORECASE)
    text = re.sub(r'Remi[^.]*?boy[^.]*?hair[^.]*?', '11-year-old boy, dark curly brown hair, blue shirt with red diamond "3" logo ', text, flags=re.IGNORECASE)
    text = re.sub(r'Oona[^.]*?girl[^.]*?hair[^.]*?', '11-year-old girl, long honey blonde hair, blue shirt with red diamond "3" logo ', text, flags=re.IGNORECASE)
    text = re.sub(r'Zephyr[^.]*?girl[^.]*?hair[^.]*?', '9-year-old girl, light brown shoulder-length hair, blue shirt with red diamond "3" logo, smallest child ', text, flags=re.IGNORECASE)
    text = re.sub(r'The Store at Five Corners[^.]*?', 'cream/yellow colonial building, 4 white two-story columns, dark green shutters, green door ', text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace and formatting
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('"', '')
    text = text.replace('(', '').replace(')', '')
    text = text.strip()
    
    # Start with style keywords
    prompt = "2D cartoon illustration, cel-shading, Phil Foglio style, bold outlines, flat colors. "
    
    # Add cleaned scene description
    prompt += text
    
    # Keep it concise (75-150 words)
    words = prompt.split()
    if len(words) > 150:
        prompt = ' '.join(words[:150])
    
    return prompt

def get_negative_prompt(page_num, scene_text):
    """Generate appropriate negative prompt for the page."""
    base_negative = "hair on bald character, realistic style, 3D render, photorealistic, gradient shading, blurry, bad anatomy, extra limbs, deformed faces, wrong number of fingers, text errors, watermark, signature, cropped frame"
    
    # Add scene-specific negatives
    scene_lower = scene_text.lower()
    
    additional = []
    
    if "sad" in scene_lower or "crying" in scene_lower or "defeated" in scene_lower:
        additional.append("happy expressions")
    elif "happy" in scene_lower or "smiling" in scene_lower or "celebrating" in scene_lower:
        additional.append("sad expressions, dark mood")
    
    if "crowd" not in scene_lower and "many people" not in scene_lower:
        additional.append("extra people, crowd")
    
    if additional:
        return base_negative + ", " + ", ".join(additional)
    else:
        return base_negative

def convert_page_file(file_path):
    """Convert a single page file to Leonardo format."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract page number from filename
    filename = Path(file_path).name
    page_num = re.search(r'page-(\d+)', filename).group(1)
    
    # Extract scene description
    scene_description = extract_scene_description(content)
    
    # Create Leonardo prompt
    leonardo_prompt = create_leonardo_prompt(scene_description, page_num)
    
    # Get negative prompt
    negative_prompt = get_negative_prompt(page_num, scene_description)
    
    # Format output
    output = f"[PROMPT]\n{leonardo_prompt}\n\n[NEGATIVE PROMPT]\n{negative_prompt}"
    
    # Write to leonardo folder
    output_filename = f"page-{page_num}-leonardo.txt"
    if filename.startswith("page-00-cover"):
        output_filename = "page-00-cover-leonardo.txt"
    elif filename.endswith("back-cover.md"):
        output_filename = "page-56-back-cover-leonardo.txt"
    
    output_path = f"leonardo/{output_filename}"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ Converted: {filename} → {output_filename}")
    return output_path

def main():
    print("🎨 Converting page prompts to Leonardo.ai format...")
    
    # Find all page files
    page_files = glob.glob("page-prompts/page-*.md")
    
    if not page_files:
        print("❌ No page files found in page-prompts/")
        return
    
    page_files.sort()
    print(f"📄 Found {len(page_files)} page files")
    
    converted_count = 0
    
    for page_file in page_files:
        try:
            convert_page_file(page_file)
            converted_count += 1
        except Exception as e:
            print(f"❌ Error converting {page_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Converted: {converted_count}/{len(page_files)} files")
    print(f"   📁 Output folder: leonardo/")
    print(f"   🎯 Ready for Leonardo.ai image generation")

if __name__ == "__main__":
    main()