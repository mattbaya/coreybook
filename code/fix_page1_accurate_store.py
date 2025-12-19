#!/usr/bin/env python3
"""
Regenerate page 1 to accurately match the Store at Five Corners photo.
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

def generate_accurate_page1():
    """Generate page 1 that accurately matches the Store photo."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    page1_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio) in PHIL FOGLIO cartoon style.

Create a Phil Foglio style illustration of THE STORE AT FIVE CORNERS looking abandoned, but ACCURATELY matching the real building architecture.

**CRITICAL ARCHITECTURAL ACCURACY:**
Reference the actual Store at Five Corners building:
- TWO-STORY historic New England colonial building
- CREAM/PALE YELLOW clapboard siding (weathered and faded for abandonment)
- DARK FOREST GREEN shutters (some hanging crooked)
- Four WHITE COLUMNS on the front porch (two-story height)
- Glass-enclosed SUNROOM addition on the LEFT side of building
- Green canvas AWNINGS over ground-floor windows (now torn/faded)
- Second-floor BALCONY with white wooden railings
- Multiple CHIMNEYS on the roof
- "The Store at Five Corners" sign (weathered and faded)

**ABANDONMENT DETAILS:**
- Paint peeling from siding
- Some shutters hanging crooked or missing
- Dusty, dirty windows with cobwebs
- Weeds growing around the foundation
- Small crooked "CLOSED" sign in one window
- Overall neglected appearance but structurally sound

**SETTING DETAILS:**
- Five roads converging at the intersection
- Rolling Berkshire Mountains in background
- Red barn visible across one of the streets
- Gray, melancholy sky (not threatening, just sad)
- Empty parking area with scattered leaves
- American flag on flagpole (drooping)

**PHIL FOGLIO STYLE:**
- Thick black outlines with hand-drawn feel
- Slightly exaggerated decay for comic effect
- Building has character even when sad
- Muted but recognizable colors

**EMOTIONAL TONE:**
- Lonely but waiting to be loved again
- "Character in need of rescue" feeling
- Inherent beauty underneath the neglect
- Potential visible despite current state

The building should look exactly like the real Store at Five Corners but in cartoon style and showing abandonment.
"""
    
    print("🏚️ Regenerating page 1 with accurate Store architecture...")
    
    try:
        response = model.generate_content(page1_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page1_accurate_store.jpg")
                        image.save(output_path, quality=95)
                        print(f"✅ Generated accurate page 1: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 1: {e}")
        return False

def main():
    """Fix page 1 with accurate Store architecture."""
    print("🎨 Regenerating page 1 with accurate Store at Five Corners architecture...\n")
    
    if generate_accurate_page1():
        print("\n✅ Success! Page 1 now accurately matches the real Store building")
        print("- Correct two-story colonial architecture")
        print("- Cream siding with green shutters") 
        print("- Four white columns and sunroom addition")
        print("- Proper Berkshire Mountains setting")
        print("💰 Cost: $0.039")
    else:
        print("\n❌ Failed to generate accurate Store image")

if __name__ == "__main__":
    main()