#!/usr/bin/env python3
"""
Regenerate pages 6, 9, 33, 35 with correct Phil Foglio style and character consistency.
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

def generate_page6_phil_foglio():
    """Generate page 6 (review explosion) with Phil Foglio style."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    # Page 6 prompt with Phil Foglio style emphasis
    page6_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio) in PHIL FOGLIO cartoon style.

Create a Phil Foglio style 2D cartoon illustration with exaggerated expressions, dynamic poses, and whimsical energy showing Corey overwhelmed with JOY from the flood of positive reviews.

**PHIL FOGLIO STYLE REQUIREMENTS:**
- Exaggerated expressions with very wide eyes and huge smiles
- Dynamic, energetic poses with bent limbs and action lines
- Thick black outlines with hand-drawn feel
- Whimsical, slightly chaotic composition
- Characters slightly caricatured but still recognizable

**COREY (protagonist):**
- Completely BALD head (no hair at all)
- Round face, huge beaming smile showing teeth
- Navy blue apron over white shirt
- Position: Center, jumping with pure joy, arms raised
- Expression: Eyes wide with amazement, mouth open in delight
- Activity: Phone in one raised hand, other fist pumping

**REVIEW EXPLOSION SCENE:**
- Multiple devices floating chaotically around Corey
- Review quotes bursting out like fireworks:
  - "Beautifully composed sandwiches!" (large, prominent)
  - "Food obsessed in the best way!" (flowing banner)
  - "What a find!" (speech bubble with stars)
  - "Great baked goods!" (floating text)
  - "Worth the stop!" (glowing letters)
  - "5 STARS!" (repeated, scattered everywhere)

**PHIL FOGLIO STYLE EFFECTS:**
- Motion lines showing Corey jumping/dancing
- Sound effects: "PING!" "BUZZ!" "DING!" in comic style
- Stars and sparkles drawn in exaggerated comic style
- Everything slightly tilted for dynamic energy
- Background swirls showing motion and excitement

**CHARACTER CONSISTENCY:**
- COREY: Completely bald Caucasian male, round face
- Art style: Phil Foglio's energetic cartoon style with thick lines
- Mood: Overwhelming joy expressed through exaggerated comic art

**Visual Style:**
- Phil Foglio cartoon style with thick black outlines
- Bright, saturated colors (golds, bright blues, greens)
- Exaggerated expressions and poses
- Dynamic composition with slight chaos
- Perfect square format (1:1 aspect ratio)
"""
    
    print("📱 Generating page 6 (review explosion) in Phil Foglio style...")
    
    try:
        response = model.generate_content(page6_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page6_phil_foglio.png")
                        image.save(output_path)
                        print(f"✅ Generated page 6 in Phil Foglio style: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 6: {e}")
        return False

def generate_page9_phil_foglio():
    """Generate page 9 (guest book) with Phil Foglio style."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    page9_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio) in PHIL FOGLIO cartoon style.

Create a Phil Foglio style 2D cartoon illustration showing Corey's GUEST BOOK filled with visitor comments, featuring the actual handwritten quotes in a readable guest book format.

**PHIL FOGLIO STYLE REQUIREMENTS:**
- Exaggerated happy expressions
- Thick black outlines with organic, hand-drawn feel
- Dynamic composition even for static scene
- Whimsical details and slight caricature

**COREY (protagonist):**
- Completely BALD head (no hair)
- Warm proud smile with crinkled eyes
- Navy blue apron over white shirt
- Position: Leaning over guest book, one hand on page
- Expression: Deep satisfaction, emotional gratitude
- Body language showing he's touched by the comments

**GUEST BOOK SCENE:**
- Large, thick guest book open on rustic wooden table
- Book should be angled so we can READ the actual entries
- Pages filled with different handwriting styles

**ACTUAL GUEST BOOK ENTRIES (must be readable):**
Show these REAL quotes written in the book:
- "This Chef is a wizard!" (fancy script)
- "Your pizza is BEST!" (bold letters)
- "My favorite café!" (neat handwriting)
- "Such welcoming vibes!" (flowing cursive)
- "This place lifts my mood!" (happy writing)
- "Worth the drive!" (underlined)
- "Delicious! So neat!" (with drawn hearts)
- "Great spot for a break on a backcountry ride!" (cramped writing)
- "My compliments to the chef!" (formal script)

**PHIL FOGLIO TOUCHES:**
- Some doodles next to entries (smiley faces, hearts, stars)
- Coffee stain on one page corner
- Pen/pencil visible on table
- Warm golden light making scene cozy
- Background customers visible, all smiling

**COMPOSITION:**
- Guest book as central focus, readable entries
- Corey positioned to side, not blocking text
- Warm cafe atmosphere in background
- All text must be legible and look handwritten

**Visual Style:**
- Phil Foglio cartoon style with thick outlines
- Warm, cozy colors (browns, golds, warm whites)
- Handwritten fonts for guest book entries
- Expressive character art
- Perfect square format (1:1 aspect ratio)
"""
    
    print("📚 Generating page 9 (guest book) in Phil Foglio style...")
    
    try:
        response = model.generate_content(page9_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page9_phil_foglio.png")
                        image.save(output_path)
                        print(f"✅ Generated page 9 in Phil Foglio style: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 9: {e}")
        return False

def main():
    """Regenerate images with Phil Foglio style."""
    print("🎨 Regenerating images with Phil Foglio style...\n")
    
    success_count = 0
    
    # Generate page 6
    if generate_page6_phil_foglio():
        success_count += 1
        time.sleep(3)
    
    # Generate page 9
    if generate_page9_phil_foglio():
        success_count += 1
    
    print(f"\n✅ Regenerated {success_count}/2 images in Phil Foglio style")
    print(f"💰 Total cost: ${success_count * 0.039:.2f}")
    
    if success_count == 2:
        print("\n🎯 Ready to update the book with Phil Foglio style images!")
        print("\nNote: Pages 33 and 35 already have updated prompts with specific")
        print("career content (podcast/TikTok and mattress tester) that match")
        print("their text, so they don't need the generic review/phone regeneration.")

if __name__ == "__main__":
    main()