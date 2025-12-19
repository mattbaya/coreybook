#!/usr/bin/env python3
"""
Fix cover, page 1, and page 2 to properly show the Store at Five Corners.
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

def generate_cover_with_store():
    """Generate cover with store-cartoon.jpg as background."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    cover_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio) in PHIL FOGLIO cartoon style.

Create the COVER for "The Chef at the Store" featuring the Wentworth family in front of THE STORE AT FIVE CORNERS.

**STORE BUILDING (CRITICAL - MUST MATCH):**
- Reference: cartoon-characters/store-cartoon.jpg
- Historic cream/pale yellow clapboard building
- Dark green shutters and front door
- 4 WHITE COLUMNS on front porch (two-story columns)
- "The Store at Five Corners" sign in gold lettering
- Glass sunroom addition on LEFT side
- Green awnings over windows
- Building should be bright, welcoming, restored

**TITLE TREATMENT:**
Top of cover in large, friendly lettering:
"The Chef at the Store"
Subtitle below: "Who Found So Much MORE!"

**THE WENTWORTH FAMILY (center foreground):**
Standing together in front of the Store:
- COREY: Completely BALD (no hair), navy blue apron, huge warm smile, center
- EMILY: Short silver pixie hair, black glasses, supportive expression, beside Corey
- REMI: 11yo boy, dark brown straight hair, blue Super3 shirt
- OONA: 11yo girl, long honey blonde hair, blue Super3 shirt
- ZEPHYR: 9yo girl, light brown hair, blue Super3 shirt
- All with Phil Foglio style exaggerated happy expressions

**COMPOSITION:**
- Store building fills background, bright and inviting
- Family grouped together in foreground
- Title at top, subtitle below
- Five roads visible converging at the intersection
- Berkshire Mountains in distance
- Warm, welcoming atmosphere

**PHIL FOGLIO STYLE:**
- Thick black outlines with hand-drawn feel
- Exaggerated expressions (huge smiles, wide eyes)
- Dynamic poses even in family portrait
- Whimsical details throughout
- Bold, saturated colors

The Store should look restored and successful (not sad) as this is the cover showing the happy ending/new beginning.
"""
    
    print("📚 Generating cover with Store at Five Corners...")
    
    try:
        response = model.generate_content(cover_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/Cover_with_store.jpg")
                        image.save(output_path, quality=95)
                        print(f"✅ Generated cover with Store: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating cover: {e}")
        return False

def generate_page1_sad_store():
    """Generate page 1 with sad/drab version of the Store."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    page1_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio) in PHIL FOGLIO cartoon style.

Create a Phil Foglio style illustration of THE STORE AT FIVE CORNERS looking abandoned and sad.

**STORE BUILDING (CRITICAL - MUST MATCH but SAD):**
- Reference: cartoon-characters/store-cartoon.jpg
- Same historic cream/yellow building BUT:
  - Paint peeling and faded
  - Green shutters hanging crooked
  - Dusty, dirty windows with cobwebs
  - "The Store at Five Corners" sign weathered/faded
  - Small crooked "CLOSED" sign in window
  - 4 white columns still there but need paint
  - Weeds growing around foundation
  - Overall neglected appearance

**ATMOSPHERE:**
- Gray, melancholy sky (not threatening, just sad)
- Empty parking area with a few scattered leaves
- Five roads stretching away, all empty
- Red barn visible across street, also looking lonely
- Berkshire Mountains in background under gray clouds

**PHIL FOGLIO TOUCHES:**
- Even sad buildings have character in his style
- Slightly exaggerated decay (comically crooked shutters)
- Building has a "waiting to be loved" quality
- Thick black outlines, hand-drawn feel
- Muted colors but still recognizable

**NO PEOPLE** - just the lonely, abandoned Store waiting at the crossroads.

The building should look neglected but structurally sound - it's been closed, not destroyed. Like a character waiting for someone to bring it back to life.
"""
    
    print("🏚️ Generating page 1 with sad Store...")
    
    try:
        response = model.generate_content(page1_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page1_sad_store.jpg")
                        image.save(output_path, quality=95)
                        print(f"✅ Generated page 1 sad Store: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 1: {e}")
        return False

def generate_page2_corey_arriving():
    """Generate page 2 with Corey arriving with cart of supplies."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-image')
    
    page2_prompt = """CRITICAL: Generate as a PERFECT SQUARE image (1:1 aspect ratio) in PHIL FOGLIO cartoon style.

Create a Phil Foglio style illustration of COREY arriving at the Store with an overflowing cart of cooking supplies.

**COREY (protagonist):**
- Completely BALD (no hair at all)
- Huge excited smile, stars in eyes
- Navy blue apron already on
- Pulling/pushing a wheeled cart
- Expression shows determination and joy
- Phil Foglio style exaggerated enthusiasm

**THE OVERFLOWING CART:**
Comically overstuffed with cooking supplies:
- Spatulas sticking out at all angles (multiple types)
- Stack of cookbooks teetering on top
- Whisks poking out
- Mixing bowls nested and stacked high
- Measuring cups dangling
- Rolling pin
- Chef's knives (safely sheathed)
- Cutting boards
- Cast iron pans
- Maybe a rubber chicken for humor
- Items should be falling off/barely balanced

**THE STORE (background):**
- Same building from page 1 but with golden sunlight
- Ray of sunshine breaking through clouds
- Illuminating the Store like destiny
- Still has "CLOSED" sign but Corey doesn't care
- Green front door he's heading toward

**PHIL FOGLIO STYLE ELEMENTS:**
- Motion lines showing Corey's movement
- Some items falling from cart with action lines
- Exaggerated perspective on the pile of supplies
- Thick black outlines
- Dynamic composition with tilted angles
- Comic energy and movement

**ATMOSPHERE:**
- Hopeful golden light on the Store
- Corey's enthusiasm contrasts with quiet building
- Sense of "this is meant to be"
- A few curious townspeople peeking from behind trees

The scene captures the moment of new beginning - one determined chef with too many supplies and infinite optimism approaching his destiny.
"""
    
    print("🛒 Generating page 2 with Corey arriving...")
    
    try:
        response = model.generate_content(page2_prompt)
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    
                    if image.width == image.height:
                        output_path = Path("cartoon-characters/leonardo/page2_corey_cart.jpg")
                        image.save(output_path, quality=95)
                        print(f"✅ Generated page 2 Corey with cart: {image.width}x{image.height}")
                        return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating page 2: {e}")
        return False

def main():
    """Fix cover and early pages."""
    print("🎨 Fixing cover and early pages with correct Store imagery...\n")
    
    success_count = 0
    
    # Generate cover
    if generate_cover_with_store():
        success_count += 1
        time.sleep(3)
    
    # Generate page 1
    if generate_page1_sad_store():
        success_count += 1
        time.sleep(3)
    
    # Generate page 2
    if generate_page2_corey_arriving():
        success_count += 1
    
    print(f"\n✅ Generated {success_count}/3 corrected pages")
    print(f"💰 Total cost: ${success_count * 0.039:.2f}")
    
    if success_count == 3:
        print("\n🎯 Success! Cover and early pages now properly show the Store at Five Corners")
        print("- Cover: Family in front of restored Store")
        print("- Page 1: Sad, abandoned Store waiting")  
        print("- Page 2: Corey arriving with overflowing cart of supplies")

if __name__ == "__main__":
    main()