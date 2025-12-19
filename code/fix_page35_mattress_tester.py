#!/usr/bin/env python3
"""
Fix page 35 - generate correct mattress tester image instead of duplicate reviews.
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

def fix_page35_mattress_tester():
    """Generate correct mattress tester image for page 35."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    # Configure API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    # Correct mattress tester prompt for page 35
    mattress_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio).

Create a modern 2D cartoon illustration with cel-shading showing Corey as a PROFESSIONAL MATTRESS TESTER in a dreamy, whimsical scene.

**COREY (protagonist):**
- Completely BALD head (no hair), peaceful sleeping expression with slight smile
- Navy blue apron over white shirt (but relaxed, slightly loosened)
- Position: Lying comfortably on a luxury mattress in testing position
- Expression: Blissfully sleeping, completely relaxed and content

**MATTRESS TESTING SCENE:**
- Large, luxurious mattress with plush pillows and high-quality bedding
- Corey lying in professional testing position (on his back, arms at sides)
- Clipboard on nightstand with "MATTRESS QUALITY ASSESSMENT" form
- Professional badge or vest reading "CERTIFIED MATTRESS TESTER"

**DREAMY SLEEP ELEMENTS (filling square space):**
- Floating Z's and sleep bubbles around Corey's head
- Soft, puffy clouds floating in the background
- Gentle sparkles indicating supreme comfort
- Moon and stars visible through a window
- Text floating nearby: "PROFESSIONAL MATTRESS TESTER"
- Small alarm clock showing various times (testing different sleep cycles)

**CAREER FANTASY ELEMENTS:**
- Dream bubble above showing "SLEEP FOR A LIVING!"
- Rating stars floating around: "5 STARS FOR COMFORT"
- Professional mattress testing checklist visible: "SOFTNESS ✓ SUPPORT ✓ COMFORT ✓"

**SQUARE COMPOSITION REQUIREMENTS:**
- Mattress positioned diagonally or centrally to fill square format
- Sleep/dream elements arranged around all edges
- Corey's peaceful pose as central focus
- Background elements filling all corners (clouds, stars, floating text)

**Visual Style:**
- Modern 2D cartoon with cel-shading
- Soft, dreamy color palette (blues, purples, whites)
- Bold outlines but gentler than usual to match sleepy mood
- Expressive detailed eyes (closed peacefully, with long lashes)
- Cozy, comfortable, whimsical atmosphere
- Perfect square format (1:1 aspect ratio)

**Page Text Reference:** "PROFESSIONAL MATTRESS TESTER! You'd sleep for a living from dusk until dawn!"
"""
    
    print("🛏️ Generating correct mattress tester image for page 35...")
    
    try:
        response = model.generate_content(mattress_prompt)
        
        # Process response
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    print(f"📐 Generated image size: {image.width}x{image.height}")
                    
                    if image.width == image.height:
                        # Backup current wrong version
                        current_path = Path("cartoon-characters/leonardo/page35.png")
                        backup_path = Path("cartoon-characters/leonardo/page35.wrong_reviews.png")
                        
                        if current_path.exists():
                            current_path.rename(backup_path)
                            print("📁 Backed up wrong reviews version to page35.wrong_reviews.png")
                        
                        # Save correct mattress tester version
                        image.save(current_path)
                        print(f"✅ Saved correct mattress tester image: {image.width}x{image.height}")
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
    if fix_page35_mattress_tester():
        print("\n🎯 Success! Page 35 now has correct mattress tester image.")
        print("💰 Cost: $0.039")
    else:
        print("\n❌ Failed to generate mattress tester image")