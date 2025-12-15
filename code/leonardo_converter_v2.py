#!/usr/bin/env python3
"""
Convert page prompts to Leonardo.ai optimized format - Version 2
Simplified approach with manual scene descriptions.
"""

import os
import glob
import re
from pathlib import Path

# Manual scene summaries for key pages to ensure quality
SCENE_DESCRIPTIONS = {
    "page-00-cover": "Family portrait of five people standing together in front of historic store building. Completely BALD man, no hair, dark olive-green apron, white shirt, round friendly face with huge smile stands center. Woman with short silver pixie-cut hair, black glasses, gray hoodie, green shirt beside him. Three children wearing blue shirts with red diamond '3' logo: 11-year-old boy dark curly brown hair, 11-year-old girl long honey blonde hair, 9-year-old girl light brown shoulder-length hair smallest child. Cream/yellow colonial building, 4 white two-story columns, dark green shutters, green door background. Warm golden sunlight, happy family atmosphere.",
    
    "page-02": "Completely BALD man, no hair, dark olive-green apron, white shirt, round friendly face approaching cream/yellow colonial building, 4 white two-story columns, dark green shutters, green door. Carries comically large teetering stack of shiny pots, pans, spatulas, kitchen equipment towering above head. Stars in eyes, huge excited grin, eager posture stepping toward green front door. Dramatic ray of golden sunshine breaking through gray clouds illuminating building like spotlight of destiny. Curious townspeople peeking from behind trees.",
    
    "page-04": "Warm bustling café interior at peak success. Completely BALD man, no hair, dark olive-green apron, white shirt, round friendly face with huge smile standing behind counter handing soup bowl to happy customer. Wood-paneled walls, professional silver espresso machine, copper pendant lamps, chalkboard menu. Glass sunroom filled with happy neighbors at tables chatting, laughing, holding coffee cups. Steam rising from dishes, golden sunlight through windows, cozy community atmosphere.",
}

def get_scene_description(page_num, content):
    """Get scene description for a page."""
    page_key = f"page-{page_num:02d}" if page_num < 56 else f"page-{page_num}"
    
    if page_key == "page-00":
        page_key = "page-00-cover"
    elif "back-cover" in content:
        page_key = "page-56-back-cover"
    
    if page_key in SCENE_DESCRIPTIONS:
        return SCENE_DESCRIPTIONS[page_key]
    
    # Extract from original content as fallback
    lines = content.split('\n')
    scene_lines = []
    in_image_section = False
    
    for line in lines:
        if line.startswith("## IMAGE PROMPT"):
            in_image_section = True
            continue
        elif line.startswith("## ") and in_image_section:
            break
        elif in_image_section and line.strip():
            # Skip character consistency blocks
            if ("CRITICAL CHARACTER CONSISTENCY" in line or 
                line.startswith("- COREY:") or line.startswith("- EMILY:") or 
                line.startswith("- REMI:") or line.startswith("- OONA:") or 
                line.startswith("- ZEPHYR:") or line.startswith("- SUPER3") or 
                line.startswith("- STORE:") or line.startswith("- TOTAL PEOPLE:")):
                continue
            scene_lines.append(line.strip())
    
    # Clean up the extracted text
    text = ' '.join(scene_lines)
    
    # Remove instructional language
    text = re.sub(r'Create a modern 2D cartoon illustration.*?showing ', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Create a.*?illustration.*?showing ', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*Art Style\*\*:.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*.*?\*\*', '', text)  # Remove markdown
    text = re.sub(r'reference: cartoon-characters/.*?\.jpg', '', text, flags=re.IGNORECASE)
    
    # Simplify and shorten
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Limit to key visual elements
    words = text.split()
    if len(words) > 80:
        text = ' '.join(words[:80])
    
    return text

def create_leonardo_prompt(scene_description):
    """Create Leonardo.ai optimized prompt."""
    prompt = f"2D cartoon illustration, cel-shading, Phil Foglio style, bold outlines, flat colors. {scene_description}"
    
    # Keep within word limit
    words = prompt.split()
    if len(words) > 150:
        prompt = ' '.join(words[:150])
    
    return prompt

def get_negative_prompt(scene_description):
    """Generate negative prompt."""
    base_negative = "hair on bald character, realistic style, 3D render, photorealistic, gradient shading, blurry, bad anatomy, extra limbs, deformed faces, wrong number of fingers, text errors, watermark, signature, cropped frame"
    
    scene_lower = scene_description.lower()
    additional = []
    
    if "sad" in scene_lower or "crying" in scene_lower or "defeated" in scene_lower:
        additional.append("happy expressions")
    elif "happy" in scene_lower or "smiling" in scene_lower or "celebrating" in scene_lower:
        additional.append("sad expressions, dark mood")
    
    if "crowd" not in scene_lower:
        additional.append("extra people, crowd")
    
    if additional:
        return f"{base_negative}, {', '.join(additional)}"
    else:
        return base_negative

def convert_page_file(file_path):
    """Convert a single page file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = Path(file_path).name
    
    # Extract page number
    if "back-cover" in filename:
        page_num = 56
        output_name = "page-56-back-cover-leonardo.txt"
    elif "cover" in filename:
        page_num = 0
        output_name = "page-00-cover-leonardo.txt"
    else:
        match = re.search(r'page-(\d+)', filename)
        if match:
            page_num = int(match.group(1))
            output_name = f"page-{page_num:02d}-leonardo.txt"
        else:
            return None
    
    # Get scene description
    scene_description = get_scene_description(page_num, content)
    
    # Create prompts
    leonardo_prompt = create_leonardo_prompt(scene_description)
    negative_prompt = get_negative_prompt(scene_description)
    
    # Format output
    output = f"[PROMPT]\n{leonardo_prompt}\n\n[NEGATIVE PROMPT]\n{negative_prompt}\n"
    
    # Write file
    output_path = f"leonardo/{output_name}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ {filename} → {output_name}")
    return output_path

def main():
    print("🎨 Converting page prompts to Leonardo.ai format (v2)...")
    
    # Find all page files
    page_files = glob.glob("page-prompts/page-*.md")
    page_files.sort()
    
    print(f"📄 Found {len(page_files)} page files")
    
    converted_count = 0
    for page_file in page_files:
        try:
            if convert_page_file(page_file):
                converted_count += 1
        except Exception as e:
            print(f"❌ Error converting {page_file}: {e}")
    
    print(f"\n📊 Converted: {converted_count}/{len(page_files)} files")
    print(f"📁 Output: leonardo/ folder")

if __name__ == "__main__":
    main()