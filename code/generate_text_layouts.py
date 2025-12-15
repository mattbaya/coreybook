#!/usr/bin/env python3
"""
Generate just the text layouts with improved accuracy.
"""

import os
import time
import glob
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import argparse

# Load environment variables
load_dotenv()

class TextLayoutGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.output_dir = Path("generated_images")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        self.request_delay = 2.0

    def load_page_prompt(self, file_path: Path):
        """Load page text from markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = lines[0].replace('# ', '') if lines else "Unknown Page"
        
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
        
        return {
            'title': title.strip(),
            'page_text': page_text.strip(),
            'file_path': str(file_path)
        }

    def create_text_layout_prompt(self, page_text: str) -> str:
        """Create improved prompt for accurate text rendering."""
        clean_text = page_text.replace('"', "'").strip()
        
        # Split into words for emphasis
        words = clean_text.split()
        word_list = ", ".join([f'"{word}"' for word in words])
        
        prompt = f"""TYPOGRAPHY ACCURACY MISSION: Create text art with PERFECT spelling and NO REPETITION.

EXACT TEXT TO RENDER: "{clean_text}"

REQUIRED WORDS (each must appear exactly ONCE): {word_list}

Design as beautiful typography:
- Hand-lettered children's book style
- Warm colors (soft oranges, yellows, greens)
- Simple decorative elements (stars, hearts, swirls)
- Clean, readable layout
- Cream or light background

CRITICAL SPELLING RULES:
- Every letter must be exactly correct
- No extra or missing letters
- No made-up words
- Punctuation must match exactly
- Word order must be preserved
- NO REPETITION: Each word/phrase should appear only ONCE
- Do not duplicate any text elements

Focus on accuracy over decoration. Better to have plain, correct text than fancy, wrong text."""
        
        return prompt

    def generate_text_layout(self, prompt: str, output_path: Path) -> bool:
        """Generate a single text layout."""
        try:
            print(f"  Generating text layout...")
            response = self.model.generate_content(prompt)
            
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        with open(output_path, 'wb') as f:
                            f.write(part.inline_data.data)
                        
                        file_size_mb = len(part.inline_data.data) / (1024 * 1024)
                        print(f"  ✅ Text layout saved: {output_path} ({file_size_mb:.1f} MB)")
                        return True
            
            print(f"  ❌ No image data in response")
            return False
            
        except Exception as e:
            print(f"  ❌ Error generating text layout: {e}")
            return False

    def process_pages(self, start_page: int = 1, end_page: int = 56):
        """Generate text layouts for specified pages."""
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
        
        print(f"🎨 Generating text layouts for pages {start_page}-{end_page}")
        print(f"📄 Found {len(selected_files)} page files")
        
        success_count = 0
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            base_name = file_path.stem
            
            print(f"\n📝 [{i}/{len(selected_files)}] Processing {base_name} text layout...")
            
            try:
                # Load page data
                page_data = self.load_page_prompt(file_path)
                
                if not page_data['page_text'].strip():
                    print(f"  ⏭️ No text found for {base_name}")
                    continue
                
                print(f"   Text: {page_data['page_text'][:50]}...")
                
                # Create text layout
                text_output_path = self.output_dir / f"{base_name}-text.png"
                text_prompt = self.create_text_layout_prompt(page_data['page_text'])
                
                if self.generate_text_layout(text_prompt, text_output_path):
                    success_count += 1
                
                # Rate limiting
                if i < len(selected_files):
                    print(f"   ⏳ Waiting {self.request_delay}s...")
                    time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"❌ Error processing {base_name}: {e}")
        
        print(f"\n📊 Text Layout Summary:")
        print(f"   ✅ Generated: {success_count}/{len(selected_files)}")

def main():
    parser = argparse.ArgumentParser(description='Generate text layouts only')
    parser.add_argument('--start', type=int, default=1, help='Starting page number')
    parser.add_argument('--end', type=int, default=56, help='Ending page number')
    parser.add_argument('--api-key', default=os.getenv('GEMINI_API_KEY'), help='Gemini API key')
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ No API key provided. Set GEMINI_API_KEY or use --api-key")
        return
    
    generator = TextLayoutGenerator(args.api_key)
    generator.process_pages(args.start, args.end)

if __name__ == "__main__":
    main()