#!/usr/bin/env python3
"""
Verify text accuracy in generated images and regenerate if needed.
"""

import os
import time
import glob
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TextVerifier:
    def __init__(self, api_key):
        self.api_key = api_key
        self.output_dir = Path("generated_images")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        self.request_delay = 2.0

    def load_page_text(self, file_path: Path):
        """Load expected page text from markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        page_text = ""
        in_page_text = False
        
        for line in lines:
            if line.startswith("## PAGE TEXT"):
                in_page_text = True
                continue
            elif line.startswith("## "):
                in_page_text = False
                continue
            
            if in_page_text and line.strip():
                page_text += line.strip() + " "
        
        return page_text.strip()

    def create_verification_prompt(self, expected_text: str) -> str:
        """Create prompt to verify text accuracy in image."""
        return f"""ACCURACY CHECK: Compare the text in this image to the expected text below.

EXPECTED TEXT: "{expected_text}"

Please examine the image carefully and report:
1. Is ALL text spelled correctly? 
2. Are there any missing words, letters, or punctuation?
3. Are there any extra words, letters, or punctuation?
4. Is the word order exactly correct?

Respond with:
- "ACCURATE" if the text matches perfectly
- "ERRORS: [list specific problems]" if there are mistakes

Focus only on text accuracy, not visual design."""

    def create_regeneration_prompt(self, page_text: str) -> str:
        """Create improved prompt for regenerating text."""
        clean_text = page_text.replace('"', "'").strip()
        
        # Split into words for emphasis
        words = clean_text.split()
        word_list = ", ".join([f'"{word}"' for word in words])
        
        prompt = f"""TEXT ACCURACY MISSION: Create SIMPLE, PERFECTLY SPELLED text.

EXACT TEXT TO RENDER: "{clean_text}"

REQUIRED WORDS (each must appear exactly ONCE): {word_list}

ULTRA-LEGIBLE REQUIREMENTS:
- Very large, bold, clear font
- High contrast black text on white/cream background
- Simple sans-serif font (Arial, Helvetica style)
- NO decorative elements or illustrations
- Clean white background
- Generous spacing between lines
- Text centered and fills most of image

SPELLING ACCURACY RULES:
- Copy EVERY letter, punctuation mark, and space exactly
- Preserve ALL quotation marks, exclamation points, commas
- Keep exact word order and capitalization
- NO REPETITION: Each word appears only ONCE
- Double-check every letter before finalizing

PRIORITY: Perfect spelling over everything else."""
        
        return prompt

    def verify_image_accuracy(self, image_path: Path, expected_text: str) -> tuple[bool, str]:
        """Verify if image text matches expected text."""
        try:
            verification_prompt = self.create_verification_prompt(expected_text)
            
            # Upload and analyze image
            uploaded_file = genai.upload_file(path=str(image_path))
            
            response = self.model.generate_content([
                verification_prompt,
                uploaded_file
            ])
            
            result_text = response.text.strip()
            is_accurate = result_text.startswith("ACCURATE")
            
            # Clean up uploaded file
            uploaded_file.delete()
            
            return is_accurate, result_text
            
        except Exception as e:
            print(f"  ❌ Error verifying image: {e}")
            return False, f"ERROR: {e}"

    def regenerate_text_image(self, prompt: str, output_path: Path) -> bool:
        """Regenerate text image with improved accuracy."""
        try:
            print(f"  🔄 Regenerating with improved accuracy...")
            response = self.model.generate_content(prompt)
            
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        with open(output_path, 'wb') as f:
                            f.write(part.inline_data.data)
                        
                        file_size_mb = len(part.inline_data.data) / (1024 * 1024)
                        print(f"  ✅ Regenerated: {output_path} ({file_size_mb:.1f} MB)")
                        return True
            
            print(f"  ❌ No image data in regeneration response")
            return False
            
        except Exception as e:
            print(f"  ❌ Error regenerating: {e}")
            return False

    def verify_and_fix_pages(self, start_page: int = 1, end_page: int = 41):
        """Verify all text images and fix any with errors."""
        prompt_files = sorted(glob.glob("page-prompts/page-*.md"))
        
        # Filter to requested range
        selected_files = []
        for prompt_file in prompt_files:
            file_path = Path(prompt_file)
            base_name = file_path.stem
            
            if "cover" in base_name:
                page_num = 0
            else:
                import re
                match = re.search(r'page-(\d+)', base_name)
                page_num = int(match.group(1)) if match else -1
            
            if start_page <= page_num <= end_page:
                selected_files.append(prompt_file)
        
        print(f"🔍 Verifying text accuracy for pages {start_page}-{end_page}")
        
        verified_count = 0
        fixed_count = 0
        errors_found = []
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            base_name = file_path.stem
            text_image_path = self.output_dir / f"{base_name}-text.png"
            
            print(f"\n📝 [{i}/{len(selected_files)}] Checking {base_name}...")
            
            # Skip if no text image exists
            if not text_image_path.exists():
                print(f"  ⏭️ No text image found")
                continue
            
            try:
                # Load expected text
                expected_text = self.load_page_text(file_path)
                if not expected_text.strip():
                    print(f"  ⏭️ No text found in source")
                    continue
                
                print(f"   Expected: {expected_text[:50]}...")
                
                # Verify accuracy
                is_accurate, verification_result = self.verify_image_accuracy(text_image_path, expected_text)
                
                if is_accurate:
                    print(f"  ✅ ACCURATE")
                    verified_count += 1
                else:
                    print(f"  ❌ ERRORS FOUND: {verification_result}")
                    errors_found.append(f"{base_name}: {verification_result}")
                    
                    # Regenerate with improved prompt
                    regeneration_prompt = self.create_regeneration_prompt(expected_text)
                    
                    if self.regenerate_text_image(regeneration_prompt, text_image_path):
                        fixed_count += 1
                        
                        # Verify the fix worked
                        time.sleep(2)  # Wait before re-verification
                        is_fixed, verify_result = self.verify_image_accuracy(text_image_path, expected_text)
                        
                        if is_fixed:
                            print(f"  ✅ FIXED successfully")
                        else:
                            print(f"  ⚠️ Still has issues: {verify_result}")
                
                # Rate limiting
                time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"❌ Error processing {base_name}: {e}")
        
        print(f"\n📊 Verification Summary:")
        print(f"   ✅ Verified accurate: {verified_count}")
        print(f"   🔄 Fixed errors: {fixed_count}")
        if errors_found:
            print(f"   ❌ Errors found:")
            for error in errors_found:
                print(f"      {error}")

def main():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key provided. Set GEMINI_API_KEY")
        return
    
    verifier = TextVerifier(api_key)
    verifier.verify_and_fix_pages(1, 41)

if __name__ == "__main__":
    main()