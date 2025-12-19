#!/usr/bin/env python3
"""
Regenerate page 33 with square-optimized composition.
"""

import os
import time
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()
load_dotenv("/Users/mjb9/Dropbox/scripts/coreybook/.env")

def regenerate_page33_square():
    """Regenerate page 33 with optimized square composition."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    # Configure API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    # Square-optimized prompt for page 33
    square_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio).

Create a modern 2D cartoon illustration with cel-shading showing Corey in his kitchen reading amazing reviews on his phone, with the composition optimized for a SQUARE format.

**COREY (protagonist):**
- Completely BALD head (no hair), big warm genuine smile, eyes sparkling with joy
- Navy blue apron over white shirt, looking confident and successful
- Position: CENTER of the square image, holding phone with both hands at chest level
- Expression: Beaming with pride, genuine delight reading the reviews

**COMPOSITION FOR SQUARE FORMAT:**
- Corey should fill the central portion of the square
- Background shows his kitchen with professional espresso machine and clean workspace
- Golden afternoon light streaming from windows creates warm atmosphere

**3D HOLOGRAPHIC PHONE EFFECTS (filling square space):**
- Large glowing THUMBS UP hologram floating ABOVE Corey's head
- Five GOLD STARS with sparkle effects arranged in a circle around the thumbs up
- Review quote bubbles floating around the sides of the square:
  - "Chef Corey is awesome!" (top left)
  - "Ridiculously good!" (top right)  
  - "Finally someone who knows what they're doing!" (bottom)
  - "5 STARS!" (with star icons)

**SQUARE COMPOSITION REQUIREMENTS:**
- Corey positioned in center with holographic elements filling the full square space
- Review quotes positioned around the edges to use all square area
- Vertical elements (Corey + thumbs up) balanced with horizontal elements (review bubbles)
- NO empty space in corners - fill the entire square with content

**Visual Style:**
- Modern 2D cartoon with cel-shading
- Bold outlines and flat colors
- Expressive detailed eyes (never dots)
- Bright, warm, celebratory mood
- Perfect square format (1:1 aspect ratio)
"""
    
    print("🎨 Regenerating page 33 with square-optimized composition...")
    
    try:
        response = model.generate_content(square_prompt)
        
        # Process response
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    print(f"📐 Generated image size: {image.width}x{image.height}")
                    
                    if image.width == image.height:
                        # Backup current version
                        current_path = Path("cartoon-characters/leonardo/page33.png")
                        backup_path = Path("cartoon-characters/leonardo/page33.square_backup.png")
                        
                        if current_path.exists():
                            current_path.rename(backup_path)
                            print("📁 Backed up current version to page33.square_backup.png")
                        
                        # Save new version
                        image.save(current_path)
                        print(f"✅ Saved new square-optimized page 33: {image.width}x{image.height}")
                        return True
                    else:
                        print(f"⚠️ Generated image is not square: {image.width}x{image.height}")
                        return False
        
        print("❌ No image data found in response")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if regenerate_page33_square():
        print("\n🎯 Success! Page 33 regenerated with square-optimized composition.")
        print("💰 Cost: $0.039")
    else:
        print("\n❌ Failed to regenerate page 33")