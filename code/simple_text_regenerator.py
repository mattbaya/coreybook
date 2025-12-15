#!/usr/bin/env python3
"""
Simple text regeneration with focus on common problematic pages.
"""

import os
import time
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleTextRegenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.output_dir = Path("generated_images")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        self.request_delay = 3.0

    def create_simple_prompt(self, page_text: str) -> str:
        """Create very simple, clean prompt."""
        clean_text = page_text.replace('"', "'").strip()
        
        prompt = f"""Create simple text image:

TEXT: {clean_text}

STYLE: Plain black text on white background, large readable font, centered.

Make text clear and spell every word correctly."""
        
        return prompt

    def generate_text_image(self, prompt: str, output_path: Path) -> bool:
        """Generate a single text image."""
        try:
            response = self.model.generate_content(prompt)
            
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        with open(output_path, 'wb') as f:
                            f.write(part.inline_data.data)
                        
                        file_size_mb = len(part.inline_data.data) / (1024 * 1024)
                        print(f"  ✅ Generated: {output_path} ({file_size_mb:.1f} MB)")
                        return True
            
            print(f"  ❌ No image data in response")
            return False
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False

    def regenerate_priority_pages(self):
        """Regenerate the most problematic pages we know have errors."""
        
        # Additional problematic pages with their expected text
        priority_pages = {
            "page-03": "So he scrubbed and he polished from ceiling to floor, He hung up a sign that said 'GRAND OPENING SOON!' And 'We've got everything here that you'll ever need!' 'Come on in!' the sign shouted. 'Come see what we've got! Come and be happy! Come READY or NOT! Come one! Come all! We want all of you!'",
            
            "page-04": "For three wonderful years, Corey cooked in that place. He served up his bagels and scones with a smile on his face. YELP filled up with love, many customers thought, 'Life in the MOUNTAINS doesn't GET better than this!'",
            
            "page-06": "The tablet glowed bright with review after review, Each one more delightful than the last one he knew! The nicest reviews that he'd ever seen! From 'Captain of this ship' to 'Best croissant in life'— He couldn't wait to share this with Emily, his wife! 'Four years of work and the dream is now PACKED! The folks are all talking and our café's on track!'",
            
            "page-08": "But the money was tight—oh, so terribly tight! He'd count up his pennies by dim kitchen light. But his dream still lived! It would fly like a bird to the sky!",
            
            "page-12": "And Corey sat down in the quiet café, Convinced that his dream had just slipped away. The roundabout project had won the day.",
            
            "page-13": "Now Corey must go, though it hurt quite a lot. He whispered, 'Goodbye to this beautiful spot.' He stood there alone as the sun sank away. At the end of his final and difficult day?"
        }
        
        print("🔧 SIMPLE REGENERATION: Priority pages with known errors")
        
        success_count = 0
        
        for page_name, expected_text in priority_pages.items():
            print(f"\n📝 Regenerating {page_name}...")
            print(f"   Text: {expected_text[:60]}...")
            
            try:
                text_image_path = self.output_dir / f"{page_name}-text.png"
                prompt = self.create_simple_prompt(expected_text)
                
                if self.generate_text_image(prompt, text_image_path):
                    success_count += 1
                
                # Rate limiting
                time.sleep(self.request_delay)
                    
            except Exception as e:
                print(f"❌ Error processing {page_name}: {e}")
        
        print(f"\n📊 SIMPLE REGENERATION RESULTS:")
        print(f"   ✅ Successfully regenerated: {success_count}/{len(priority_pages)}")

def main():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No API key provided. Set GEMINI_API_KEY")
        return
    
    regenerator = SimpleTextRegenerator(api_key)
    regenerator.regenerate_priority_pages()

if __name__ == "__main__":
    main()