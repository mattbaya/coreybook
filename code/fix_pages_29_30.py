#!/usr/bin/env python3
"""
Fix pages 29 & 30 with correct career fantasy images instead of duplicate reviews.
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

def generate_page29_politics():
    """Generate correct politics image for page 29."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    politics_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio).

Create a modern 2D cartoon illustration with cel-shading showing Corey in a POLITICAL CAREER FANTASY scene.

**COREY (politician):**
- Completely BALD head (no hair), confident political smile
- Professional navy blue suit (not apron - this is career fantasy)
- Position: Center of square at podium or campaign stage
- Expression: Charismatic politician persona, warm but official smile
- Gesture: One hand raised in political wave, other at podium

**POLITICAL CAMPAIGN SCENE (square composition):**
- Campaign podium with "COREY FOR [OFFICE]" banner
- American flags positioned on both sides
- Crowd of supporters in background with campaign signs
- "VOTE COREY!" and "CHANGE WE KNEAD!" signs visible

**POLITICAL ELEMENTS (filling square):**
- Speech bubble with "You could go into POLITICS!"
- Campaign buttons floating around: "CHEF FOR CHANGE"
- Political debate stage setup or town hall setting
- Microphones and cameras capturing the moment
- Capitol building or government building in background

**FANTASY CAREER ELEMENTS:**
- Text banners: "RUN FOR OFFICE!" "PARTNER WITH AOC!"
- Political imagery: voting booths, debate podiums
- Campaign trail elements: "KISS BABIES!" "MAKE SPEECHES!"
- Enthusiastic crowd holding "COREY 2024!" signs

**SQUARE COMPOSITION REQUIREMENTS:**
- Corey at podium as central focus in middle of square
- Campaign elements arranged around all edges
- Background crowd filling upper portion
- Political banners and signs filling side areas
- No empty corners - full square utilization

**Visual Style:**
- Modern 2D cartoon with cel-shading
- Patriotic colors (red, white, blue with gold accents)
- Bold political poster aesthetic
- Expressive detailed eyes showing political confidence
- Inspiring, dynamic campaign energy
- Perfect square format (1:1 aspect ratio)

**Text Reference:** "You could go into POLITICS and run for an office! You could partner with AOC—she'd be your accomplice! Debate on a stage! Make speeches! Kiss babies!"
"""
    
    print("🏛️ Generating correct politics image for page 29...")
    
    try:
        response = model.generate_content(politics_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        # Backup wrong version
                        current_path = Path("cartoon-characters/leonardo/page27.png")
                        backup_path = Path("cartoon-characters/leonardo/page27.wrong_reviews.png")
                        
                        if current_path.exists() and not backup_path.exists():
                            current_path.rename(backup_path)
                            print("📁 Backed up wrong reviews version to page27.wrong_reviews.png")
                        
                        # Save correct politics version
                        image.save(current_path)
                        print(f"✅ Generated page 29 politics image: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 29: {e}")
        return False

def generate_page30_librarian():
    """Generate correct librarian image for page 30."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    librarian_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio).

Create a modern 2D cartoon illustration with cel-shading showing Corey suggesting becoming a LIBRARIAN while Emily objects.

**COREY (aspiring librarian):**
- Completely BALD head (no hair), enthusiastic expression
- Navy blue apron but holding library books
- Position: Left side of square, gesturing excitedly toward library elements
- Expression: Bright idea face, eyes wide with possibility
- Activity: Holding stack of books, pointing to library scene

**EMILY (objecting):**
- Short silver pixie hair, black glasses, stern expression
- Position: Right side of square, arms crossed disapprovingly
- Expression: Glaring, eyebrows furrowed
- Speech bubble: "STAY IN YOUR LANE!"

**LIBRARY FANTASY SCENE (center/background):**
- Towering library shelves filled with books
- "OPEN SCHOLARSHIP AND RESEARCH DATA SERVICES" sign
- Computer terminals and research desks
- Cozy reading areas with comfortable chairs
- Globe and academic references visible

**LIBRARIAN CAREER ELEMENTS:**
- Floating books and knowledge symbols around Corey
- Research databases and digital screens
- "OUTREACH LIBRARIAN" nameplate floating nearby
- Academic atmosphere with warm lighting
- Students studying in background

**SQUARE COMPOSITION REQUIREMENTS:**
- Corey (left) and Emily (right) as main figures
- Library fantasy scene filling center and background
- Speech/thought bubbles filling upper area
- Books and academic elements scattered throughout
- Emily's disapproval contrasting Corey's enthusiasm

**Visual Style:**
- Modern 2D cartoon with cel-shading
- Warm academic colors (browns, golds, deep blues)
- Contrast between Corey's excitement and Emily's stern objection
- Bold outlines and expressive detailed eyes
- Humorous family dynamic with academic setting
- Perfect square format (1:1 aspect ratio)

**Text Reference:** "Or maybe a LIBRARIAN! I could fit in! An 'Open Scholarship and Research Data Services Outreach Librarian'—how hard could THAT be?" But Emily GLARED. "Stay in your LANE!"
"""
    
    print("📚 Generating correct librarian image for page 30...")
    
    try:
        response = model.generate_content(librarian_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        # Backup wrong version
                        current_path = Path("cartoon-characters/leonardo/page28.jpg")
                        backup_path = Path("cartoon-characters/leonardo/page28.wrong_reviews.jpg")
                        
                        if current_path.exists() and not backup_path.exists():
                            current_path.rename(backup_path)
                            print("📁 Backed up wrong reviews version to page28.wrong_reviews.jpg")
                        
                        # Save correct librarian version (keep as .jpg to match original)
                        output_path = Path("cartoon-characters/leonardo/page28.jpg")
                        image.save(output_path)
                        print(f"✅ Generated page 30 librarian image: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 30: {e}")
        return False

def main():
    """Fix pages 29 and 30 with correct career fantasy images."""
    print("🎨 Fixing pages 29 & 30 with correct career fantasy images...")
    
    success_count = 0
    
    # Generate page 29 (politics)
    if generate_page29_politics():
        success_count += 1
        time.sleep(3)  # Rate limiting
    
    # Generate page 30 (librarian)
    if generate_page30_librarian():
        success_count += 1
    
    print(f"\n✅ Fixed {success_count}/2 pages with correct content")
    print(f"💰 Total cost: ${success_count * 0.039:.2f}")
    
    if success_count == 2:
        print("\n🎯 Success! Pages 29 & 30 now have correct career fantasy images.")

if __name__ == "__main__":
    main()