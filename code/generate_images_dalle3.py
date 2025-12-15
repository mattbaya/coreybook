#!/usr/bin/env python3
"""
Auto-generate images for "The Chef at the Store" using OpenAI's DALL-E 3.
DALL-E 3 has better text rendering and character consistency than many other models.
"""

import os
import time
import glob
import json
from pathlib import Path
from typing import Dict, List, Optional
import openai
from datetime import datetime
import argparse
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class StoryImageGeneratorDALLE3:
    def __init__(self, api_key: str, output_dir: str = "generated_images"):
        """
        Initialize the DALL-E 3 image generator.
        
        Args:
            api_key: OpenAI API key
            output_dir: Directory to save generated images
        """
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up OpenAI client
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        
        # Rate limiting
        self.request_delay = 1.0  # seconds between requests
        
        # Cost tracking
        self.cost_per_image = {
            "standard": 0.040,  # 1024x1024 standard quality
            "hd": 0.080,        # 1024x1024 HD quality
            "hd_wide": 0.120    # 1024x1792 HD quality
        }
        self.generated_count = 0
        self.total_cost = 0.0
        
    def load_page_prompt(self, file_path: Path) -> Dict:
        """Load and parse a page prompt markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = lines[0].replace('# ', '') if lines else "Unknown Page"
        
        # Find PAGE TEXT section
        page_text = ""
        image_prompt = ""
        
        in_page_text = False
        in_image_prompt = False
        
        for line in lines:
            if line.startswith("## PAGE TEXT"):
                in_page_text = True
                in_image_prompt = False
                continue
            elif line.startswith("## IMAGE PROMPT"):
                in_page_text = False
                in_image_prompt = True
                continue
            elif line.startswith("## "):
                in_page_text = False
                in_image_prompt = False
                continue
            
            if in_page_text and line.strip():
                page_text += line.strip() + " "
            elif in_image_prompt and line.strip() and not line.startswith("**Art Style**"):
                image_prompt += line.strip() + " "
        
        return {
            'title': title.strip(),
            'page_text': page_text.strip(), 
            'image_prompt': image_prompt.strip(),
            'file_path': str(file_path)
        }
    
    def create_dalle3_prompt(self, page_data: Dict) -> str:
        """Create an optimized prompt for DALL-E 3."""
        
        # DALL-E 3 specific prompt structure
        prompt = "Children's book illustration in Phil Foglio cartoon style with cel-shading.\n\n"
        
        # Critical character consistency
        prompt += "IMPORTANT CHARACTER DESIGNS (maintain exact consistency):\n"
        prompt += "- COREY: Completely bald chef (no hair at all), round friendly face, navy blue apron\n"
        prompt += "- EMILY: Short silver pixie hair, black glasses, librarian style\n"
        prompt += "- CHILDREN: All wear red diamond 'Super3' shirts with yellow '3'\n"
        prompt += "- STORE: Cream/yellow building with 4 white columns\n\n"
        
        # Scene description
        prompt += f"SCENE: {page_data['image_prompt']}\n\n"
        
        # Text rendering instructions (DALL-E 3 is better at this)
        if "sign" in page_data['image_prompt'].lower() or "text" in page_data['image_prompt'].lower():
            prompt += "TEXT RENDERING: Ensure all text is clearly legible and spelled correctly.\n\n"
        
        # Page text for context
        if page_data['page_text']:
            prompt += f"STORY CONTEXT: {page_data['page_text'][:200]}...\n\n"
        
        # Final requirements
        prompt += "Style: Modern 2D cartoon, bold outlines, vibrant colors, expressive characters, consistent designs throughout."
        
        return prompt
    
    def generate_image(self, prompt: str, output_path: Path, quality: str = "standard", size: str = "1024x1024") -> bool:
        """Generate a single image using DALL-E 3."""
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"  Generating image (attempt {attempt + 1}/{max_retries})...")
                print(f"  Quality: {quality}, Size: {size}")
                
                # Generate image using DALL-E 3
                response = self.client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    n=1,
                    style="vivid"  # "vivid" for more creative, "natural" for more realistic
                )
                
                # Get the image URL
                image_url = response.data[0].url
                
                # Download the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(image_response.content)
                    
                    self.generated_count += 1
                    
                    # Calculate cost
                    if quality == "hd" and size == "1024x1792":
                        cost = self.cost_per_image["hd_wide"]
                    elif quality == "hd":
                        cost = self.cost_per_image["hd"]
                    else:
                        cost = self.cost_per_image["standard"]
                    
                    self.total_cost += cost
                    
                    file_size_mb = len(image_response.content) / (1024 * 1024)
                    print(f"  ✅ Image saved: {output_path} ({file_size_mb:.1f} MB)")
                    print(f"  💰 Cost: ${cost:.3f}")
                    
                    # Also save the revised prompt if provided
                    if response.data[0].revised_prompt:
                        revised_path = output_path.with_suffix('.txt')
                        with open(revised_path, 'w') as f:
                            f.write(f"Original prompt:\n{prompt}\n\n")
                            f.write(f"Revised prompt:\n{response.data[0].revised_prompt}")
                    
                    return True
                
                print(f"  ❌ Failed to download image (attempt {attempt + 1})")
                    
            except Exception as e:
                print(f"  ❌ Error generating image (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(self.request_delay * 2)
                    
        return False
    
    def generate_all_images(self, prompts_dir: str = "page-prompts", 
                          start_page: int = 0, end_page: int = 56,
                          quality: str = "standard", size: str = "1024x1024") -> None:
        """Generate images for all page prompts using DALL-E 3."""
        
        print(f"🎨 Starting DALL-E 3 image generation for pages {start_page}-{end_page}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🎨 Quality: {quality}, Size: {size}")
        
        # Find all page prompt files
        prompt_files = sorted(glob.glob(f"{prompts_dir}/page-*.md"))
        
        if not prompt_files:
            print(f"❌ No page prompt files found in {prompts_dir}")
            return
            
        print(f"📄 Found {len(prompt_files)} page prompt files")
        
        # Filter to requested page range
        if start_page == 0:
            start_idx = 0
        else:
            start_idx = start_page
            
        if end_page >= 56:
            end_idx = len(prompt_files)
        else:
            end_idx = end_page + 1
        
        selected_files = prompt_files[start_idx:end_idx]
        print(f"🎯 Generating {len(selected_files)} images")
        
        # Estimate cost
        if quality == "hd" and size == "1024x1792":
            cost_per = self.cost_per_image["hd_wide"]
        elif quality == "hd":
            cost_per = self.cost_per_image["hd"]
        else:
            cost_per = self.cost_per_image["standard"]
            
        estimated_cost = len(selected_files) * cost_per
        print(f"💰 Estimated cost: ${estimated_cost:.2f} ({len(selected_files)} images × ${cost_per})")
        
        # Generate images
        start_time = datetime.now()
        success_count = 0
        
        for i, prompt_file in enumerate(selected_files, 1):
            file_path = Path(prompt_file)
            base_name = file_path.stem
            output_path = self.output_dir / f"{base_name}.png"
            
            # Create old versions folder if needed
            old_versions_dir = self.output_dir / "old_versions"
            old_versions_dir.mkdir(exist_ok=True)
            
            # Move existing file to old versions
            if output_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                old_path = old_versions_dir / f"{base_name}_{timestamp}.png"
                output_path.rename(old_path)
                print(f"  📁 Moved existing to: {old_path}")
            
            print(f"\n🖼️  [{i}/{len(selected_files)}] Processing {base_name}...")
            
            try:
                # Load page data
                page_data = self.load_page_prompt(file_path)
                print(f"   Title: {page_data['title']}")
                
                # Create DALL-E 3 optimized prompt
                dalle3_prompt = self.create_dalle3_prompt(page_data)
                
                # Generate image
                if self.generate_image(dalle3_prompt, output_path, quality, size):
                    success_count += 1
                else:
                    print(f"   ❌ Failed to generate image for {base_name}")
                
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
        
        print(f"\n📊 Generation Summary:")
        print(f"   ✅ Successful: {success_count}/{len(selected_files)}")
        print(f"   💰 Actual cost: ${self.total_cost:.2f}")
        print(f"   ⏱️  Total time: {duration}")
        print(f"   📁 Images saved to: {self.output_dir}")
        print(f"\n💡 TIP: DALL-E 3 saves revised prompts as .txt files next to images")

def main():
    parser = argparse.ArgumentParser(description="Generate images using OpenAI DALL-E 3")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY in .env)")
    parser.add_argument("--output", default="generated_images", help="Output directory")
    parser.add_argument("--start", type=int, default=0, help="Start page number (0 for cover)")
    parser.add_argument("--end", type=int, default=2, help="End page number")
    parser.add_argument("--quality", choices=["standard", "hd"], default="standard", 
                      help="Image quality (standard=$0.04, hd=$0.08)")
    parser.add_argument("--size", choices=["1024x1024", "1024x1792", "1792x1024"], 
                      default="1024x1024", help="Image size")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OpenAI API key is required!")
        print("   Set OPENAI_API_KEY in .env file or use --api-key argument")
        return
    
    print(f"✅ OpenAI API key found: {api_key[:20]}...")
    
    # Create generator
    generator = StoryImageGeneratorDALLE3(api_key, args.output)
    generator.request_delay = args.delay
    
    # Generate images
    generator.generate_all_images(
        start_page=args.start,
        end_page=args.end,
        quality=args.quality,
        size=args.size
    )

if __name__ == "__main__":
    main()