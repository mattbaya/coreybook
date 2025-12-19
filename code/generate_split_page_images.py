#!/usr/bin/env python3
"""
Generate unique illustrations for split pages 6 and 9.
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

def generate_page6_unique():
    """Generate unique image for page 6 (second half of reviews)."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    # Page 6 prompt - continuation of reviews with different visual focus
    page6_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio).

Create a modern 2D cartoon illustration with cel-shading showing Corey overwhelmed with JOY from the flood of positive reviews continuing to pour in.

**COREY (protagonist):**
- Completely BALD head (no hair), absolutely ecstatic expression
- Navy blue apron over white shirt, arms raised in celebration
- Position: Center of square, dancing or jumping with pure joy
- Expression: Eyes wide with amazement, huge beaming smile
- Activity: Phone in one hand, other hand raised in triumph

**REVIEW EXPLOSION SCENE:**
- Multiple phones/tablets floating around Corey showing different review sites
- Cascading review quotes filling the entire square space:
  - "Beautifully composed sandwiches!" (large, prominent)
  - "Food obsessed in the best way!" (flowing banner)
  - "What a find!" (speech bubble)
  - "Great baked goods!" (floating text)
  - "Worth the stop!" (glowing letters)
  - "5 STARS!" (repeated multiple times)

**OVERWHELMING SUCCESS ELEMENTS:**
- Phone notification sounds visualized as "PING!" "BUZZ!" effects
- Star ratings raining down like confetti (all 5-star ratings)
- Cars visible through window showing overflowing parking lot
- Cash register "CHA-CHING!" sound effects
- Golden light rays emanating from all the positive feedback

**SQUARE COMPOSITION:**
- Corey as joyful center point
- Review quotes arranged in circular pattern around him
- Notification effects filling corners
- Visual representation of "reviews floating everywhere"

**Visual Style:**
- Modern 2D cartoon with cel-shading
- Bright, celebratory colors (golds, bright blues, greens)
- Bold outlines and expressive detailed eyes
- High energy, overwhelming success mood
- Perfect square format (1:1 aspect ratio)

**Text Reference:** "The praise for Corey floated everywhere! His phone buzzed and ping with each new review, And cars overflowed his tiny parking lot too!"
"""
    
    print("📱 Generating unique image for page 6 (review explosion)...")
    
    try:
        response = model.generate_content(page6_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page6_unique.png")
                        image.save(output_path)
                        print(f"✅ Generated page 6 unique image: {image.width}x{image.height}")
                        return True
        
        print("❌ No valid image generated for page 6")
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 6: {e}")
        return False

def generate_page9_unique():
    """Generate unique image for page 9 (second half of visitors)."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    # Page 9 prompt - guest book signing scene
    page9_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio).

Create a modern 2D cartoon illustration with cel-shading showing Corey's GUEST BOOK filled with amazing comments from visitors.

**COREY (protagonist):**
- Completely BALD head (no hair), warm proud smile
- Navy blue apron over white shirt
- Position: Standing beside/behind the guest book table
- Expression: Reading the guest book with deep satisfaction and gratitude
- Activity: Gently turning pages of the thick guest book

**GUEST BOOK SCENE:**
- Large, thick guest book open on rustic wooden table
- Corey's hand visible turning pages or pointing to entries
- Multiple pages visible showing handwritten comments
- Vintage-style guest book with ornate cover

**FLOATING TESTIMONIALS (filling square):**
Arrange these actual quotes around the guest book in handwriting style:
- "My favorite café!" (top left)
- "Such welcoming vibes!" (top right)
- "This place lifts my mood!" (flowing across)
- "Worth the drive!" (prominent)
- "Delicious! So neat!" (speech bubble style)
- "Great spot for a break on a backcountry ride!" (banner)
- "My compliments to the chef!" (bottom)
- "This Chef is a wizard!" (glowing text)
- "Your pizza is BEST!" (enthusiastic lettering)

**CAFE ATMOSPHERE:**
- Warm, cozy interior with customers in background
- Coffee steam rising from cups
- Satisfied customers visible at tables
- Golden afternoon light through windows
- Feeling of community and appreciation

**SQUARE COMPOSITION:**
- Guest book as central focus
- Floating testimonials arranged around all edges
- Corey positioned to one side reading proudly
- Background elements filling remaining space

**Visual Style:**
- Modern 2D cartoon with cel-shading
- Warm, cozy colors (browns, golds, warm whites)
- Handwritten-style fonts for guest book entries
- Bold outlines and expressive detailed eyes
- Grateful, heartwarming mood
- Perfect square format (1:1 aspect ratio)

**Text Reference:** "The journal pages filled up, line after line, With praise for his cooking and space so divine."
"""
    
    print("📚 Generating unique image for page 9 (guest book testimonials)...")
    
    try:
        response = model.generate_content(page9_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page9_unique.png")
                        image.save(output_path)
                        print(f"✅ Generated page 9 unique image: {image.width}x{image.height}")
                        return True
        
        print("❌ No valid image generated for page 9")
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 9: {e}")
        return False

def main():
    """Generate unique images for split pages."""
    print("🎨 Generating unique images for split pages 6 and 9...")
    
    success_count = 0
    
    # Generate page 6 (review explosion)
    if generate_page6_unique():
        success_count += 1
        time.sleep(3)  # Rate limiting
    
    # Generate page 9 (guest book)
    if generate_page9_unique():
        success_count += 1
    
    print(f"\n✅ Generated {success_count}/2 unique split page images")
    print(f"💰 Total cost: ${success_count * 0.039:.2f}")
    
    if success_count == 2:
        print("\n🎯 Ready to update the book with unique images for pages 6 and 9!")

if __name__ == "__main__":
    main()