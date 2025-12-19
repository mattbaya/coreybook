#!/usr/bin/env python3
"""
Fix non-square Leonardo images by regenerating them as perfect squares using Gemini API.
"""

import os
import time
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO

# Load environment variables
load_dotenv()
load_dotenv("/Users/mjb9/Dropbox/scripts/coreybook/.env")

# Non-square images that need fixing
NON_SQUARE_IMAGES = [
    "cartoon-characters/leonardo/page-47-back-cover-montage.png",
    "cartoon-characters/leonardo/page34.png", 
    "cartoon-characters/leonardo/page27.png",
    "cartoon-characters/leonardo/page33.png",
    "cartoon-characters/leonardo/page26.png",
    "cartoon-characters/leonardo/page31.png",
    "cartoon-characters/leonardo/page42.png",
    "cartoon-characters/leonardo/page43.png",
    "cartoon-characters/leonardo/page41.png",
    "cartoon-characters/leonardo/page40.png",
    "cartoon-characters/leonardo/page44.png",
    "cartoon-characters/leonardo/page45.png",
    "cartoon-characters/leonardo/page46.png",
    "cartoon-characters/leonardo/page28.jpg"
]

# Map filenames to page numbers for prompt lookup
FILENAME_TO_PAGE = {
    "page-47-back-cover-montage.png": "47-back-cover",
    "page34.png": "34",
    "page27.png": "27", 
    "page33.png": "33",
    "page26.png": "26",
    "page31.png": "31",
    "page42.png": "42",
    "page43.png": "43",
    "page41.png": "41",
    "page40.png": "40",
    "page44.png": "44",
    "page45.png": "45",
    "page46.png": "46",
    "page28.jpg": "28"
}

def get_page_prompt(page_num):
    """Get the image prompt for a specific page."""
    if page_num == "47-back-cover":
        prompt_file = Path("page-prompts/page-47-back-cover.md")
    else:
        prompt_file = Path(f"page-prompts/page-{int(page_num):02d}.md")
    
    if not prompt_file.exists():
        print(f"  ⚠️ Prompt file not found: {prompt_file}")
        return None
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Extract IMAGE PROMPT section
    lines = content.split('\n')
    in_image_prompt = False
    prompt_text = ""
    
    for line in lines:
        if line.strip().startswith("## IMAGE PROMPT"):
            in_image_prompt = True
            continue
        elif line.strip().startswith("## ") and in_image_prompt:
            break
        elif in_image_prompt:
            prompt_text += line + "\n"
    
    return prompt_text.strip()

def generate_square_image(api_key, prompt, output_path, page_num):
    """Generate a square image using Gemini API."""
    print(f"  🎨 Generating square image for page {page_num}...")
    
    # Configure API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    # Enhanced prompt to ensure square output
    enhanced_prompt = f"""CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio). 

{prompt}

IMPORTANT VISUAL REQUIREMENTS:
- Image must be perfectly square (1:1 aspect ratio)
- All characters must have expressive, detailed eyeballs - never just dots for eyes
- Modern 2D cartoon style with cel-shading
- Bold outlines and flat colors
- Clean prominent dark outlines
"""
    
    try:
        response = model.generate_content(enhanced_prompt)
        
        # Process the response
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    
                    try:
                        # Data should be bytes already
                        image = Image.open(BytesIO(image_data))
                        
                        print(f"  📐 Generated image size: {image.width}x{image.height}")
                        
                        # Verify it's square and save
                        if image.width == image.height:
                            image.save(output_path)
                            print(f"  ✅ Saved square image: {image.width}x{image.height}")
                            return True
                        else:
                            print(f"  ⚠️ Image is not square, trying to crop to square...")
                            # Make it square by cropping to the smaller dimension
                            size = min(image.width, image.height)
                            left = (image.width - size) // 2
                            top = (image.height - size) // 2
                            right = left + size
                            bottom = top + size
                            
                            square_image = image.crop((left, top, right, bottom))
                            square_image.save(output_path)
                            print(f"  ✅ Cropped and saved square image: {square_image.width}x{square_image.height}")
                            return True
                            
                    except Exception as decode_error:
                        print(f"  ❌ Error processing image: {decode_error}")
                        continue
        
        print(f"  ❌ No image data found in response")
        return False
        
    except Exception as e:
        print(f"  ❌ Error generating image: {str(e)}")
        return False

def main():
    """Fix all non-square images."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return
    
    print("🔧 Fixing non-square Leonardo images...")
    
    # Process all non-square images
    print(f"   Found {len(NON_SQUARE_IMAGES)} images to fix\n")
    
    success_count = 0
    
    for image_path in NON_SQUARE_IMAGES:
        full_path = Path(image_path)
        filename = full_path.name
        
        if filename not in FILENAME_TO_PAGE:
            print(f"⚠️ Unknown page mapping for {filename}")
            continue
        
        page_num = FILENAME_TO_PAGE[filename]
        print(f"🔄 Fixing {filename} (page {page_num})")
        
        # Get original prompt
        prompt = get_page_prompt(page_num)
        if not prompt:
            continue
        
        # Create backup
        backup_path = full_path.with_suffix(f'.backup{full_path.suffix}')
        if full_path.exists() and not backup_path.exists():
            full_path.rename(backup_path)
            print(f"  📁 Backed up to {backup_path.name}")
        
        # Generate new square image
        if generate_square_image(api_key, prompt, full_path, page_num):
            success_count += 1
        
        # Rate limiting
        time.sleep(3)
        print()
    
    print(f"✅ Fixed {success_count}/{len(NON_SQUARE_IMAGES)} images")
    print(f"💰 Total cost: ${success_count * 0.039:.2f}")

if __name__ == "__main__":
    main()