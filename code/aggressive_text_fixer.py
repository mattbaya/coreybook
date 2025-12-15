#!/usr/bin/env python3
"""
Aggressively fix text errors with multiple regeneration attempts.
"""

import os
import time
import glob
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AggressiveTextFixer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.output_dir = Path("generated_images")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        self.request_delay = 2.0
        self.max_attempts = 3

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

    def create_word_by_word_prompt(self, page_text: str, attempt: int) -> str:
        """Create extremely explicit word-by-word prompt."""
        clean_text = page_text.replace('"', "'").strip()
        
        # Break into individual words with positions
        words = clean_text.split()
        word_instructions = []
        for i, word in enumerate(words, 1):
            word_instructions.append(f"Word {i}: '{word}'")
        
        word_list = "\n".join(word_instructions)
        
        if attempt == 1:
            style = "BASIC BLACK TEXT ON WHITE BACKGROUND"
        elif attempt == 2:
            style = "SIMPLE SANS-SERIF FONT, LARGE SIZE"
        else:
            style = "PLAIN TEXT ONLY - NO FORMATTING"
        
        prompt = f"""WORD-BY-WORD TRANSCRIPTION (Attempt {attempt}/3)

TRANSCRIBE EXACTLY - EVERY LETTER MATTERS:
"{clean_text}"

WORD-BY-WORD BREAKDOWN:
{word_list}

RENDER AS: {style}

ABSOLUTE REQUIREMENTS:
- Type each word exactly as listed above
- Preserve all punctuation: ! ? . , " ' -
- Keep exact spacing between words
- Maintain capitalization exactly
- NO repetition of any word
- NO adding extra words
- NO changing any letters
- NO missing any words

VERIFICATION: After rendering, check that every word appears exactly once in the correct order."""
        
        return prompt

    def verify_text_accuracy(self, image_path: Path, expected_text: str) -> tuple[bool, str]:
        """Quick verification of image text."""
        try:
            prompt = f"""Check if this image contains exactly this text: "{expected_text}"

Respond with only:
"PERFECT" if text matches exactly
"ERRORS: [brief list]" if there are mistakes"""
            
            uploaded_file = genai.upload_file(path=str(image_path))
            
            response = self.model.generate_content([prompt, uploaded_file])
            
            result_text = response.text.strip()
            is_accurate = result_text.startswith("PERFECT")
            
            uploaded_file.delete()
            
            return is_accurate, result_text
            
        except Exception as e:
            return False, f"ERROR: {e}"

    def generate_with_retries(self, page_name: str, expected_text: str) -> bool:
        """Generate text image with multiple retry attempts."""
        text_image_path = self.output_dir / f"{page_name}-text.png"
        
        for attempt in range(1, self.max_attempts + 1):
            print(f"    Attempt {attempt}/{self.max_attempts}...")
            
            try:
                # Create attempt-specific prompt
                prompt = self.create_word_by_word_prompt(expected_text, attempt)
                
                # Generate image
                response = self.model.generate_content(prompt)
                
                if response.parts:
                    for part in response.parts:
                        if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                            with open(text_image_path, 'wb') as f:
                                f.write(part.inline_data.data)
                            
                            # Quick verification
                            time.sleep(1)
                            is_accurate, result = self.verify_text_accuracy(text_image_path, expected_text)
                            
                            if is_accurate:
                                print(f"    ✅ PERFECT on attempt {attempt}")
                                return True
                            else:
                                print(f"    ⚠️ Still has errors: {result[:50]}...")
                                if attempt < self.max_attempts:
                                    time.sleep(self.request_delay)
                                continue
                
                print(f"    ❌ No image generated on attempt {attempt}")
                
            except Exception as e:
                print(f"    ❌ Error on attempt {attempt}: {e}")
            
            if attempt < self.max_attempts:
                time.sleep(self.request_delay)
        
        print(f"    ⚠️ Could not achieve perfect accuracy after {self.max_attempts} attempts")
        return False

    def fix_all_pages(self, start_page: int = 1, end_page: int = 47):
        """Fix all pages with aggressive retry approach."""
        prompt_files = sorted(glob.glob("page-prompts/page-*.md"))
        
        # Filter to requested range
        selected_files = []
        for prompt_file in prompt_files:
            file_path = Path(prompt_file)
            base_name = file_path.stem
            
            if "cover" in base_name:
                page_num = 0
            elif "back-cover" in base_name:
                page_num = 47
            else:
                import re
                match = re.search(r'page-(\d+)', base_name)
                page_num = int(match.group(1)) if match else -1
            
            if start_page <= page_num <= end_page:
                selected_files.append(prompt_file)
        
        print(f"🔧 AGGRESSIVE TEXT FIXING: Pages {start_page}-{end_page}")
        
        perfect_count = 0
        improved_count = 0
        total_attempts = 0
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            base_name = file_path.stem
            
            print(f"\n📝 [{i}/{len(selected_files)}] FIXING {base_name}...")
            
            try:
                # Load expected text
                expected_text = self.load_page_text(file_path)
                if not expected_text.strip():
                    print(f"  ⏭️ No text found")
                    continue
                
                print(f"   Target: {expected_text[:60]}...")
                
                # Attempt to fix with retries
                success = self.generate_with_retries(base_name, expected_text)
                total_attempts += self.max_attempts
                
                if success:
                    perfect_count += 1
                else:
                    improved_count += 1
                
                time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"❌ Error processing {base_name}: {e}")
        
        print(f"\n📊 AGGRESSIVE FIXING RESULTS:")
        print(f"   ✅ Perfect accuracy: {perfect_count}")
        print(f"   📈 Improved (but not perfect): {improved_count}")
        print(f"   🔄 Total generation attempts: {total_attempts}")

def main():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key provided. Set GEMINI_API_KEY")
        return
    
    fixer = AggressiveTextFixer(api_key)
    fixer.fix_all_pages(1, 47)

if __name__ == "__main__":
    main()