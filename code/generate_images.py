#!/usr/bin/env python3
"""
Auto-generate images for "The Chef at the Store" series using Google's nano-banana (Gemini 2.5 Flash Image).
This script reads page prompt files and generates illustrations via the Gemini API.
"""

import os
import time
import glob
import json
from pathlib import Path
from typing import Dict, List, Optional
import google.generativeai as genai
from datetime import datetime
import argparse
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file (check multiple locations)
load_dotenv()  # Current directory
load_dotenv("/Users/mjb9/Dropbox/scripts/coreybook/.env")  # coreybook directory

class StoryImageGenerator:
    def __init__(self, api_key: str, output_dir: str = "generated_images"):
        """
        Initialize the image generator.
        
        Args:
            api_key: Google AI API key for Gemini
            output_dir: Directory to save generated images
        """
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        # Use Gemini 2.5 Flash Image (Nano Banana) for image generation
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        # Rate limiting - Gemini API has limits
        self.request_delay = 2.0  # seconds between requests
        
        # Cost tracking ($0.039 per image)
        self.cost_per_image = 0.039
        self.generated_count = 0
        
        # Load reference images once (for future use)
        self.reference_images = {}
        
    def load_page_prompt(self, file_path: Path) -> Dict:
        """Load and parse a page prompt markdown file with new structure."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = lines[0].replace('# ', '') if lines else "Unknown Page"
        
        # In new format: image prompt is right after title, before first ## section
        image_prompt = ""
        page_text = ""
        
        # Parse the new format
        current_section = None
        capturing_image_prompt = True  # Start capturing right after title
        
        for i, line in enumerate(lines):
            if i == 0:  # Skip title line
                continue
            elif line.startswith("## PAGE TEXT"):
                current_section = "page_text"
                capturing_image_prompt = False
                continue
            elif line.startswith("## CHARACTER DESCRIPTIONS") or line.startswith("## SETTING DETAILS"):
                current_section = None
                capturing_image_prompt = False
                continue
            elif line.startswith("## "):
                current_section = None
                capturing_image_prompt = False
                continue
            
            # Capture image prompt (everything before first ## section)
            if capturing_image_prompt and line.strip():
                image_prompt += line.strip() + " "
            elif current_section == "page_text" and line.strip():
                page_text += line.strip() + " "
        
        return {
            'title': title.strip(),
            'page_text': page_text.strip(), 
            'image_prompt': image_prompt.strip(),
            'file_path': str(file_path)
        }
    
    def load_character_profiles(self, profiles_dir: str = "character-profiles") -> Dict:
        """Load character profile files for reference."""
        profiles = {}
        profiles_path = Path(profiles_dir)
        
        if not profiles_path.exists():
            return profiles
            
        for profile_file in profiles_path.glob("*.md"):
            char_name = profile_file.stem.upper()
            with open(profile_file, 'r', encoding='utf-8') as f:
                profiles[char_name] = f.read()
                
        return profiles
    
    def load_art_direction(self, art_file: str = "art-direction.md") -> str:
        """Load art direction guidelines."""
        art_path = Path(art_file)
        if art_path.exists():
            with open(art_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def create_enhanced_prompt(self, page_data: Dict, characters: Dict, art_direction: str) -> str:
        """Create a comprehensive prompt for image generation."""
        
        # Start with critical character consistency (MOST IMPORTANT)
        prompt = "CRITICAL: This is for a children's book series. Characters MUST look exactly the same in every illustration.\\n\\n"
        
        # Add the title
        prompt += f"Create an illustration for: {page_data['title']}\\n\\n"
        
        # Add art style direction first to set the tone
        prompt += f"ART STYLE:\\nModern 2D cartoon style (Phil Foglio influenced) with cel-shading, bold outlines, flat colors, clean prominent dark outlines, and expressive character designs.\\n\\n"
        
        # Add cartoon character references FIRST with stronger emphasis
        prompt += "CRITICAL CHARACTER CONSISTENCY - MUST MATCH REFERENCE IMAGES EXACTLY:\\n"
        prompt += "YOU MUST use these exact character designs from the reference images. Characters should look IDENTICAL to these references in every image:\\n\\n"
        
        prompt += "COREY WENTWORTH (MAIN CHARACTER - MOST IMPORTANT):\\n"
        prompt += "- MUST MATCH cartoon-characters/corey1.jpg EXACTLY\\n"
        prompt += "- COMPLETELY BALD HEAD (no hair whatsoever, smooth shiny bald dome)\\n"
        prompt += "- NO CHEF'S HAT - his baldness is a key character trait\\n"
        prompt += "- Large expressive eyes with thick dark eyebrows\\n"
        prompt += "- Round/oval face shape, warm friendly smile\\n"
        prompt += "- Always wears navy blue chef's apron over white shirt\\n"
        prompt += "- Medium build, friendly demeanor\\n"
        prompt += "- Phil Foglio cartoon style - exaggerated expressions\\n"
        prompt += "- CRITICAL: DO NOT add hair, stubble, hat, or change his appearance\\n\\n"
        
        prompt += "OTHER CHARACTERS (must also match references exactly):\\n"
        prompt += "- EMILY (wife): MUST MATCH cartoon-characters/emily.jpg - short silver pixie hair, black rectangular glasses, confident librarian\\n"
        prompt += "- REMI (son, 11): MUST MATCH cartoon-characters/remi.jpg - dark brown hair (not curly), pale/white skin tone, blue Super3 shirt, energetic CAUCASIAN WHITE BOY, non-identical twin to Oona\\n"
        prompt += "- OONA (daughter, 11): MUST MATCH cartoon-characters/Oona.jpg - long flowing honey blonde hair, pale/white skin tone, athletic CAUCASIAN WHITE GIRL, non-identical twin to Remi\\n"
        prompt += "- ZEPHYR (daughter, 9): MUST MATCH cartoon-characters/zephyr.jpg - smallest child, light brown hair, pale/white skin tone, biggest smile CAUCASIAN WHITE GIRL\\n"
        prompt += "- THE STORE: MUST MATCH cartoon-characters/store-cartoon.jpg - cream/yellow building with 4 white columns\\n"
        prompt += "- MATT (if appears): Reference cartoon-characters/matt.jpg but make him much thinner\\n\\n"
        
        # Add Super3 logo reference
        prompt += "SUPER3 LOGO (on children's shirts):\\n"
        prompt += "Red diamond shield with large yellow '3' in center, small letters 'Z', 'O', 'R' in corners. Reference: images/super3v3.png\\n\\n"
        
        prompt += "CRITICAL ETHNICITY REMINDER: ALL CHILDREN ARE CAUCASIAN WHITE with pale/light skin tones. Dark hair color does NOT indicate ethnicity - Remi has dark brown hair (NOT curly) BUT WHITE/PALE SKIN like his reference image. Remi and Oona are non-identical twins - same pale skin tone.\\n"
        prompt += "FINAL CHARACTER REMINDER: Study the reference images. Characters MUST be consistent throughout the book.\\n\\n"
        
        # NOW add the specific scene description
        prompt += f"SCENE TO ILLUSTRATE:\\n{page_data['image_prompt']}\\n\\n"
        
        # Add story context if available
        if page_data['page_text']:
            prompt += f"STORY TEXT FOR CONTEXT:\\n{page_data['page_text']}\\n\\n"
        
        # Final formatting instructions
        prompt += """FINAL REQUIREMENTS:
- Characters MUST match their reference images exactly
- Corey MUST be completely bald (no hair, no hat)
- IMPORTANT: All characters must have expressive, detailed eyeballs - never just dots for eyes
- Eyes should be large, expressive, and clearly defined with pupils and emotional detail
- 8x10.5 inch book illustration format
- High contrast for print reproduction
- Bold, saturated colors
- Expressive character poses and faces
- Maintain visual consistency throughout
- Include all story elements from the scene description"""
        
        return prompt.strip()

    def enhance_prompt_for_consistency(self, prompt: str) -> str:
        """Enhance prompt with stronger character consistency language."""
        
        # Replace character descriptions with enhanced versions
        enhanced_chars = {
            "completely BALD man, no hair, dark olive-green apron, white shirt, round friendly face": 
            "COREY: COMPLETELY BALD MALE CHEF (absolutely no hair, completely hairless scalp, shiny bald head), round friendly face with huge warm smile, medium build, dark olive-green kitchen apron over white shirt, Phil Foglio cartoon art style. MUST match this exact appearance every time",
            
            "woman with short silver pixie-cut hair, black glasses, gray hoodie, green shirt":
            "EMILY: ADULT WOMAN with distinctive SHORT SILVER PIXIE HAIR (styled, not messy), black rectangular glasses, gray hoodie over green shirt, confident expression, Phil Foglio cartoon art style. MUST match this exact appearance every time",
            
            "11-year-old boy, dark curly brown hair, blue shirt with red diamond \"3\" logo":
            "REMI: 11-YEAR-OLD CAUCASIAN WHITE BOY with distinctive DARK BROWN HAIR (not curly) and PALE/WHITE SKIN TONE, blue t-shirt with red diamond shield logo containing yellow number 3, Phil Foglio cartoon art style, non-identical twin to Oona. MUST match this exact appearance every time",
            
            "11-year-old girl, long honey blonde hair, blue shirt with red diamond \"3\" logo":
            "OONA: 11-YEAR-OLD CAUCASIAN WHITE GIRL with distinctive LONG HONEY BLONDE HAIR (wavy, past shoulders) and PALE/WHITE SKIN TONE, blue t-shirt with red diamond shield logo containing yellow number 3, Phil Foglio cartoon art style, non-identical twin to Remi. MUST match this exact appearance every time",
            
            "9-year-old girl, light brown shoulder-length hair, blue shirt with red diamond \"3\" logo, smallest child":
            "ZEPHYR: 9-YEAR-OLD CAUCASIAN WHITE GIRL (smallest of three children) with distinctive LIGHT BROWN SHOULDER-LENGTH HAIR and PALE/WHITE SKIN TONE, blue t-shirt with red diamond shield logo containing yellow number 3, Phil Foglio cartoon art style. MUST match this exact appearance every time"
        }
        
        # Apply character replacements
        enhanced_prompt = prompt
        for old_desc, new_desc in enhanced_chars.items():
            enhanced_prompt = enhanced_prompt.replace(old_desc, new_desc)
        
        # Add strong consistency reinforcement
        if "COREY" in enhanced_prompt:
            enhanced_prompt += " ABSOLUTELY CRITICAL: Corey must be completely bald with no hair whatsoever - shiny bald scalp is essential character trait."
        
        # Add art style consistency
        enhanced_prompt = enhanced_prompt.replace("2D cartoon illustration, cel-shading, Phil Foglio style", 
                                                "CONSISTENT 2D cartoon illustration with cel-shading, Phil Foglio art style with bold outlines and flat colors")
        
        return enhanced_prompt

    def create_text_layout_prompt(self, page_text: str, page_name: str) -> str:
        """Create a prompt for generating whimsical text layout."""
        
        # Clean the text and make it safe for AI generation
        clean_text = page_text.replace('"', "'").strip()
        
        # Split into individual words for emphasis
        words = clean_text.split()
        word_list = ", ".join([f'"{word}"' for word in words])
        
        prompt = f"""IMPORTANT: You are creating text typography art. The text must be EXACTLY as specified with NO changes, additions, or omissions.

Text to render (MUST be exact): "{clean_text}"

Individual words that MUST appear exactly: {word_list}

Typography design requirements:
- Create beautiful hand-lettered typography in children's book style
- Use playful, readable fonts with decorative elements
- Arrange text in an appealing layout with good spacing
- Use warm, inviting colors (oranges, yellows, soft reds, greens)
- Include decorative borders, flourishes, or small design elements
- Background should be simple (cream, light texture, or subtle pattern)
- Phil Foglio cartoon aesthetic with whimsical touches

ABSOLUTE REQUIREMENTS FOR TEXT ACCURACY:
- Every single word must be spelled exactly as provided
- No extra letters, missing letters, or changed letters
- No additional words or text beyond what is specified
- Punctuation must match exactly
- Capitalization must match exactly
- Word order must be preserved exactly

If you cannot render the text with 100% accuracy, create a simple typographic layout focusing on legibility over decoration."""
        
        return prompt
    
    def generate_image(self, prompt: str, output_path: Path, max_retries: int = 3) -> bool:
        """Generate a single image using Gemini nano-banana."""
        
        for attempt in range(max_retries):
            try:
                print(f"  Generating image (attempt {attempt + 1}/{max_retries})...")
                
                # Generate content with the model
                response = self.model.generate_content(prompt)
                
                # Check if the response contains an image
                if response.parts:
                    for part in response.parts:
                        if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                            # Check if it's actually an image by looking at mime_type
                            mime_type = getattr(part.inline_data, 'mime_type', '')
                            if mime_type.startswith('image/') or len(part.inline_data.data) > 1000:
                                # Save the raw data directly
                                with open(output_path, 'wb') as f:
                                    f.write(part.inline_data.data)
                                
                                self.generated_count += 1
                                file_size_mb = len(part.inline_data.data) / (1024 * 1024)
                                print(f"  ✅ Image saved: {output_path} ({file_size_mb:.1f} MB)")
                                return True
                
                print(f"  ❌ No image in response (attempt {attempt + 1})")
                    
            except Exception as e:
                print(f"  ❌ Error generating image (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(self.request_delay * 2)  # Wait longer on error
                    
        return False
    
    def generate_all_images(self, prompts_dir: str = "page-prompts", 
                          character_dir: str = "character-profiles",
                          start_page: int = 1, end_page: int = 50) -> None:
        """Generate images for all page prompts."""
        
        print(f"🎨 Starting image generation for pages {start_page}-{end_page} (56 total pages)")
        print(f"📁 Output directory: {self.output_dir}")
        
        # Load supporting files
        print("📚 Loading character profiles...")
        characters = self.load_character_profiles(character_dir)
        print(f"   Loaded {len(characters)} character profiles")
        
        print("🎭 Loading art direction...")
        art_direction = self.load_art_direction()
        print("   Art direction loaded" if art_direction else "   No art direction file found")
        
        # Find all page prompt files
        prompt_files = sorted(glob.glob(f"{prompts_dir}/page-*.md"))
        
        if not prompt_files:
            print(f"❌ No page prompt files found in {prompts_dir}")
            return
            
        print(f"📄 Found {len(prompt_files)} page prompt files")
        
        # Filter to requested page range (now includes covers)
        # Cover is page-00, story pages are 1-54, back cover is page-56
        total_pages = len(prompt_files)
        
        # Convert page numbers to indices (accounting for page-00-cover)
        if start_page == 0:  # Cover page
            start_idx = 0
        elif start_page >= 56:  # Back cover  
            start_idx = total_pages - 1
        else:  # Story pages 1-54
            start_idx = start_page  # page-01 is at index 1
            
        if end_page == 0:  # Cover page only
            end_idx = 1
        elif end_page >= 56:  # Include back cover
            end_idx = total_pages
        else:  # Story pages
            end_idx = min(total_pages - 1, end_page + 1)  # +1 because of page-00
        
        selected_files = prompt_files[start_idx:end_idx]
        print(f"🎯 Generating pages {start_page}-{min(end_page, total_pages)} ({len(selected_files)} files)")
        
        # Estimate cost
        estimated_cost = len(selected_files) * self.cost_per_image
        print(f"💰 Estimated cost: ${estimated_cost:.2f} ({len(selected_files)} images × ${self.cost_per_image})")
        
        # Generate images
        start_time = datetime.now()
        success_count = 0
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            
            # Create output filename  
            base_name = file_path.stem  # e.g., "page-01" or "page-00-cover"
            output_path = self.output_dir / f"{base_name}.png"
            
            if output_path.exists():
                print(f"⏭️  Skipping {base_name} (already exists)")
                continue
            
            print(f"\\n🖼️  [{i}/{len(selected_files)}] Processing {base_name}...")
            
            try:
                # Load page data
                page_data = self.load_page_prompt(file_path)
                print(f"   Title: {page_data['title']}")
                
                # Create enhanced prompt
                enhanced_prompt = self.create_enhanced_prompt(page_data, characters, art_direction)
                enhanced_prompt = self.enhance_prompt_for_consistency(enhanced_prompt)
                
                # Generate main illustration
                main_generated = False
                if self.generate_image(enhanced_prompt, output_path):
                    success_count += 1
                    main_generated = True
                else:
                    print(f"   ❌ Failed to generate image for {base_name}")
                
                # Generate text layout page (regardless of whether main image was generated)
                if page_data['page_text'].strip():
                    text_output_path = self.output_dir / f"{base_name}-text.png"
                    text_prompt = self.create_text_layout_prompt(page_data['page_text'], base_name)
                    if self.generate_image(text_prompt, text_output_path):
                        print(f"   ✅ Generated text layout: {base_name}-text.png")
                    else:
                        print(f"   ⚠️ Failed to generate text layout for {base_name}")
                
                # Rate limiting
                if i < len(selected_files):
                    print(f"   ⏳ Waiting {self.request_delay}s before next request...")
                    time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"   ❌ Error processing {base_name}: {str(e)}")
                continue
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        actual_cost = success_count * self.cost_per_image
        
        print(f"\\n📊 Generation Summary:")
        print(f"   ✅ Successful: {success_count}/{len(selected_files)}")
        print(f"   💰 Actual cost: ${actual_cost:.2f}")
        print(f"   ⏱️  Total time: {duration}")
        print(f"   📁 Images saved to: {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate images for The Chef at the Store series")
    parser.add_argument("--api-key", help="Google AI API key (or set GOOGLE_AI_API_KEY in .env)")
    parser.add_argument("--output", default="generated_images", help="Output directory")
    parser.add_argument("--prompts", default="page-prompts", help="Page prompts directory") 
    parser.add_argument("--characters", default="character-profiles", help="Character profiles directory")
    parser.add_argument("--start", type=int, default=1, help="Start page number")
    parser.add_argument("--end", type=int, default=56, help="End page number (56 for all including back cover)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests (seconds)")
    
    args = parser.parse_args()
    
    # Get API key from args or environment (try both variable names)
    api_key = args.api_key or os.getenv('GOOGLE_AI_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ API key is required!")
        print("   Set GOOGLE_AI_API_KEY or GEMINI_API_KEY in .env file or use --api-key argument")
        print("   Get one from: https://makersuite.google.com/app/apikey")
        return
    
    print(f"✅ API key found: {api_key[:20]}...")  # Show first 20 chars for verification
    
    # Create generator
    generator = StoryImageGenerator(api_key, args.output)
    generator.request_delay = args.delay
    
    # Generate images
    generator.generate_all_images(
        prompts_dir=args.prompts,
        character_dir=args.characters, 
        start_page=args.start,
        end_page=args.end
    )

if __name__ == "__main__":
    main()